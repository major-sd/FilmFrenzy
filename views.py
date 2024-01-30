from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required,current_user
from models import * #import database details
from sqlalchemy import or_
from datetime import *





#creating blueprint for views page
views = Blueprint("views", __name__)



#represents homepage
@views.route("/")
def home():
    return render_template("home.html",user=current_user, admin=current_user)




#represents admin-dashboard with created venues onscreen
@views.route("/admin_dashboard/<int:id>")
@login_required # only admin
def admin_dashboard(id):
    
    id=current_user.id
    
    if not (current_user.admin): # Ensures only admin can access this page (current.admin= 0 or 1)
        return render_template("404.html")
    
    venues=Venue.query.all()
    
    return render_template("admin_dashboard.html", admin=current_user, user=current_user, venue=venues, id=id)




#represnt user dashboard display with recently added shows
@views.route("/user_dashboard/<int:id>")
@login_required # user and admin
def user_dashboard(id):
    
    id=current_user.id
    
    shows=Show.query.order_by(Show.id.desc()).all()
    # vname=Venue.query.get(shows.venue_id)
        
    return render_template("user_dashboard.html", user=current_user,admin=current_user,shows=shows,id=id)



#adding new venues from admin page
@views.route("/add_venue", methods=['GET','POST'])
@login_required # only admin
def add_venue():
    
    if not (current_user.admin):
        return render_template("404.html")
    
    if(request.method=="POST"):
        name=request.form.get("name")
        location=request.form.get("location")
        capacity=request.form.get("capacity")
        vimg=request.form.get("image")
        print(vimg)
        
        v=Venue(name=name,location=location,capacity=capacity,vimg=vimg)
        db.session.add(v)
        db.session.commit()
        flash('Venue added successfully!', category="success")
        return redirect(url_for('views.admin_dashboard', admin=current_user, id=current_user.id))
        
        
    return render_template("add_venue.html", user=current_user, admin=current_user)





#editing venues from admin page
@views.route("/<int:venue_id>/edit_venue", methods=['GET','POST'])
@login_required # only admin
def edit_venue(venue_id):
    
    v=Venue.query.get(venue_id)
    
    if not (current_user.admin):
        return render_template("404.html")
    
    if(request.method=="POST"):
        name=request.form.get("name")
        location=request.form.get("location")
        capacity=request.form.get("capacity")
        vimg=request.form.get("image")
        
        
        
        print(vimg)
        
        if name:
            v.name=name
        
        if location:    
            v.location=location
        
        if capacity:
            v.capacity=capacity
        
        if vimg:    
            v.vimg=vimg
        # v=Venue(name=name,location=location,capacity=capacity,vimg=vimg)
        # db.session.add(v)
        db.session.commit()
        flash(f'Venue {venue_id} edited successfully!', category="success")
        return redirect(url_for('views.admin_dashboard', admin=current_user, id=current_user.id))
        
        
    return render_template("edit_venue.html", user=current_user, admin=current_user,v=v)





#deleting venues from admin page
@views.route("/delete_venue/<int:venue_id>", methods=['GET','POST'])
@login_required # only admin
def delete_venue(venue_id):
    
    if not (current_user.admin):
        return render_template("404.html")
        
    v=Venue.query.get(venue_id)
    vname=v.name
    db.session.delete(v)
    db.session.commit()
    flash(f'Venue {vname} deleted successfully!', category="success")
    return redirect(url_for('views.admin_dashboard', admin=current_user, id=current_user.id))
    
    
    
    
    
    
    
    
    
    
    
    
    
      
#display shows of a particular venue on clicking SHOW button of a venue
@views.route("/<int:venue_id>/show")
@login_required # only admin
def shows(venue_id):
    
    if not (current_user.admin):
        return render_template("404.html")
        
    v=Venue.query.get(venue_id)
    shows=Show.query.filter_by(venue_id=v.id).all()
        
    return render_template("shows.html",admin=current_user,user=current_user, id=current_user.id, shows=shows, v=v)
    
    
    
    


