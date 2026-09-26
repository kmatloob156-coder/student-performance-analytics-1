from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "mca-student-performance-secret"

# Students list with unique 'id'
students = [
    {"id": 1, "name": "Aman", "marks": 82, "attendance": 91},
    {"id": 2, "name": "Rahul", "marks": 74, "attendance": 86},
    {"id": 3, "name": "Priya", "marks": 91, "attendance": 95},
    {"id": 4, "name": "Neha", "marks": 68, "attendance": 78},
    {"id": 5, "name": "Rohit", "marks": 59, "attendance": 72},
    {"id": 6, "name": "Simran", "marks": 88, "attendance": 93},
    {"id": 7, "name": "Vikas", "marks": 77, "attendance": 84},
    {"id": 8, "name": "Anjali", "marks": 95, "attendance": 97},
    {"id": 9, "name": "Karan", "marks": 63, "attendance": 75},
    {"id": 10, "name": "Pooja", "marks": 81, "attendance": 89},
]

def grade(marks):
    if marks >= 90: return "A+"
    if marks >= 80: return "A"
    if marks >= 70: return "B"
    if marks >= 60: return "C"
    if marks >= 50: return "D"
    return "F"

@app.route("/")
def dashboard():
    if not students:
        return render_template("index.html", students=[], total=0, avg_marks=0, avg_att=0, passed=0, pass_rate=0)
    avg_marks = sum(s["marks"] for s in students) / len(students)
    avg_att = sum(s["attendance"] for s in students) / len(students)
    passed = sum(s["marks"] >= 50 for s in students)
    pass_rate = (passed / len(students)) * 100
    return render_template("index.html", students=students, total=len(students), avg_marks=avg_marks, avg_att=avg_att, passed=passed, pass_rate=pass_rate)

@app.route("/students")
def show_all():
    return render_template("students.html", students=students, grade=grade)

# 1. ADD STUDENT ROUTE
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name")
        marks = int(request.form.get("marks", 0))
        attendance = int(request.form.get("attendance", 0))
        
        new_id = max([s["id"] for s in students], default=0) + 1
        students.append({"id": new_id, "name": name, "marks": marks, "attendance": attendance})
        flash("Student added successfully!", "success")
        return redirect(url_for("show_all"))
    return render_template("add.html")

# 2. EDIT STUDENT ROUTE
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    student = next((s for s in students if s["id"] == id), None)
    if not student:
        flash("Student not found!", "danger")
        return redirect(url_for("show_all"))

    if request.method == "POST":
        student["name"] = request.form.get("name")
        student["marks"] = int(request.form.get("marks", 0))
        student["attendance"] = int(request.form.get("attendance", 0))
        flash("Student updated successfully!", "success")
        return redirect(url_for("show_all"))

    return render_template("edit.html", student=student)

# 3. DELETE STUDENT ROUTE
@app.route("/delete/<int:id>")
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    flash("Student deleted successfully!", "danger")
    return redirect(url_for("show_all"))

@app.route("/top")
def top_students():
    top = sorted(students, key=lambda x: x["marks"], reverse=True)[:5]
    return render_template("top.html", students=top, grade=grade)

@app.route("/search")
def search_student():
    query = request.args.get("name", "").strip().lower()
    found = [s for s in students if query and query in s["name"].lower()]
    return render_template("search.html", students=found, query=query, grade=grade)

@app.route("/low-attendance")
def low_attendance():
    found = [s for s in students if s["attendance"] < 75]
    return render_template("low_attendance.html", students=found)

if __name__ == "__main__":
    app.run(debug=True)
    
