from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import * #import databse details
from flask_login import login_user, logout_user, login_required, current_user #for login sessions 
from werkzeug.security import generate_password_hash, check_password_hash #for password hashing 

# NOTE: once user is logged in, "current_user" can be used as variable to fetch credentials of User model
# i.e. current_user.id, current_user.name, current_user.username, current_user.userpassword


#creating blueprint for login page
auth = Blueprint("auth", __name__)


@auth.route("/adminlogin", methods=["GET","POST"])
def admin_login():
    
    if request.method=='POST':
        
        username=request.form.get("admin_username")
        password=request.form.get("admin_password")
        
        user=User.query.filter(User.username==username).first()
        
        if user and user.admin:
            if check_password_hash(user.userpassword,password):
                flash("Logged in Successfully as Admin...", category="success")
                login_user(user)
                return redirect(url_for("views.admin_dashboard",id=current_user.id,user=current_user))
            
            else:
                flash('Password is incorrect.Try again...', category='error')
        else:
            flash('Sorry!! Admin does not exist.', category='error')
    
    return render_template("admin_login.html",user=current_user)




@auth.route("/userlogin", methods=['GET','POST'])
def user_login():
    
    if request.method=='POST':
        
        username=request.form.get("username")
        password=request.form.get("password")
        
        user=User.query.filter(User.username==username).first()
        
        if user:
            if check_password_hash(user.userpassword,password):
                login_user(user)
                flash("Logged in Successfully...", category="success")
                return redirect(url_for("views.user_dashboard",id=current_user.id,user=current_user))
            
            else:
                flash('Password is incorrect.Try again...', category='error')
        else:
            flash('Sorry!! Username does not exist. Please Sign Up...', category='error')
                
        
     
     
     
    return render_template("user_login.html",user=current_user)




@auth.route("/sign-up", methods=['GET','POST'])
def sign_up():
    
    if request.method=='POST':
        name=request.form.get("name")
        username=request.form.get("new_username")
        password=request.form.get("new_password")
        confirm_pass=request.form.get("confirm_password")
        
        exist_user= User.query.filter(User.username==username).first()
        
        if exist_user:
            flash("Username already exists", category="error")
            
        elif password != confirm_pass:
             flash("Passwords do not matches with entered password", category="error")
             
        elif len(username) < 4:
            flash('Username is too short.', category='error')
            
        elif len(password) < 5:
            flash('Password is too short.', category='error')
            
        else:
            new_user = User(name=name, username=username, userpassword=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)#logging in new user
            flash('User created successfully!', category="success")
            return redirect(url_for('views.home'))
        
    return render_template("sign-up.html",user=current_user)




@auth.route("/<int:user_id>/edit_profile")
@login_required # admin and user
def edit_profile(user_id):
    user=User.query.get(user_id)
    
    if request.method=='POST':
        
        name=request.form.get("name")
        nuname=request.form.get("nun")
        opass=request.form.get("opass")
        npass=request.form.get("npass")
        cnpass=request.form.get("cnpass")
        
        
        if name:
            user.name=name
        
            
            
        if nuname:
            user.username=nuname
            
            
            
        if opass:    
            
        
            if check_password_hash(user.userpassword,opass):
                if(npass==cnpass):
                    user.userpassword=generate_password_hash(cnpass)
                    
                    
                else:
                    flash("Confirm password does not matches with entered new password", category="error")
                    
                
            else:
                flash("Please enter your old password correctly", category="error")
                
        db.session.commit()
        flash("Profile updated successfully",category="success")       
        return redirect(f"/{user.id}/myprofile")
            
        
    return render_template("edit_profile.html",admin=current_user,user=current_user,id=current_user.id)


@auth.route("/logout")
@login_required # ensures only logged in user access this functionality
def logout():
    logout_user()
    flash("Logged Out successfully..........")
    return redirect(url_for("views.home"))