import os
import sqlite3
from flask import Flask, redirect, render_template, request, session
from ticketsense import loopy
from apscheduler.schedulers.background import BackgroundScheduler



app = Flask(__name__)



def db_connection():
    db = sqlite3.connect('ticketsense.db')
    db.row_factory = sqlite3.Row
    return db

def db_insert(arg1, arg2=''):
    conn = db_connection()
    db = conn.cursor()
    db.execute(arg1, arg2)
    conn.commit()
    conn.close()

def db_select(arg1, arg2=''):
    db = db_connection()
    out = db.execute(arg1, arg2)
    return out.fetchall()




@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        link = request.form.get("link")
        filmname = request.form.get("filmname")
        date = request.form.get("date")

        if not link:
            return render_template("error.html", message="Enter correct link")
        elif not filmname:
            return render_template("error.html", message="Enter correct filmname")
        elif not date:
            return render_template("error.html", message="Enter correct date")

        else:
            newlink = link.rsplit('/', 1)
            newfilmname = filmname.rsplit(' ', 1)
            startdate = date.rsplit('/')

            db_insert("INSERT INTO ticketsensedata (link, name, day, month, year) VALUES (?, ?, ?, ?, ?)",
                    (newlink[0], newfilmname[0], startdate[0], startdate[1], startdate[2]))

            return redirect("/submitted")

    else:
        return render_template("index.html")


@app.route("/submitted")
def submitted():
    datas = db_select("SELECT * FROM ticketsensedata")
    return render_template("submitted.html", datas=datas)


@app.route("/deregister", methods=["POST"])
def deregister():
    id = request.form.get("id")
    if id:
        db_insert("DELETE FROM ticketsensedata WHERE id = ?", (id,))
    return redirect("/submitted")


def test_job():
    loopy()

scheduler = BackgroundScheduler()
job = scheduler.add_job(test_job, 'interval', seconds=60)
scheduler.start()


if __name__ == '__main__':
    app.run()

