import os
import sys
import json
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
import firebase_admin
from firebase_admin import credentials, auth
from datetime import datetime as dt

# Load environment variables
load_dotenv()

# Initialize Firebase Admin SDK
try:
    cred = credentials.Certificate('firebase-service-account.json')
    firebase_admin.initialize_app(cred)
except Exception as e:
    print(f"Firebase initialization error: {e}")

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")
CORS(app)

# Email setup
EMAIL_USER = "sparksolutionfreelancing@gmail.com"
EMAIL_APP_PASSWORD = "xmng fmym qfuq oswj"

def send_email(subject, body, to_email):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
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
    try:
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
    except Exception as e:
        print(f"Enrollment error: {e}")
        flash("An error occurred during enrollment. Please try again.", "error")
        return redirect(url_for('form'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
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
    except Exception as e:
        print(f"Contact form error: {e}")
        flash("An error occurred. Please try again.", "error")
        return redirect(url_for('contact'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    # Client-side logout handled by Firebase JS
    return redirect(url_for('home'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if username == 'founder' and password == 'nickfounder@123':
                session['admin_logged_in'] = True
                return redirect(url_for('admin_panel'))
            else:
                flash('Invalid credentials', 'error')

        return render_template('admin_login.html')
    except Exception as e:
        print(f"Admin login error: {e}")
        flash('An error occurred during login', 'error')
        return render_template('admin_login.html')

@app.route('/admin')
def admin_panel():
    try:
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))

        # Get all users from Firebase Auth
        users = []
        page = auth.list_users()
        while page:
            for user in page.users:
                # Format timestamps
                creation_time = dt.fromtimestamp(user.user_metadata.creation_timestamp / 1000) if user.user_metadata.creation_timestamp else None
                last_sign_in_time = dt.fromtimestamp(user.user_metadata.last_sign_in_timestamp / 1000) if user.user_metadata.last_sign_in_timestamp else None

                users.append({
                    'uid': user.uid,
                    'email': user.email,
                    'display_name': user.display_name,
                    'phone_number': user.phone_number,
                    'email_verified': user.email_verified,
                    'disabled': user.disabled,
                    'creation_timestamp': creation_time.strftime('%Y-%m-%d %H:%M:%S') if creation_time else 'N/A',
                    'last_sign_in_timestamp': last_sign_in_time.strftime('%Y-%m-%d %H:%M:%S') if last_sign_in_time else 'N/A',
                    'provider_data': [{'provider_id': provider.provider_id, 'email': provider.email} for provider in user.provider_data]
                })
            page = page.get_next_page()

        return render_template('admin_panel.html', users=users)
    except Exception as e:
        print(f"Admin panel error: {e}")
        flash(f'Error fetching users: {str(e)}', 'error')
        return render_template('admin_panel.html', users=[])

@app.route('/admin/logout')
def admin_logout():
    try:
        session.pop('admin_logged_in', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(f"Admin logout error: {e}")
        return redirect(url_for('home'))

# Vercel serverless function handler
def handler(event, context):
    try:
        # Handle the request for Vercel
        from werkzeug.test import Client
        from werkzeug.wrappers import Response

        # Extract request details
        method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        query_string = event.get('queryStringParameters', {})
        headers = event.get('headers', {})
        body = event.get('body', '')

        # Convert query string to URL format
        query_str = '&'.join([f"{k}={v}" for k, v in query_string.items()]) if query_string else ''

        # Create test client
        client = Client(app)

        # Make request
        response = client.open(path, method=method, query_string=query_str, headers=headers, data=body)

        # Return Vercel response format
        return {
            'statusCode': response.status_code,
            'headers': {k: v for k, v in response.headers},
            'body': response.get_data(as_text=True)
        }
    except Exception as e:
        print(f"Vercel handler error: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Internal Server Error', 'details': str(e)})
        }

if __name__ == '__main__':
    app.run(debug=True)
