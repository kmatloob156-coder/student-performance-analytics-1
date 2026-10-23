import os, sqlite3, smtplib, logging
from email.message import EmailMessage
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, abort

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.environ.get('DATABASE_PATH', os.path.join(BASE_DIR, 'students.db'))
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-secret-before-deployment')
logging.basicConfig(level=logging.INFO)

COURSES = ['MCA', 'BCA', 'B.Tech', 'M.Tech', 'B.Sc IT', 'B.Com', 'MBA', 'Other']


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    with connect_db() as db:
        db.execute("CREATE TABLE IF NOT EXISTS students (student_id TEXT PRIMARY KEY, name TEXT NOT NULL, course TEXT NOT NULL, email TEXT, phone TEXT, marks REAL NOT NULL CHECK(marks BETWEEN 0 AND 100), attendance REAL NOT NULL CHECK(attendance BETWEEN 0 AND 100), created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")
        count = db.execute('SELECT COUNT(*) FROM students').fetchone()[0]
        if count == 0:
            demo = [
                ('MCA001','Aman Sharma','MCA','aman@example.com','+919876500001',82,91),
                ('MCA002','Rahul Verma','MCA','rahul@example.com','+919876500002',74,86),
                ('MCA003','Priya Singh','MCA','priya@example.com','+919876500003',91,95),
                ('MCA004','Neha Gupta','MCA','neha@example.com','+919876500004',68,78),
                ('MCA005','Rohit Kumar','MCA','rohit@example.com','+919876500005',59,72),
                ('MCA006','Simran Kaur','MCA','simran@example.com','+919876500006',88,93),
                ('MCA007','Vikas Yadav','MCA','vikas@example.com','+919876500007',77,84),
                ('MCA008','Anjali Mehta','MCA','anjali@example.com','+919876500008',95,97),
                ('MCA009','Karan Joshi','MCA','karan@example.com','+919876500009',63,75),
                ('MCA010','Pooja Mishra','MCA','pooja@example.com','+919876500010',81,89),
                ('BCA001','Amit Patel','BCA','amit@example.com','+919876500011',85,70),
                ('BCA002','Sneha Roy','BCA','sneha@example.com','+919876500012',92,68),
                ('BTECH01','Deepak Sen','B.Tech','deepak@example.com','+919876500013',54,62),
                ('BTECH02','Kavya Pandey','B.Tech','kavya@example.com','+919876500014',89,92),
                ('MTECH01','Riya Kapoor','M.Tech','riya@example.com','+919876500015',96,98)]
            db.executemany('INSERT INTO students(student_id,name,course,email,phone,marks,attendance) VALUES(?,?,?,?,?,?,?)', demo)


def grade(marks):
    marks=float(marks)
    if marks >= 90: return 'A+'
    if marks >= 80: return 'A'
    if marks >= 70: return 'B'
    if marks >= 60: return 'C'
    if marks >= 50: return 'D'
    return 'F'


def notify_low_attendance(student):
    """Send configured email/WhatsApp alerts. Missing credentials safely skip that channel."""
    if float(student['attendance']) >= 75:
        return
    message = (f"Attendance Alert for {student['name']} (ID: {student['student_id']})\n"
               f"Course: {student['course']}\nCurrent attendance: {student['attendance']}%\n"
               "Required attendance: at least 75%. Please contact your faculty/department.")
    sent = []
    # Email via SMTP (Gmail app password or institutional SMTP credentials recommended).
    host=os.environ.get('SMTP_HOST'); port=os.environ.get('SMTP_PORT','587')
    user=os.environ.get('SMTP_USER'); password=os.environ.get('SMTP_PASSWORD')
    sender=os.environ.get('SMTP_FROM') or user
    if student['email'] and host and user and password and sender:
        try:
            msg=EmailMessage(); msg['Subject']='Low Attendance Alert'; msg['From']=sender; msg['To']=student['email']; msg.set_content(message)
            with smtplib.SMTP(host, int(port), timeout=15) as server:
                server.starttls(); server.login(user,password); server.send_message(msg)
            sent.append('email')
        except Exception as exc:
            app.logger.warning('Email notification failed for %s: %s', student['student_id'], exc)
    # WhatsApp via Twilio WhatsApp API. Both numbers must be E.164 / WhatsApp-enabled.
    sid=os.environ.get('TWILIO_ACCOUNT_SID'); token=os.environ.get('TWILIO_AUTH_TOKEN')
    wa_from=os.environ.get('TWILIO_WHATSAPP_FROM')
    if student['phone'] and sid and token and wa_from:
        try:
            from twilio.rest import Client
            Client(sid,token).messages.create(from_=wa_from, to='whatsapp:'+student['phone'], body=message)
            sent.append('WhatsApp')
        except Exception as exc:
            app.logger.warning('WhatsApp notification failed for %s: %s', student['student_id'], exc)
    if sent:
        app.logger.info('Low attendance notification sent via %s for %s', ', '.join(sent), student['student_id'])
    else:
        app.logger.info('Low attendance alert detected for %s; configure SMTP and/or Twilio to send it.', student['student_id'])


