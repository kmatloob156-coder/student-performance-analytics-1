Student Performance Analytics System - MCA Major Project

A phone-friendly web version of the original Python Student Performance Analytics program.


Backend logic

The Flask backend follows the original program:



grade() calculates A+, A, B, C, D and F.

Dashboard calculates total students, average marks, average attendance and pass rate.

Top 5 sorts students by marks.

Search finds students by name.

Low attendance finds students below 75%.

Add Student validates marks and attendance from 0-100.


Demo data

The project starts with the same 10 demo students from the original program:
Aman, Rahul, Priya, Neha, Rohit, Simran, Vikas, Anjali, Karan and Pooja.


Run

pip install -r requirements.txt
python app.py

Render

Build command:
pip install -r requirements.txt


Start command:
gunicorn app:app

