from flask import Flask,render_template
# from flask_sqlalchemy import SQLAlchemy---already imported in models.py
from os import path
from flask_login import LoginManager
from models import *

#declaring function for creating flask app under Flask()
app = Flask(__name__)

#database setup and initialisation
db.init_app(app)
app.app_context().push() #  pushing the created "app" inside application context. App context is the space where our application is run, db is imported and controllers are configured.


#db configurations
app.config['SECRET_KEY'] = "helloworld"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#db setup completed


#importing blueprints for all views and authorisation functionality
from views import views
from auth import auth

app.register_blueprint(views)
app.register_blueprint(auth)


#Setting up Login Manager

login_manager = LoginManager()
login_manager.login_view = "auth.user_login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))











#Page not found error
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

#internal server error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"),500



if __name__=="__main__":    
    app.run(debug=True)
    

