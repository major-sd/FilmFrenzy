# Author
Soujit Das

# Ticket Show Web Application (FilmFrenzy)

The Ticket Show Application is a web-based application that allows multiple users to book movie tickets for different shows under different venues. The application has two parties - an admin and users. The admin can add/edit/delete movie shows, venues, and users, while the users can browse movies, view show timings, and book tickets. The web application consists multiple API’s to add/edit/delete venues and shows by the admin side.


## Tech Stack

- Flask: web framework for building the web application
- Flask-SQLAlchemy: ORM for connecting to the database and performing CRUD operations
- Flask-Login: extension for user authentication and authorization
- Werkzeug for password hashing
- SQLite: database for storing user, shows, venues and booking data
- Bootstrap: Bootstrap version 4.1 is used in this project for the HTML styling and overall frontend designing. 


## Database Schema
- Venues - This table stores the details of the venues which includes fields like ID, Name, Location and Capacity.



- Shows - This table stores the details of the movie shows which includes fields like ID, Show Name, Average Show Rating, Show Price, Timing, Venue ID of show and Show Capacity (i.e. Seat availability of the show).



- Users - This table stores the details of the users as well as admin. Here user with admin role is indicated with boolean value "True" in admin field of Users table. It also stores the user id and hashed password of the users which further helps in authorization and authentication of user.



- Bookings - This table stores all the details of the bookings made by a particular users.


- User-Show-Rating(USR)- This table stores the ratings for a particular show by a particular user. It helps in calculating dynamic average rating of a show.



The relationships between these tables are as follows:

- Users has many Bookings, Show Ratings for different shows
- Venue has many Shows and Bookings
- Show has many User Ratings and Bookings













## Architecture and Features
The Model-View-Controller (MVC) paradigm is used to organise the entire project. The controllers for processing requests and rendering templates are located in the views module of the application package. Controllers for handling user authentication and authorisation are present in the authentication module. Classes for database tables can be found in the models module. The HTML view templates are located in the templates folder. The application provides user registration and login, CRUD of shows/venues by admin, booking of shows by users, user ratings, distribution of dynamic average ratings to shows based on users' ratings, and multiple bookings by users. Moreover, the user can alter their username and password in My Profile section.



The Ticket Show Booking Application (FilmFrenzy) is a user-friendly and efficient web-based application that allows users to book movie tickets for different shows under different venues. The application provides an easy-to-use interface for browsing movies, viewing show timings, and booking tickets. The admin panel provides an efficient way to manage the application. The application well equipped with business logic to stop show bookings when show is houseful.  


## Installation and Usage

The application can be rendered on a web server using the following steps:

- Clone the project
- Unzip the Project 
- Create a virtual environment with command `python -m venv {{Foldername}}` in cmd
- Activate the virtual environment with `{{Foldername}}\Scripts\activate`
- Install the dependencies with `pip install -r requirements.txt`
- To run the flask app, on the shell, run `python app.py`
- Access the application at `http://localhost:5000`