def get_student(student_id):
    with connect_db() as db:
        return db.execute('SELECT * FROM students WHERE student_id=?', (student_id,)).fetchone()


def read_form():
    student_id=request.form.get('student_id','').strip().upper()
    name=request.form.get('name','').strip()
    course=request.form.get('course','').strip()
    email=request.form.get('email','').strip()
    phone=request.form.get('phone','').strip()
    try:
        marks=float(request.form.get('marks',''))
        attendance=float(request.form.get('attendance',''))
    except ValueError:
        raise ValueError('Marks and attendance must be numbers.')
    if not student_id or not name or not course:
        raise ValueError('Student ID, name and course are required.')
    if len(student_id)>30: raise ValueError('Student ID must be 30 characters or fewer.')
    if course not in COURSES: raise ValueError('Please select a valid course.')
    if not 0 <= marks <= 100: raise ValueError('Marks must be between 0 and 100.')
    if not 0 <= attendance <= 100: raise ValueError('Attendance must be between 0 and 100.')
    if email and ('@' not in email or '.' not in email.rsplit('@',1)[-1]): raise ValueError('Enter a valid email address.')
    return {'student_id':student_id,'name':name,'course':course,'email':email,'phone':phone,'marks':marks,'attendance':attendance}

@app.route('/')
def dashboard():
    course=request.args.get('course','').strip()
    with connect_db() as db:
        where=' WHERE course=?' if course in COURSES else ''
        args=(course,) if where else ()
        rows=db.execute('SELECT * FROM students'+where+' ORDER BY name COLLATE NOCASE',args).fetchall()
    total=len(rows)
    avg_marks=round(sum(s['marks'] for s in rows)/total,2) if total else 0
    avg_att=round(sum(s['attendance'] for s in rows)/total,2) if total else 0
    passed=sum(s['marks']>=50 for s in rows)
    low=sum(s['attendance']<75 for s in rows)
    return render_template('index.html',students=rows,total=total,avg_marks=avg_marks,avg_att=avg_att,
        pass_rate=round(passed*100/total,2) if total else 0,low=low,courses=COURSES,selected_course=course)

@app.route('/students')
def show_all():
    query=request.args.get('q','').strip()
    course=request.args.get('course','').strip()
    sql='SELECT * FROM students WHERE 1=1'; args=[]
    if query:
        sql += ' AND (student_id LIKE ? OR name LIKE ? OR email LIKE ?)'; like=f'%{query}%'; args.extend([like,like,like])
    if course in COURSES: sql+=' AND course=?'; args.append(course)
    sql+=' ORDER BY course, student_id'
    with connect_db() as db: rows=db.execute(sql,args).fetchall()
    return render_template('students.html',students=rows,grade=grade,courses=COURSES,query=query,selected_course=course)

@app.route('/search')
def search_student():
    query=request.args.get('q',request.args.get('name','')).strip()
    return redirect(url_for('show_all',q=query))

