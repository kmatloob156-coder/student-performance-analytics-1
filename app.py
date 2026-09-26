import os
import sys
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.secret_key = "secret_key_student_analytics"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'student.db')

def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = db()
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL, 
        roll TEXT UNIQUE NOT NULL, 
        course TEXT DEFAULT 'MCA', 
        semester TEXT, 
        marks REAL DEFAULT 0, 
        attendance REAL DEFAULT 0, 
        skills TEXT DEFAULT '', 
        placement_status TEXT DEFAULT 'Preparing'
    )""")
    
    cur.execute("SELECT COUNT(*) FROM students")
    count = cur.fetchone()[0]
    
    # Auto-insert 30 sample students if database is empty
    if count == 0:
        sample_students = [
            ('Aarav Sharma', 'MCA202401', 'MCA', 'Sem 3', 85.5, 92.0, 'Python, SQL', 'Placed'),
            ('Aditi Verma', 'MCA202402', 'MCA', 'Sem 3', 78.0, 88.5, 'Java, HTML', 'Preparing'),
            ('Amit Kumar', 'MCA202403', 'MCA', 'Sem 3', 62.5, 75.0, 'C++, Data Structures', 'Preparing'),
            ('Ananya Roy', 'MCA202404', 'MCA', 'Sem 3', 91.0, 96.0, 'Python, ML, SQL', 'Placed'),
            ('Aniket Singh', 'MCA202405', 'MCA', 'Sem 3', 55.0, 68.0, 'HTML, CSS', 'Preparing'),
            ('Bhavya Gupta', 'MCA202406', 'MCA', 'Sem 3', 82.0, 89.0, 'JavaScript, React', 'Placed'),
            ('Deepak Patel', 'MCA202407', 'MCA', 'Sem 3', 70.5, 81.0, 'Python, Django', 'Preparing'),
            ('Divya Joshi', 'MCA202408', 'MCA', 'Sem 3', 88.0, 94.0, 'Java, Spring Boot', 'Placed'),
            ('Gaurav Mehta', 'MCA202409', 'MCA', 'Sem 3', 64.0, 72.0, 'SQL, PHP', 'Preparing'),
            ('Harsh Vardhan', 'MCA202410', 'MCA', 'Sem 3', 79.5, 85.0, 'Python, Flask', 'Preparing'),
            ('Isha Kapoor', 'MCA202411', 'MCA', 'Sem 3', 93.0, 97.5, 'Python, AI, Data Science', 'Placed'),
            ('Jatin Mishra', 'MCA202412', 'MCA', 'Sem 3', 58.0, 70.0, 'C, C++', 'Preparing'),
            ('Kavya Saxena', 'MCA202413', 'MCA', 'Sem 3', 84.0, 90.0, 'Node.js, MongoDB', 'Placed'),
            ('Manish Pandey', 'MCA202414', 'MCA', 'Sem 3', 67.5, 78.0, 'Java, SQL', 'Preparing'),
            ('Neha Sharma', 'MCA202415', 'MCA', 'Sem 3', 89.5, 95.0, 'Python, SQL, Tableau', 'Placed'),
            ('Nikhil Chaudhari', 'MCA202416', 'MCA', 'Sem 3', 73.0, 83.0, 'HTML, CSS, JS', 'Preparing'),
            ('Pooja Nair', 'MCA202417', 'MCA', 'Sem 3', 81.0, 88.0, 'Java, MySQL', 'Placed'),
            ('Prateek Yadav', 'MCA202418', 'MCA', 'Sem 3', 60.0, 65.0, 'Python', 'Preparing'),
            ('Rahul Das', 'MCA202419', 'MCA', 'Sem 3', 76.5, 84.0, 'C++, Algorithms', 'Preparing'),
            ('Riya Sen', 'MCA202420', 'MCA', 'Sem 3', 90.0, 93.0, 'Python, Machine Learning', 'Placed'),
            ('Rohan Malhotra', 'MCA202421', 'MCA', 'Sem 3', 69.0, 79.0, 'PHP, MySQL', 'Preparing'),
            ('Sakshi Agarwal', 'MCA202422', 'MCA', 'Sem 3', 86.0, 91.0, 'React, Node.js', 'Placed'),
            ('Sanjay Kumar', 'MCA202423', 'MCA', 'Sem 3', 52.0, 62.0, 'HTML, Bootstrap', 'Preparing'),
            ('Shreya Rastogi', 'MCA202424', 'MCA', 'Sem 3', 87.5, 94.0, 'Python, SQL, AWS', 'Placed'),
            ('Siddharth Rao', 'MCA202425', 'MCA', 'Sem 3', 74.0, 80.0, 'Java, Android', 'Preparing'),
            ('Sneha Kulkarni', 'MCA202426', 'MCA', 'Sem 3', 83.0, 89.0, 'Python, Django, React', 'Placed'),
            ('Tushar Bansal', 'MCA202427', 'MCA', 'Sem 3', 66.0, 76.0, 'SQL, PowerBI', 'Preparing'),
            ('Varun Bhatia', 'MCA202428', 'MCA', 'Sem 3', 79.0, 87.0, 'C++, Java', 'Preparing'),
            ('Vikram Singhania', 'MCA202429', 'MCA', 'Sem 3', 94.5, 98.0, 'Python, Deep Learning', 'Placed'),
            ('Yashvi Shah', 'MCA202430', 'MCA', 'Sem 3', 80.5, 86.0, 'JavaScript, Express', 'Placed')
        ]
        cur.executemany("""
            INSERT INTO students (name, roll, course, semester, marks, attendance, skills, placement_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_students)
        
    con.commit()
    con.close()

