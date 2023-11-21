

#database setup and initialisation
db.init_app(app)
app.app_context().push() #  pushing the created "app" inside application context. App context is the space where our application is run, db is imported and controllers are configured.


#db configurations
app.config['SECRET_KEY'] = "helloworld"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket.db'