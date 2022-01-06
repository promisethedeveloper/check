from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import SignUpForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///first_capstone_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route("/")
def homePage():
    """Show homepage with links to site areas."""

    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Registers a user. Produce form and handles form submissions."""

    if "user_id" in session:
        return redirect("/")

    
    form = SignUpForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        user = User.register(first_name, last_name, email, password)

        db.session.commit()

        session["user_id"] = user.id

        return redirect("/")
    else:
        return render_template("users/signup.html", form=form)



@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("user_id")

    return redirect("/")