from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps


# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username, password and confirmation were submitted
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            flash("All fields are required.", "error")
            return redirect("/register")

        # Ensure password and confirmation match
        if password != confirmation:
            flash("Must confirm password.", "error")
            return redirect("/logbook")

        # Query database for username and ensure username does not already exist
        existing_users = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(existing_users) > 0:
            flash("Username already registered.", "error")
            return redirect("/logbook")

        # hash password
        hash = generate_password_hash(password)

        # Insert new user into database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        # Query database for newly inserted user
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username.", "error")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password.", "error")
            return redirect("/login")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("Invalid login details.", "error")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/logbook", methods=["GET", "POST"])
@login_required
def logbook():
    if request.method == "POST":

        date = request.form.get("date")
        name = request.form.get("name")
        mode = request.form.get("mode")
        supervision_code = request.form.get("supervision_code")
        hospital = request.form.get("hospital")

        # Check if all fields are provided, return error if not
        if not date or not name or not mode or not supervision_code or not hospital:
            flash("All fields are required.", "error")
            return redirect("/logbook")

        # Insert the operation into the database
        db.execute("INSERT INTO operations (user_id, date, name, mode, supervision, hospital) VALUES (?, ?, ?, ?, ?, ?)",
                session["user_id"], date, name.title(), mode.title(), supervision_code.upper(), hospital.title())

        # Redirect to the logbook page or another page as desired after successful insertion
        return redirect("/logbook")

    else:
        # Fetch existing operations from the database
        operations = db.execute("SELECT id, date, name, mode, supervision, hospital FROM operations WHERE user_id = ?", session["user_id"])

        # Aggregate the number of each operation
        operation_counts = db.execute("SELECT name, COUNT(*) as total_number FROM operations WHERE user_id = ? GROUP BY name", session["user_id"])

        return render_template("logbook.html", operations=operations, operation_counts=operation_counts)



@app.route("/delete_operation", methods=["POST"])
@login_required
def delete_operation():
    operation_id = int(request.form.get("operation_id"))
    print("Operation ID to delete:", operation_id)

    if operation_id:
        db.execute("DELETE FROM operations WHERE id = ? AND user_id = ?", operation_id, session["user_id"])
    else:
        flash("Operation could not be deleted.", "error")

    return redirect("/logbook")


@app.route("/operations")
@login_required
def operations():
    return render_template("operations.html")


@app.route("/appendicectomy")
@login_required
def appendicectomy():
    return render_template("appendicectomy.html")


@app.route("/cholecystectomy")
@login_required
def cholecystectomy():
    return render_template("cholecystectomy.html")


@app.route("/laparotomy")
@login_required
def laparotomy():
    return render_template("laparotomy.html")