#Adding Shows under particular venue
@views.route("/<int:venue_id>/add_shows", methods=['GET','POST'])
@login_required # only admin
def add_shows(venue_id):
    
    if not (current_user.admin):
        return render_template("404.html")
    
    
    v=Venue.query.get(venue_id)
    
    if request.method=='POST':
        name=request.form.get("name")
        tags=request.form.get("tags")
        price=request.form.get("price")
        
        # show_timing=request.form.get("show_timing")
        
        venue_id=v.id
        
        # show_capacity=v.capacity
        
        simg=request.form.get("image")
        strailer=request.form.get("trailer")
        print(simg)
        
        ##vvip
        s=Show(name=name,tags=tags,price=price,venue=v,s_img=simg,s_trailer=strailer)
        #in this we pass obj of venue as "venue=v" in place of venue_id field, this allows to access venue table
        # fields directly from "show" objects for e.g. "s.venue.name" (name of corresp venue related to "s")
        
        db.session.add(s)
        db.session.commit()
        flash(f'Show added successfully to {v.name}!', category="success")
        
        # logic for slotting date for 3 days only
        today=datetime.now()
        tmrw= today + timedelta(days=1)
        max_date= today + timedelta(days=2)
        
        ps1m= Slot(venue=v,show=s,show_date=today,show_time="M",slot_capacity=v.capacity)# premiere slot 1 "M"-> Morning
        ps1e= Slot(venue=v,show=s,show_date=today,show_time="E",slot_capacity=v.capacity)# "E"->Evening
        ps1n= Slot(venue=v,show=s,show_date=today,show_time="N",slot_capacity=v.capacity)# "N"-> Night
        
        ps2m= Slot(venue=v,show=s,show_date=tmrw,show_time="M",slot_capacity=v.capacity)
        ps2e= Slot(venue=v,show=s,show_date=tmrw,show_time="E",slot_capacity=v.capacity)
        ps2n= Slot(venue=v,show=s,show_date=tmrw,show_time="N",slot_capacity=v.capacity)
        
        ps3m= Slot(venue=v,show=s,show_date=max_date,show_time="M",slot_capacity=v.capacity)
        ps3e= Slot(venue=v,show=s,show_date=max_date,show_time="E",slot_capacity=v.capacity)
        ps3n= Slot(venue=v,show=s,show_date=max_date,show_time="N",slot_capacity=v.capacity)
        
        db.session.add_all([ps1m,ps1e,ps1n,ps2m,ps2e,ps2n,ps3m,ps3e,ps3n])
        db.session.commit()
        
        return redirect(f"/{venue_id}/show")  
    
    return render_template("add_show.html",admin=current_user,user=current_user, id=current_user.id, v=v)







# edit shows details
@views.route("/<int:venue_id>/<int:show_id>/edit_shows", methods=['GET','POST'])
@login_required # only admin
def edit_shows(venue_id,show_id):
    
    if not (current_user.admin):
        return render_template("404.html")
    
    
    v=Venue.query.get(venue_id)
    s=Show.query.get(show_id)
    
    if request.method=='POST':
        name=request.form.get("name")
        tags=request.form.get("tags")
        price=request.form.get("price")
        show_timing=request.form.get("show_timing")
        venue_id=v.id
        show_capacity=v.capacity
        
        simg=request.form.get("image")
        print(simg)
        
        if name:
            s.name=name
            
        
        if tags:
            s.tags=tags
            
            
        if price:
            s.price=price
            
            
        if show_timing:
            s.show_timing=show_timing
            
            
        if simg:
            s.s_img=simg
            
        
        ##vvip
        # s=Show(name=name,tags=tags,price=price,show_timing=show_timing,venue=v,show_capacity=show_capacity,simg=simg)
        #in this we pass obj of venue as "venue=v" in place of venue_id field, this allows to access venue table
        # fields directly from "show" objects for e.g. s.venue.name (name of corresp venue related to "s")
        
        # db.session.add(s)
        db.session.commit()
        flash(f'Show {show_id} edited successfully to {v.name}!', category="success")
        return redirect(f"/{venue_id}/show")  
    
    return render_template("edit_show.html",admin=current_user,user=current_user, id=current_user.id, v=v,s=s)



    





#for deleting show under particular venue_id
@views.route("/delete_show/<int:show_id>", methods=['GET','POST'])
@login_required # only admin
def delete_show(show_id):
    
    if not (current_user.admin):
        return render_template("404.html")
     
    s=Show.query.get(show_id)
    v=s.venue_id
    sname=s.name
    db.session.delete(s)
    db.session.commit()
    flash(f'Show {sname} deleted successfully!', category="success")
    return redirect(f"/{v}/show")




