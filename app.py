#ticketsenseweb

# imports sqlite3 modules
import sqlite3

from flask import Flask, redirect, render_template, request

# used for scraping throught ticket booking websites
from ticketsense import loopy 
# used for setting cron jobs
from apscheduler.schedulers.background import BackgroundScheduler 


app = Flask(__name__)

# connect to SQLite database
def db_connection():
    db = sqlite3.connect('ticketsense.db')
    db.row_factory = sqlite3.Row
    return db

# function to simplify inserting commands to SQLite
def db_insert(arg1, arg2=''):
    conn = db_connection()
    db = conn.cursor()
    db.execute(arg1, arg2)
    conn.commit()
    conn.close()

# function to simplify selection commands to SQLite
def db_select(arg1, arg2=''):
    db = db_connection()
    out = db.execute(arg1, arg2)
    return out.fetchall()



# index route

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # when used in POST mode collects data from form inputs
        link = request.form.get("link")
        filmname = request.form.get("filmname")
        date = request.form.get("date")

        # verifies the data entered by the user
        if not link:
            return render_template("error.html", message="Enter correct link")
        elif not filmname:
            return render_template("error.html", message="Enter correct filmname")
        elif not date:
            return render_template("error.html", message="Enter correct date")

        else:

            # if all checks are complete, data is further formatted and stores inside ticketsensedata table in ticketsense.db
            newlink = link.rsplit('/', 1)
            newfilmname = filmname.rsplit(' ', 1)
            startdate = date.rsplit('/')

            db_insert("INSERT INTO ticketsensedata (link, name, day, month, year) VALUES (?, ?, ?, ?, ?)",
                    (newlink[0], newfilmname[0], startdate[0], startdate[1], startdate[2]))

            return redirect("/submitted")

    else:
        # In GET mode display the index page
        return render_template("index.html")


# submitted route
@app.route("/submitted")
def submitted():

    # selects data from database and passes it on to submitted.html
    datas = db_select("SELECT * FROM ticketsensedata")
    return render_template("submitted.html", datas=datas)

# route to deregister data from database
@app.route("/deregister", methods=["POST"])
def deregister():
    # gets the id of the deleted data
    id = request.form.get("id")
    if id:
        # if id is present/valid that data is deleted
        db_insert("DELETE FROM ticketsensedata WHERE id = ?", (id,))

        # then returns the same page updated
    return redirect("/submitted")

# cron function - used for calling at present time interval
def test_job():
    # scraping function from ticketsense.py
    loopy()

# scheduler setup code
scheduler = BackgroundScheduler()

# function and time assigned
job = scheduler.add_job(test_job, 'interval', seconds=60)

# starting scheduler with program
scheduler.start()

# if file is main then this is run
if __name__ == '__main__':
    app.run()

