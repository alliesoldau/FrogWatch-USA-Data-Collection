import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from helpers import apology, login_required, lookup, usd

app = Flask(__name__)

if __name__ == "__main__":
    app.run()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure library to use SQLite database
db = SQL("sqlite:///watchdata.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Default route
@app.route("/")
@login_required
def index():
    # Get the user id from the current session
    user_id = session["user_id"]
    # Pull memberID from userdata database
    memberID_db = db.execute("SELECT memberID FROM userdata WHERE id = :id", id=user_id)
    member_ID = memberID_db[0]["memberID"]
    # Using the member id gather the info from the watch log table
    watchlogdata = db.execute("SELECT siteID, dateoflog, windspeed, precipitation, precipitationpast48, temp, americantoad, springpeeper, graytreefrog, bullfrog, greenfrog, northernleopardfrog, pickerelfrog, woodfrog, fowlerstoad, easternspadefoot FROM watchlogs WHERE memberID = ?", member_ID)
    surveysitedata = db.execute("SELECT id, sitename, latitude, longitude, sitezip, sitecharacterization, sitehabitat, waterpresence, wetlandorigin, watersource FROM surverysitereg WHERE memberID = ?", member_ID)
    # Pass this information to portfolio.html so we can display it can be displayed
    return render_template("index.html", watchlog = watchlogdata, surveydata = surveysitedata)


# Register user
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else: # This implies that it's talking about if it's a POST...
        memberID = request.form.get("memberID")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        datejoined = datetime.datetime.now()

        # Check that the user has input a member ID, password, and confirmation password
        if not memberID:
            return apology("Oops! You must enter a member ID to proceed.")
        if not password:
            return apology("Uh oh, you forgot to enter a password. Please input a password to proceed")
        if not confirmation:
            return apology("Please confirm your password to proceed")

        # Check that the memberID is the correct length
        if len(memberID) != 5:
            return apology("Member ID must be 5 numbers long")

        # Check that the password is the correct length
        if len(password) < 5:
            return apology("Password must be at least 5 values long")

        # Check that the password and confirmation password are identfical
        if password != confirmation:
            return apology("Passwords do not match. Please try again")

        # Hash the password for secure storage in the database
        hash = generate_password_hash(password)

        memberIDcheck = db.execute("SELECT COUNT(*) FROM userdata GROUP BY memberID HAVING memberID = :memberID", memberID=memberID)

        if len(memberIDcheck) > 0:
            return apology("Member ID already exists. Please pick another.")

        # However if we try and the member ID does already exist it means we need to come up with another member ID (prompt an apology)
        else:
            new_user = db.execute("INSERT INTO userdata (memberID, hash, datejoined) VALUES (?, ?, ?)", memberID, hash, datejoined)



        # Make it so immediatebly after you register it logs you in so you don't have to go back and login yourself. User session for this
        session["user_id"] = new_user

        return redirect("/") # Redirect back to the main page

# Log in user
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("memberID"):
            return apology("Must provide member ID", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM userdata WHERE memberID = ?", request.form.get("memberID"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
#Homepage
@app.route("/homepage")
def homepage():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return render_template("homepage.html")

#Log out user
@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

#Monitoring protocols
@app.route("/protocols")
@login_required
def protocols():
    # Redirect user to login form
    return render_template("protocols.html")


# User profile
@app.route("/profile")
@login_required
def profile():
    # Get the user id from the current session
    user_id = session["user_id"]
    # Using the user id gather the info from the userdata table
    namedata_db = db.execute("SELECT firstname, lastname, email, homechapter FROM userdata WHERE id = ?", user_id)
    # Pass this information to portfolio.html so we can display it can be displayed
    return render_template("profile.html", namedata = namedata_db)

# Update member information form
@app.route("/updateprofile", methods=["GET", "POST"])
@login_required
def updateprofile():
    if request.method == "GET":
        return render_template("updateprofile.html")

    else:
        # Ensure all member info has been submitted
        if not request.form.get("firstname"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("lastname"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("homechapter"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("email"):
            return apology("You must fill out all fields to continue", 403)

        # Get the user id from the current session
        user_id = session["user_id"]
        # Update the database with the updated user information
        db.execute("UPDATE userdata SET firstname = ?, lastname = ?, homechapter= ?, email = ? WHERE id = ?", request.form.get("firstname"), request.form.get("lastname"), request.form.get("homechapter"), request.form.get("email"), user_id)

        # Display to the user that we successful bought the stock
        flash("Member information updated!")

        # Redirect to the member profile
        return redirect("/profile")

@app.route("/logwatches", methods=["GET", "POST"])
@login_required
def logwatches():
    if request.method == "GET":
        return render_template("logwatches.html")

    else:
        # Get the user id from the current session
        user_id = session["user_id"]
        # Pull memberID and homechapter from the userdata database
        memberID_db = db.execute("SELECT memberID FROM userdata WHERE id = :id", id=user_id)
        member_ID = memberID_db[0]["memberID"]
        homechapter_db = db.execute("SELECT homechapter FROM userdata WHERE id = :id", id=user_id)
        homechapter_ID = homechapter_db[0]["homechapter"]
        # Gather information from the watch log form
        siteID = request.form.get("siteID")
        dateoflog = request.form.get("dateoflog")
        starttime = request.form.get("starttime")
        endtime = request.form.get("endtime")
        windspeed = request.form.get("windspeed")
        precipitation = request.form.get("precipitation")
        precipitationpast48 = request.form.get("precipitationpast48")
        temp = request.form.get("temp")
        americantoad = request.form.get("americantoad")
        springpeeper = request.form.get("springpeeper")
        graytreefrog = request.form.get("graytreefrog")
        bullfrog = request.form.get("bullfrog")
        greenfrog = request.form.get("greenfrog")
        northernleopardfrog = request.form.get("northernleopardfrog")
        pickerelfrog = request.form.get("pickerelfrog")
        woodfrog = request.form.get("woodfrog")
        fowlerstoad = request.form.get("fowlerstoad")
        easternspadefoot = request.form.get("easternspadefoot")

        # Ensure all member info has been submitted
        if not request.form.get("siteID"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("dateoflog"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("starttime"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("endtime"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("windspeed"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("precipitation"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("precipitationpast48"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("temp"):
            return apology("You must fill out all fields to continue", 403)
        if not request.form.get("americantoad"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("springpeeper"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("graytreefrog"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("bullfrog"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("northernleopardfrog"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("pickerelfrog"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("woodfrog"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("fowlerstoad"):
            return apology("You must fill out all fields to continue", 403)
        elif not request.form.get("easternspadefoot"):
            return apology("You must fill out all fields to continue", 403)

        # Update the database with the watch log and userinformation
        db.execute("INSERT INTO watchlogs (homechapter, memberID, siteID, dateoflog, starttime, endtime, windspeed, precipitation, precipitationpast48, temp, americantoad, springpeeper, graytreefrog, bullfrog, greenfrog, northernleopardfrog, pickerelfrog, woodfrog, fowlerstoad, easternspadefoot) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", homechapter_ID, member_ID, siteID, dateoflog, starttime, endtime, windspeed, precipitation, precipitationpast48, temp, americantoad, springpeeper, graytreefrog, bullfrog, greenfrog, northernleopardfrog, pickerelfrog, woodfrog, fowlerstoad, easternspadefoot)

        # Display to the user that we successful bought the stock
        flash("Your watch has been logged!!")

        # Redirect to the member profile
        return redirect("/")

@app.route("/surverysitereg", methods=["GET", "POST"])
@login_required
def surverysitereg():
    if request.method == "GET":
        return render_template("surverysitereg.html")

    else:
        # Get the user id from the current session
        user_id = session["user_id"]
        # Pull user data from userdata database
        memberID_db = db.execute("SELECT memberID FROM userdata WHERE id = :id", id=user_id)
        member_ID = memberID_db[0]["memberID"]
        homechapter_db = db.execute("SELECT homechapter FROM userdata WHERE id = :id", id=user_id)
        homechapter_ID = homechapter_db[0]["homechapter"]
        firstname_db = db.execute("SELECT firstname FROM userdata WHERE id = :id", id=user_id)
        firstname_ID = firstname_db[0]["firstname"]
        lastname_db = db.execute("SELECT lastname FROM userdata WHERE id = :id", id=user_id)
        lastname_ID = lastname_db[0]["lastname"]
        email_db = db.execute("SELECT email FROM userdata WHERE id = :id", id=user_id)
        email_ID = email_db[0]["email"]
        datecreated = datetime.datetime.now()
        # Gather information from the survery site registration form
        address = request.form.get("address")
        zipcode = request.form.get("zipcode")
        sitename = request.form.get("sitename")
        sitezip = request.form.get("sitezip")
        sitecharacterization = request.form.get("sitecharacterization")
        sitehabitat = request.form.get("sitehabitat")
        waterpresence = request.form.get("waterpresence")
        wetlandorigin = request.form.get("wetlandorigin")
        watersource = request.form.get("watersource")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        # Ensure all member info has been submitted
        if not request.form.get("address"):
            return apology("You must fill out all fields to continue.", 403)
        elif not request.form.get("zipcode"):
            return apology("You must fill out all fields to continue.", 403)
        elif not request.form.get("sitename"):
            return apology("You must fill out all fields to continue.", 403)
        elif not request.form.get("sitezip"):
            return apology("You must fill out all fields to continue.", 403)
        elif not request.form.get("sitecharacterization"):
            return apology("You must fill out all fields to continue.", 403)
        elif not request.form.get("sitehabitat"):
            return apology("You must fill out all fields to continue.", 403)
        elif not request.form.get("waterpresence"):
            return apology("You must fill out all fields to continue.", 403)
        if not request.form.get("wetlandorigin"):
            return apology("You must fill out all fields to continue.", 403)
        elif not request.form.get("watersource"):
            return apology("You must fill out all fields to continue.", 403)
        elif not request.form.get("latitude"):
            return apology("You must fill out all fields to continue.", 403)
        elif not request.form.get("longitude"):
            return apology("You must fill out all fields to continue.", 403)


        # Update the database with the watch log and userinformation
        db.execute("INSERT INTO surverysitereg (homechapter, memberID, firstname, lastname, email, datecreated, address, zipcode, sitename, sitezip, sitecharacterization, sitehabitat, waterpresence, wetlandorigin, watersource, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", homechapter_ID, member_ID, firstname_ID, lastname_ID, email_ID, datecreated, address, zipcode, sitename, sitezip, sitecharacterization, sitehabitat, waterpresence, wetlandorigin, watersource, latitude, longitude)

        # Display to the user that we successful bought the stock
        flash("Your site has been registered!!")

        # Redirect to the member profile
        return redirect("/")