@app.route('/top')
def top_students():
    course=request.args.get('course','').strip()
    with connect_db() as db:
        if course in COURSES: rows=db.execute('SELECT * FROM students WHERE course=? ORDER BY marks DESC, student_id LIMIT 5',(course,)).fetchall()
        else: rows=db.execute('SELECT * FROM students ORDER BY marks DESC, student_id LIMIT 5').fetchall()
    return render_template('ranking.html',students=rows,grade=grade,courses=COURSES,selected_course=course,heading='Top 5 Students',kind='top')

@app.route('/bottom')
def bottom_students():
    course=request.args.get('course','').strip()
    with connect_db() as db:
        if course in COURSES: rows=db.execute('SELECT * FROM students WHERE course=? ORDER BY marks ASC, student_id LIMIT 5',(course,)).fetchall()
        else: rows=db.execute('SELECT * FROM students ORDER BY marks ASC, student_id LIMIT 5').fetchall()
    return render_template('ranking.html',students=rows,grade=grade,courses=COURSES,selected_course=course,heading='Bottom 5 Students',kind='bottom')

@app.route('/low-attendance')
def low_attendance():
    course=request.args.get('course','').strip()
    sql='SELECT * FROM students WHERE attendance < 75'; args=[]
    if course in COURSES: sql+=' AND course=?'; args.append(course)
    sql+=' ORDER BY attendance ASC'
    with connect_db() as db: rows=db.execute(sql,args).fetchall()
    return render_template('low_attendance.html',students=rows,courses=COURSES,selected_course=course)

@app.route('/add',methods=['GET','POST'])
def add_student():
    if request.method=='POST':
        try:
            data=read_form()
            with connect_db() as db:
                db.execute('INSERT INTO students(student_id,name,course,email,phone,marks,attendance) VALUES(:student_id,:name,:course,:email,:phone,:marks,:attendance)',data)
            student=get_student(data['student_id'])
            notify_low_attendance(student)
            flash('Student added successfully. If attendance is below 75%, configured notification channels were checked.','success')
            return redirect(url_for('show_all'))
        except sqlite3.IntegrityError:
            flash('This Student ID already exists. Use a unique ID.','error')
        except ValueError as exc: flash(str(exc),'error')
    return render_template('student_form.html',student=None,courses=COURSES,mode='Add')

@app.route('/edit/<student_id>',methods=['GET','POST'])
def edit_student(student_id):
    student=get_student(student_id)
    if student is None: abort(404)
    if request.method=='POST':
        try:
            data=read_form()
            if data['student_id'] != student_id.upper():
                raise ValueError('Student ID cannot be changed during editing. Delete and re-add if the ID must change.')
            with connect_db() as db:
                db.execute("UPDATE students SET name=:name,course=:course,email=:email,phone=:phone,marks=:marks,attendance=:attendance,updated_at=CURRENT_TIMESTAMP WHERE student_id=:student_id",data)
            notify_low_attendance(get_student(student_id))
            flash('Student record updated successfully.','success')
            return redirect(url_for('show_all'))
        except sqlite3.IntegrityError: flash('Student ID already exists.','error')
        except ValueError as exc: flash(str(exc),'error')
        student={**dict(student),**request.form.to_dict()}
    return render_template('student_form.html',student=student,courses=COURSES,mode='Edit')

@app.route('/delete/<student_id>',methods=['POST'])
def delete_student(student_id):
    with connect_db() as db: cur=db.execute('DELETE FROM students WHERE student_id=?',(student_id,))
    if cur.rowcount: flash(f'Student {student_id} deleted.','success')
    else: flash('Student not found.','error')
    return redirect(url_for('show_all'))

@app.route('/analytics')
def analytics():
    course=request.args.get('course','').strip()
    sql='SELECT * FROM students'; args=()
    if course in COURSES: sql+=' WHERE course=?'; args=(course,)
    sql+=' ORDER BY name COLLATE NOCASE'
    with connect_db() as db: rows=db.execute(sql,args).fetchall()
    return render_template('analytics.html',students=rows,courses=COURSES,selected_course=course)

@app.errorhandler(404)
def not_found(_):
    return render_template('error.html',code=404,message='Student or page not found.'),404

init_db()
if __name__=='__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)),debug=os.environ.get('FLASK_DEBUG')=='1')