with app.app_context():
    init_db()

@app.route('/')
def index():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    
    total_students = len(students)
    avg_marks = round(sum(s['marks'] for s in students) / total_students, 1) if total_students > 0 else 0
    avg_attendance = round(sum(s['attendance'] for s in students) / total_students, 1) if total_students > 0 else 0
    placed_count = sum(1 for s in students if s['placement_status'] == 'Placed')
    
    con.close()
    return render_template('index.html', students=students, total_students=total_students, avg_marks=avg_marks, avg_attendance=avg_attendance, placed_count=placed_count)

@app.route('/analytics')
def analytics():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    
    total_students = len(students)
    avg_marks = round(sum(s['marks'] for s in students) / total_students, 1) if total_students > 0 else 0
    avg_attendance = round(sum(s['attendance'] for s in students) / total_students, 1) if total_students > 0 else 0
    placed_count = sum(1 for s in students if s['placement_status'] == 'Placed')
    
    con.close()
    return render_template('analytics.html', total_students=total_students, avg_marks=avg_marks, avg_attendance=avg_attendance, placed_count=placed_count)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        course = request.form.get('course', 'MCA')
        semester = request.form.get('semester', '')
        marks = float(request.form.get('marks', 0))
        attendance = float(request.form.get('attendance', 0))
        skills = request.form.get('skills', '')
        placement_status = request.form.get('placement_status', 'Preparing')

        con = db()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO students (name, roll, course, semester, marks, attendance, skills, placement_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, roll, course, semester, marks, attendance, skills, placement_status))
        con.commit()
        con.close()
        flash("Student added successfully!")
        return redirect(url_for('index'))
    return render_template('form.html', action='Add', student=None)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    con = db()
    cur = con.cursor()
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        course = request.form.get('course', 'MCA')
        semester = request.form.get('semester', '')
        marks = float(request.form.get('marks', 0))
        attendance = float(request.form.get('attendance', 0))
        skills = request.form.get('skills', '')
        placement_status = request.form.get('placement_status', 'Preparing')

        cur.execute("""
            UPDATE students 
            SET name=?, roll=?, course=?, semester=?, marks=?, attendance=?, skills=?, placement_status=?
            WHERE id=?
        """, (name, roll, course, semester, marks, attendance, skills, placement_status, id))
        con.commit()
        con.close()
        flash("Student record updated successfully!")
        return redirect(url_for('index'))
    
    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    con.close()
    return render_template('form.html', action='Edit', student=student)

@app.route('/delete/<int:id>')
def delete(id):
    con = db()
    cur = con.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (id,))
    con.commit()
    con.close()
    flash("Student record deleted successfully!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
