Student Performance Analytics System — MCA College Project
A responsive Flask + SQLite academic dashboard with course filters, student-ID-based records, search, CRUD operations, top/bottom-five rankings, performance charts, and automatic low-attendance alert integration.
Features
Dashboard cards: total students, average marks, average attendance, pass rate, low-attendance count.
Course selection/filtering (MCA, BCA, B.Tech, M.Tech, B.Sc IT, B.Com, MBA, Other).
Unique Student ID is the primary key; search by ID, name, or email.
Add, edit, and delete student records. Data is saved in SQLite, not just in memory.
Top 5 and Bottom 5 students by marks, overall or per course.
Low attendance list for attendance below 75%.
Responsive mobile-friendly UI and Chart.js analytics.
Email notification via SMTP and WhatsApp notification via Twilio when a saved student's attendance is below 75%, if credentials and contact details are configured. Notification failures are logged and do not destroy the student record.
Run locally
Install Python 3.10+.
Open terminal in this project folder.
Run:
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
Visit http://127.0.0.1:5000.
The first run seeds demo records. The demo email addresses and phone numbers are placeholders; replace them with real, consented contact details before testing notifications.
Configure email alerts
Set environment variables before running (or add them in Render → service → Environment):
SMTP_HOST (e.g. smtp.gmail.com)
SMTP_PORT (usually 587)
SMTP_USER
SMTP_PASSWORD (for Gmail, use an App Password, not your account password)
SMTP_FROM (optional; defaults to SMTP_USER)
Configure WhatsApp alerts
Create/configure a Twilio account and enable the WhatsApp Sandbox or an approved WhatsApp sender.
Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_WHATSAPP_FROM (format whatsapp:+14155238886 for the sandbox).
Store recipient phone numbers in E.164 format, e.g. +919876543210. Sandbox recipients must opt in. Production messaging may require approved templates/consent and charges.
Alerts are evaluated when a student is added or edited. If attendance is below 75%, configured channels are attempted. If no channel is configured, the app still displays the low-attendance record and logs that configuration is missing; it cannot send real messages without provider credentials and valid recipient contacts.
Deploy on Render
Push the project folder to a GitHub repository.
Create a Render Web Service connected to that repo.
Build command: pip install -r requirements.txt
Start command: gunicorn app:app
Add SECRET_KEY and any SMTP/Twilio environment variables in Render.
Persistence note: Render's local filesystem may be ephemeral. For durable SQLite data, attach a Render persistent disk (mount path /var/data) and set DATABASE_PATH=/var/data/students.db. Without a persistent disk, data may reset during redeploy/restart.
Important project notes
This is an educational project, not a secure production student information system. Add authentication/role-based access and backups before storing real student records.
Student IDs are unique and are not changed through the edit form.
Notifications can be sent again on subsequent edits while attendance remains below 75%; use provider logs and consent-based contacts responsibly.
