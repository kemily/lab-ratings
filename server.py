"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    #make a query to get all users
    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show information of the chosen user."""

    #get the first user with a user_id
    user = User.query.filter_by(user_id=user_id).first()
   
    return render_template("user_info.html", user=user)

@app.route("/movies")
def movie_list():
    """Show list of movies."""

    #make a query to get a list of all movies
    movies = Movie.query.order_by("title").all()
    return render_template("movie_list.html", movies=movies)

@app.route("/movies/<int:movie_id>", methods=["GET"])
def show_movie(movie_id):
    """Show information of the chosen movie."""

    #getting the first movie object with a movie_id
    movie = Movie.query.filter_by(movie_id=movie_id).first()
   
    return render_template("movie_info.html", movie=movie)

@app.route("/movies/<int:movie_id>", methods=['POST'])
def rate_process(movie_id):
    """Action for processing movie rating."""

    #get a rating from user input
    rating = request.form.get('rating')

    #get a user email from the current session
    user_email = session["current_user"]
    
    # get a current user object by the user email
    current_user_info = User.query.filter_by(email = user_email).first()
    #get a current user id
    current_user_id = current_user_info.user_id

    #get a current user rating.
    current_rating = Rating.query.filter_by(movie_id = movie_id, user_id = current_user_id).first()

    #if current user has no rating to the current movie
    #add a new rating instance
    #if not - update the current rating that the user has for the movie
    if current_rating is None:
        new_rating = Rating(movie_id=movie_id,
                            user_id=current_user_id, 
                            score = rating)
        db.session.add(new_rating)
    else: 
        current_rating.score = rating
    
    db.session.commit()

    flash("You rated successfully!!!")
    return redirect("/")


@app.route("/register", methods=['GET'])
def register_form():
    """Show page for the register form."""

    return render_template("register_form.html")


@app.route("/register", methods=['POST'])
def register_process():
    """Action for a register form."""

    email = request.form.get('email')
    password = request.form.get('password')
    age = request.form.get('age')
    zipcode = request.form.get('zipcode')

    #create a new_user instane of the User class, add it to database
    new_user = User(email=email, 
                    password=password, 
                    age=age, 
                    zipcode=zipcode)

    db.session.add(new_user)

    db.session.commit()

    flash("You are registered successfully!!!")
    return redirect("/")


@app.route("/login", methods=['GET'])
def login_form():
    """Show page for the login form."""

    return render_template("login_form.html")



@app.route("/login", methods=['POST'])
def login_process():
    """Action for a login form."""

    email = request.form.get('email')
    password = request.form.get('password')

    #get the current_user by email
    current_user = User.query.filter_by(email = email).first()

    #check if we have current_user, we validate the password
    #return to user_info page if password is correct
    #if not, flash message 
    if current_user:
        if current_user.password == password:
            session["current_user"] = email
            flash("You are successfully logged in")
            return render_template("user_info.html", user=current_user)
        else: 
            flash("Wrong password!")
            return redirect("/login")
    else:
        flash("User not exist!")
        return redirect("/login")

@app.route("/logout", methods=['GET'])
def user_logout():
    """Show logout page."""

    if session["current_user"]:
        del session['current_user']
        flash("Logged out!")
    return redirect ("/")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    app.jinja_env.auto_reload = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
    
