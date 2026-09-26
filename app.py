import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os
from statistics import mean

app=Flask(__name__)
app.secret_key="mca-project-secret"
DB="students.db"

def db():
    con=sqlite3.connect(DB)
    con.row_factory=sqlite3.Row
    return con

def init_db():
    con=db()
    con.execute("""CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, roll TEXT UNIQUE NOT NULL, course TEXT DEFAULT 'MCA',
        semester TEXT, marks REAL DEFAULT 0, attendance REAL DEFAULT 0,
        skills TEXT DEFAULT '', placement_status TEXT DEFAULT 'Preparing')""")
    con.commit(); con.close()

@app.route("/")
def index():
    con=db(); students=con.execute("SELECT * FROM students ORDER BY id DESC").fetchall(); con.close()
    total=len(students)
    avg_marks=round(mean([s["marks"] for s in students]),1) if students else 0
    avg_att=round(mean([s["attendance"] for s in students]),1) if students else 0
    placed=sum(s["placement_status"]=="Placed" for s in students)
    return render_template("index.html",students=students,total=total,avg_marks=avg_marks,avg_att=avg_att,placed=placed)

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method=="POST":
        data=(request.form["name"],request.form["roll"],request.form["semester"],
              request.form.get("marks",0),request.form.get("attendance",0),
              request.form.get("skills",""),request.form.get("placement_status","Preparing"))
        try:
            con=db(); con.execute("""INSERT INTO students
            (name,roll,semester,marks,attendance,skills,placement_status)
            VALUES(?,?,?,?,?,?,?)""",data); con.commit(); con.close()
            flash("Student added successfully.")
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash("Roll number already exists.")
    return render_template("form.html")

@app.route("/delete/<int:id>")
def delete(id):
    con=db(); con.execute("DELETE FROM students WHERE id=?",(id,)); con.commit(); con.close()
    return redirect(url_for("index"))

@app.route("/analytics")
def analytics():
    con=db(); students=con.execute("SELECT * FROM students").fetchall(); con.close()
    labels=[s["name"] for s in students]
    marks=[s["marks"] for s in students]
    attendance=[s["attendance"] for s in students]
    return render_template("analytics.html",labels=labels,marks=marks,attendance=attendance)

if __name__=="__main__":
    init_db()
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