#for booking show by user under user dashboard
@views.route("/<int:user_id>/<int:show_id>/book_show", methods=['GET','POST'])
@login_required # admin and user
def book_show(user_id,show_id):
    
    if(user_id != current_user.id):  #so that other users cannot intrude
        return render_template("404.html")
    
    u=User.query.get(user_id)
    s=Show.query.get(show_id)
    v=Venue.query.get(s.venue.id)#important concept
    
    today=date.today()
    max_date= today + timedelta(days=2)
    
    
   
    
    
    
    if request.method=="POST":
        seats=int(request.form.get("seats")) #required seats for booking
        total_price= s.price * seats
        
        book_date_str=request.form.get("date") # getting prefferred booking date
        book_date = datetime.strptime(book_date_str, '%Y-%m-%d').date()
        frmtd_date = book_date.strftime("%d/%m/%Y")# formatted date to dd/mm/yyyy
        print(book_date)
        book_time=request.form.get("time") # getting prefferred booking time(Morn,eve,Night)
        
        slot_time={
                    "Morning":"M",
                    "Evening":"E",
                    "Night":"N"
                   }
        curr_slot_details=(Slot.query.filter(Slot.show_id==s.id, Slot.venue_id==v.id, Slot.show_date==book_date,Slot.show_time==slot_time[book_time]).first())
        # returns current slot details as per user query
        curr_slot_cap=curr_slot_details.slot_capacity
        
        print(curr_slot_details)
        print(curr_slot_cap)
        
        
        
        if seats<0:
            flash(f'Please enter valid number of seats', category="error")
            return redirect(f"/{u.id}/{s.id}/book_show")
            
        if curr_slot_cap >= seats:
            
            b=Booking(user=u,venue=v,show=s, seats_book=seats, total_price=total_price,book_date=book_date,book_time=book_time)
            db.session.add(b)
            db.session.commit()
            curr_slot_details.slot_capacity= curr_slot_cap-seats
            db.session.commit()
            print(curr_slot_cap)
            flash(f'Hurray!! Booked {seats} ticket(s) for {s.name} at {s.venue.name} on {frmtd_date} (Slot: {book_time}) at Rs. {total_price}.', category="success")
        
            return redirect(f"/user_dashboard/{u.id}")
                
        
        # s.show_capacity=s.show_capacity-seats
        # db.session.commit()
        
        if curr_slot_cap>0:
            flash(f'OOps!! Only {curr_slot_cap} seats are remaining', category="success")
            return redirect(f"/{u.id}/{s.id}/book_show")
            
        else:
            flash(f'Show is housefull for the provided slo', category="success")
            return redirect(f"/{u.id}/{s.id}/book_show")
            # return render_template("book_show.html",admin=current_user,user=current_user, id=current_user.id,show_name=s.name,venue_name=v.name,show_price=s.price,venue_location=v.location,min_date=today,max_date=max_date )
                
    return render_template("book_show.html",admin=current_user,user=current_user, id=current_user.id,show_name=s.name,venue_name=v.name,show_price=s.price,venue_location=v.location,min_date=today,max_date=max_date )   
        


#Shows user bookings under "My Bookings Section"
@views.route("/<int:user_id>/bookings", methods=['GET','POST'])
@login_required # admin and user
def user_bookings(user_id):
    
    if(user_id!= current_user.id):  #so that other users cannit intrude
        return render_template("404.html")
    
    user=User.query.get(user_id)
    user_booking=user.booking #returns a list of booking objects under given user id (concept of backref)
    user_booking.sort(key=book_id,reverse=True)
    
    if request.method=="POST":
        ratings=int(request.form.get("rate"))
        sid=int(request.form.get("show_id"))
        vid=int(request.form.get("venue_id"))
        s=Show.query.get(sid)
        v=Venue.query.get(vid)
        
        x=Usr.query.filter(Usr.user_id==user.id, Usr.show_id==s.id).first()
        
        if x:  # checking iff x exists in the USR table or not
            x.ratings=ratings
            db.session.commit()
            print(x)
            avg_rate(sid)
            flash(f"You rated {s.name} with {ratings}")
            return render_template("user_bookings.html",admin=current_user,user=current_user, id=current_user.id, ub=user_booking,x=x)
            
            
        else:
            umr=Usr(user=user,show=s,ratings=ratings)#user-movie-rating
            # s.rating=ratings
            db.session.add(umr)
            db.session.commit()
            x=Usr.query.filter(Usr.user_id==user.id, Usr.show_id==s.id).first()
            print(x)
            avg_rate(sid)
            flash(f"You rated {s.name} with {ratings}")
            return render_template("user_bookings.html",admin=current_user,user=current_user, id=current_user.id, ub=user_booking,x=x)
        
    
    
    
    
    
    return render_template("user_bookings.html",admin=current_user,user=current_user, id=current_user.id, ub=user_booking,x=None)

