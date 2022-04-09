# This file contains creates the SQL database and tables

from cs50 import SQL
from flask import Flask, render_template


app = Flask(__name__)

if __name__ == "__main__":
    app.run()

# Create database
open("watchdata.db", "w").close()
db = SQL("sqlite:///watchdata.db")

# Create table for user data
db.execute("CREATE TABLE userdata (id INTEGER PRIMARY KEY, memberID INTEGER, firstname TEXT, lastname TEXT, email VARCHAR, hash VARCHAR, homechapter VARCHAR, datejoined DATETIME)")

# Create table for watch logs
db.execute("CREATE TABLE watchlogs (id INTEGER PRIMARY KEY, memberID INTEGER, homechapter VARCHAR, siteID INTEGER, dateoflog DATETIME, starttime DATETIME, endtime DATETIME, windspeed INTEGER, precipitation VARCHAR, precipitationpast48 TEXT, temp TEXT, americantoad INTEGER, springpeeper INTEGER, graytreefrog INTEGER, bullfrog INTEGER, greenfrog INTEGER, northernleopardfrog INTEGER, pickerelfrog INTEGER, woodfrog INTEGER, fowlerstoad INTEGER, easternspadefoot INTEGER)")

# Create table for survery site registration
db.execute("CREATE TABLE surverysitereg (id INTEGER PRIMARY KEY, memberID INTEGER, firstname TEXT, lastname TEXT, email VARCHAR, homechapter VARCHAR, datecreated DATETIME, address VARCHAR, zipcode INTEGER, sitename VARCHAR, sitezip INTEGER, sitecharacterization VARCHAR, sitehabitat VARCHAR, waterpresence VARCHAR, wetlandorigin VARCHAR, watersource VARCHAR, latitude VARCHAR, longitude VARCHAR)")