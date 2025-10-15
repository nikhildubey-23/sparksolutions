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

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")
CORS(app)

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