def book_id(booking):
        return booking.id



#function to calculate dynamic avg rating of show by the user
def avg_rate(show_id):
    s=Show.query.get(show_id)
    sr=s.ratings
    sl=[]
    
    for r in sr:
        sl.append(r.ratings)
        
    avg_rate=sum(sl)/len(sl)
    f_avg_rate='{:0.2f}'.format(avg_rate) #for storing only two values after decimal
    s.avg_rating=f_avg_rate
    db.session.commit()
     
    return



#Shows user Profile under "My Profile Section"
@views.route("/<int:user_id>/myprofile")
@login_required # admin and user
def myprofile(user_id):
    
    if(user_id != current_user.id):  #so that other users cannit intrude
        return render_template("404.html")
    
    user=User.query.get(user_id)
    b=user.booking
    return render_template("myprofile.html",admin=current_user,user=current_user,id=current_user.id,nb=len(b))   




#Custom Search functionality
@views.route("/search", methods=["GET","POST"])
@login_required # admin and user
def search(): 
    
    if request.method=="POST":
        op=request.form.get("op")#selected option
        qry=request.form.get("qry")#query in search bar...
        
        if op=="Shows":
            
            shows=Show.query.filter(Show.name.like(f"%{qry}%")).all()
            return render_template("user_dashboard.html", user=current_user,admin=current_user,shows=shows,id=current_user.id)
        
        elif op=="Venues":
            
            venues=Venue.query.filter(Venue.name.like(f"%{qry}%")).all()
            
            x=[]
            shows=[]
            for v in venues:
                x.append(v.shows)
                
            for i in range(len(x)):
                for j in range(len(x[i])):
                    shows.append(x[i][j])
                    
                    
            return render_template("user_dashboard.html", user=current_user,admin=current_user,shows=shows,id=current_user.id)
        
        
        elif op=="Location":
            
            venues=Venue.query.filter(Venue.location.like(f"%{qry}%")).all()
            
            x=[]
            shows=[]
            for v in venues:
                x.append(v.shows)
                
            for i in range(len(x)):
                for j in range(len(x[i])):
                    shows.append(x[i][j])
                    
                    
            return render_template("user_dashboard.html", user=current_user,admin=current_user,shows=shows,id=current_user.id)
        
        
        
        
        elif op=="Tags":
            
            shows=Show.query.filter(Show.tags.like(f"%{qry}%")).all()
            
            
                    
                    
            return render_template("user_dashboard.html", user=current_user,admin=current_user,shows=shows,id=current_user.id)
        
        
        
        
        elif op=="Show-Timing":
            
            shows=Show.query.filter(Show.show_timing.like(f"{qry}%")).all()
            
            
                    
                    
            return render_template("user_dashboard.html", user=current_user,admin=current_user,shows=shows,id=current_user.id)
        
        
        elif op=="Available Shows":
            
            shows=Show.query.filter(Show.show_capacity>0).all()
            
            
                    
                    
            return render_template("user_dashboard.html", user=current_user,admin=current_user,shows=shows,id=current_user.id)
        
        
        
        elif op=="Ratings":
            
            shows=Show.query.filter(Show.avg_rating>=qry).all()
            
            
                    
                    
            return render_template("user_dashboard.html", user=current_user,admin=current_user,shows=shows,id=current_user.id)
        
        
        elif op=="Price":
            
            price=int(qry)
            
            shows=Show.query.filter(Show.price<=price).all()
            
            
            
        
            
            
                    
                    
            return render_template("user_dashboard.html", user=current_user,admin=current_user,shows=shows,id=current_user.id)
        
        
        
            
            
        
    
    return render_template("search.html",admin=current_user,user=current_user,id=current_user.id)


@views.route("/add_canteen", methods=['GET','POST'])
@login_required # only admin
def add_canteen():
    return render_template("canteen.html",admin=current_user, user=current_user,id=current_user.id)
    






   




















    