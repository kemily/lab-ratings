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

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show information of the chosen user."""

    user = User.query.filter_by(user_id=user_id).first()
   
    return render_template("user_info.html", user=user)



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

    current_user = User.query.filter_by(email = email).first()

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
    
