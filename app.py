import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Optional
from flask_cors import CORS
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import bcrypt
import io
import csv
import datetime
import re
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///practice_results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

with app.app_context():
    db.create_all()

# Email setup
EMAIL_USER = "sparksolutionfreelancing@gmail.com"
EMAIL_APP_PASSWORD = "xmng fmym qfuq oswj"

def send_email(subject, body, to_email):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

def validate_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    return re.match(regex, email)

def validate_phone(phone):
    if phone == "":
        return True
    regex = r'^\+?[\d\s\-]{7,15}$'
    return re.match(regex, phone)

class PracticeResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Integer, nullable=False)

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    service_interest = SelectField('Service Interest', choices=[
        ('', 'Select a service'),
        ('software_development', 'Software Development'),
        ('video_editing', 'Video Editing'),
        ('logo_design', 'Logo Design'),
        ('content_writing', 'Content Writing'),
        ('teaching', 'Teaching')
    ], validators=[DataRequired()])

@app.context_processor
def inject_theme():
    return dict()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')

@app.route('/python')
def python():
    return render_template('python.html')

@app.route('/html')
def html_page():
    return render_template('html.html')

@app.route('/previous-work')
def previous_work():
    return render_template('previous_work.html')

@app.route('/practice')
def practice():
    return render_template('practice.html')

@app.route('/css')
def css():
    return render_template('css.html')

@app.route('/flask')
def flask():
    return render_template('flask.html')

@app.route('/nextjs')
def nextjs():
    return render_template('nextjs.html')

@app.route('/react')
def react():
    return render_template('react.html')

@app.route('/js')
def js():
    return render_template('js.html')

@app.route('/django')
def django():
    return render_template('django.html')


@app.route('/node')
def node():
    return render_template('node.html')

@app.route('/dap')
def dap():
    return render_template('dap.html')

@app.route('/htmltest')
def htmltest():
    return render_template('htmltest.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/enroll', methods=['POST'])
def enroll():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    course = request.form.get('course')
    terms = request.form.get('terms')

    if not all([name, phone, email, course, terms]):
        flash("All fields are required!", "error")
        return redirect(url_for('form'))

    # Course details mapping
    courses = {
        'python-basics': {'name': 'Python Basics with OOPs', 'price': '₹200', 'ref': 'PYB001'},
        'data-analysis': {'name': 'Data Analysis', 'price': '₹250', 'ref': 'DAP001'},
        'html-css-js-react': {'name': 'HTML, CSS, JS & React', 'price': '₹500', 'ref': 'HCR001'},
        'javascript-dsa': {'name': 'JavaScript with DSA', 'price': '₹350', 'ref': 'JSD001'},
        'nodejs': {'name': 'Node.js', 'price': '₹250', 'ref': 'NOD001'},
        'flask': {'name': 'Flask', 'price': '₹250', 'ref': 'FLA001'},
        'django': {'name': 'Django', 'price': '₹400', 'ref': 'DJG001'},
        'nextjs': {'name': 'Next.js', 'price': '₹500', 'ref': 'NXJ001'},
        'video-editing': {'name': 'Video Editing', 'price': '₹600', 'ref': 'VED001'},
    }

    course_info = courses.get(course, {'name': 'Unknown', 'price': 'N/A', 'ref': 'N/A'})

    # Send email notification
    email_body = f"""
    New course enrollment:

    Name: {name}
    Phone: {phone}
    Email: {email}
    Course: {course_info['name']}
    Course Reference: {course_info['ref']}
    Price: {course_info['price']}
    """
    send_email(f"New Course Enrollment: {course_info['name']}", email_body, EMAIL_USER)

    flash("Enrollment successful! We will contact you soon.", "success")
    return render_template('success.html')

@app.route('/submit-practice', methods=['POST'])
def submit_practice():
    name = request.form.get('name')
    mobile = request.form.get('mobile')
    email = request.form.get('email')

    if not all([name, mobile, email]):
        flash("All student details are required!", "error")
        return redirect(url_for('practice'))

    # Calculate score
    score = 0
    answers = {
        'q1': 'a', 'q2': 'a', 'q3': 'a', 'q4': 'b', 'q5': 'b', 'q6': 'a', 'q7': 'a', 'q8': 'b', 'q9': 'a', 'q10': 'b',
        'q11': 'b', 'q12': 'c', 'q13': 'c', 'q14': 'b', 'q15': 'd', 'q16': 'b', 'q17': 'b', 'q18': 'b', 'q19': 'b',
        'q20': 'a', 'q21': 'b', 'q22': 'b', 'q23': 'c', 'q24': 'd', 'q25': 'b'
    }

    for q, ans in answers.items():
        selected = request.form.get(q)
        if selected == ans:
            score += 1

    # Coding checks
    code1 = request.form.get('code1', '')
    code2 = request.form.get('code2', '')
    if 'def' in code1 and 'return' in code1:
        score += 2
    if 'for' in code2 or 'while' in code2:
        score += 2

    # Save to DB
    try:
        new_result = PracticeResult(name=name, mobile=mobile, email=email, marks=score)
        db.session.add(new_result)
        db.session.commit()
    except Exception as e:
        print(f"DB save failed: {e}")
        # Continue without saving for serverless environments

    flash(f"Test submitted! Your score: {score}/27", "success")
    return redirect(url_for('practice'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.args.get('logout'):
        session.pop('admin', None)
        return redirect(url_for('admin'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'nick' and password == 'nick@123':
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            flash("Invalid credentials!", "error")
            return redirect(url_for('admin'))

    if not session.get('admin'):
        return render_template('admin_login.html')

    # Load DB data
    try:
        results = PracticeResult.query.all()
        data = [{'id': r.id, 'Name': r.name, 'Mobile': r.mobile, 'Email': r.email, 'Marks': str(r.marks)} for r in results]
    except Exception as e:
        print(f"DB load failed: {e}")
        data = []

    # Sort by marks descending
    data.sort(key=lambda x: int(x['Marks']), reverse=True)

    # Filter by name if provided
    filter_name = request.args.get('filter_name', '').lower()
    if filter_name:
        data = [row for row in data if filter_name in row['Name'].lower()]

    return render_template('admin.html', data=data, filter_name=filter_name)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if not session.get('admin'):
        flash("Access denied!", "error")
        return redirect(url_for('admin'))

    # Delete from DB
    try:
        result = PracticeResult.query.get(id)
        if result:
            db.session.delete(result)
            db.session.commit()
            flash("Record deleted successfully!", "success")
        else:
            flash("Record not found!", "error")
    except Exception as e:
        print(f"DB delete failed: {e}")
        flash("Delete failed!", "error")

    return redirect(url_for('admin'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data
        service_interest = form.service_interest.data

        # Send email notification
        email_body = f"""
        New contact form submission:

        Name: {name}
        Email: {email}
        Phone: {phone}
        Subject: {subject}
        Service Interest: {service_interest}
        Message:
        {message}
        """
        send_email(f"New Contact Form Submission: {subject}", email_body, EMAIL_USER)

        flash("Your message has been sent successfully!", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)