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
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

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

@app.route('/previous-work')
def previous_work():
    return render_template('previous_work.html')

@app.route('/practice')
def practice():
    return render_template('practice.html')

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
