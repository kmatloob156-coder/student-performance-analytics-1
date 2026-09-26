from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "mca-student-performance-secret"

students = [
    {"name":"Aman","marks":82,"attendance":91},
    {"name":"Rahul","marks":74,"attendance":86},
    {"name":"Priya","marks":91,"attendance":95},
    {"name":"Neha","marks":68,"attendance":78},
    {"name":"Rohit","marks":59,"attendance":72},
    {"name":"Simran","marks":88,"attendance":93},
    {"name":"Vikas","marks":77,"attendance":84},
    {"name":"Anjali","marks":95,"attendance":97},
    {"name":"Karan","marks":63,"attendance":75},
    {"name":"Pooja","marks":81,"attendance":89},
    {"id": 1, "name": "Aman Sharma", "marks": 82, "attendance": 91},
    {"id": 2, "name": "Rahul Verma", "marks": 74, "attendance": 86},
    {"id": 3, "name": "Priya Singh", "marks": 91, "attendance": 95},
    {"id": 4, "name": "Neha Gupta", "marks": 68, "attendance": 78},
    {"id": 5, "name": "Rohit Kumar", "marks": 59, "attendance": 72},
    {"id": 6, "name": "Simran Kaur", "marks": 88, "attendance": 93},
    {"id": 7, "name": "Vikas Yadav", "marks": 77, "attendance": 84},
    {"id": 8, "name": "Anjali Mehta", "marks": 95, "attendance": 97},
    {"id": 9, "name": "Karan Joshi", "marks": 63, "attendance": 75},
    {"id": 10, "name": "Pooja Mishra", "marks": 81, "attendance": 89},
    {"id": 11, "name": "Amit Patel", "marks": 85, "attendance": 90},
    {"id": 12, "name": "Sneha Roy", "marks": 92, "attendance": 96},
    {"id": 13, "name": "Deepak Sen", "marks": 54, "attendance": 68},
    {"id": 14, "name": "Kavya Pandey", "marks": 89, "attendance": 92},
    {"id": 15, "name": "Manish Chaudhary", "marks": 71, "attendance": 81},
    {"id": 16, "name": "Riya Kapoor", "marks": 96, "attendance": 98},
    {"id": 17, "name": "Siddharth Malhotra", "marks": 66, "attendance": 76},
    {"id": 18, "name": "Tanya Saxena", "marks": 83, "attendance": 88},
    {"id": 19, "name": "Gaurav Bansal", "marks": 79, "attendance": 85},
    {"id": 20, "name": "Nisha Agarwal", "marks": 90, "attendance": 94},
    {"id": 21, "name": "Varun Reddy", "marks": 58, "attendance": 70},
    {"id": 22, "name": "Shweta Deshmukh", "marks": 87, "attendance": 91},
    {"id": 23, "name": "Arjun Nair", "marks": 73, "attendance": 82},
    {"id": 24, "name": "Megha Das", "marks": 80, "attendance": 87},
    {"id": 25, "name": "Harsh Vardhan", "marks": 65, "attendance": 74}
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
    avg_marks = sum(s["marks"] for s in students) / len(students)
    avg_att = sum(s["attendance"] for s in students) / len(students)
    passed = sum(s["marks"] >= 50 for s in students)
    pass_rate = passed / len(students) * 100
    return render_template(
        "index.html",
        students=students,
        total=len(students),
        avg_marks=avg_marks,
        avg_att=avg_att,
        passed=passed,
        pass_rate=pass_rate
    )

@app.route("/students")
def show_all():
    return render_template("students.html", students=students, grade=grade)

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

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        try:
            name = request.form["name"].strip()
            marks = float(request.form["marks"])
            attendance = float(request.form["attendance"])
            if not name or not (0 <= marks <= 100) or not (0 <= attendance <= 100):
                raise ValueError
            students.append({"name": name, "marks": marks, "attendance": attendance})
            flash("Student added successfully.")
            return redirect(url_for("show_all"))
        except (ValueError, KeyError):
            flash("Please enter valid values. Marks and attendance must be 0-100.")
    return render_template("add.html")
def add_student():
    try:
        name = request.form["name"].strip()
        marks = float(request.form["marks"])
        attendance = float(request.form["attendance"])

        if not name or not (0 <= marks <= 100) or not (0 <= attendance <= 100):
            return "Invalid input."

        students.append({
            "name": name,
            "marks": marks,
            "attendance": attendance
        })

        return redirect(url_for("show_students"))

    except ValueError:
        return "Please enter valid numbers."


# ⬇️ YAHAN SE EDIT CODE PASTE KARO

@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    if student_id < 0 or student_id >= len(students):
        return "Student not found", 404

    student = students[student_id]

    if request.method == "POST":
        try:
            name = request.form["name"].strip()
            marks = float(request.form["marks"])
            attendance = float(request.form["attendance"])

            if not name or not (0 <= marks <= 100) or not (0 <= attendance <= 100):
                return "Invalid input."

            student["name"] = name
            student["marks"] = marks
            student["attendance"] = attendance

            return redirect(url_for("show_students"))

        except ValueError:
            return "Please enter valid numbers."

    return render_template(
        "edit.html",
        student=student,
        student_id=student_id
    )


# ⬇️ ISKE TURANT BAAD DELETE CODE

@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    if student_id < 0 or student_id >= len(students):
        return "Student not found", 404

    students.pop(student_id)

    return redirect(url_for("show_students"))
@app.route("/analytics")
def analytics():
    return render_template(
        "analytics.html",
        labels=[s["name"] for s in students],
        marks=[s["marks"] for s in students],
        attendance=[s["attendance"] for s in students]
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(__import__("os").environ.get("PORT", 5000)))
