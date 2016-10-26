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

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/register", methods=['GET'])
def register_form():
    """Show page for the register form."""

    return render_template("register_form.html")



@app.route("/register", methods=['POST'])
def register_process():
    """Action for a login form."""

    email = request.form.get('email')
    password = request.form.get('password')

    current_user = User.query.filter_by(email = email).first()

    if current_user:
        if email != current_user.email:
            flash('Invalid credentials')
        else: 
            if current_user.password == password:
                session["current_user"] = email
                flash("You are successfully logged in")
                return redirect ("/")
            else: 
                flash("Wrong password!")
                return redirect("/register")
    else:
        flash("User not exist!")
        return redirect("/register")

@app.route("/logout", methods=['GET'])
def register_form():
    """Show logout page."""

    if session["current_user"]:
        session.pop('current_user')
        flash("Logged out!")
    return redirect ("/")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
    
