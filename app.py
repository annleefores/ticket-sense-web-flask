import os
import sqlite3
from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)

heya = heya
      
def db_connection():
    db = sqlite3.connect('ticketsense.db')
    db.row_factory = sqlite3.Row
    return db

def db_insert(arg1, arg2):
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
        start = request.form.get("start")
        end = request.form.get("end")

        newlink = link.rsplit('/', 1)
        newfilmname = filmname.rsplit(' ', 1)
        startdate = start.rsplit('/')
        enddate = end.rsplit('/')

        print((link.rsplit('/'))[2])

        db_insert("INSERT INTO ticketsensedata (link, name, startday, startmonth, startyear, endday, endmonth, endyear) VALUES (?, ?, ?, ?, ?, ? ,?, ?)", 
                  (newlink[0], newfilmname[0], startdate[0], startdate[1], startdate[2], enddate[0], enddate[1], enddate[2]))
        
    
        p = db_select("SELECT * FROM ticketsensedata")
        

        for i in p:
            print(i["link"])

        return redirect("/submitted")

        
    else:
        return render_template("index.html")


@app.route("/submitted")
def submitted():
    return render_template("submitted.html")