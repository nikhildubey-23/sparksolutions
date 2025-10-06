import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import bcrypt
import io
import csv
import datetime
import threading
import time
import re

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")
CORS(app)

# MongoDB setup
mongo_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongo_uri)
db = client.spark_solution
contacts_collection = db.contacts
chatlogs_collection = db.chatlogs

# Email setup
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

# Admin credentials
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD")  # bcrypt hashed password

# Rate limiting for chatbot
chatbot_rate_limit = {}
RATE_LIMIT_WINDOW = 60  # seconds
MAX_REQUESTS_PER_WINDOW = 5

def is_rate_limited(ip):
    now = time.time()
    if ip not in chatbot_rate_limit:
        chatbot_rate_limit[ip] = []
    # Remove timestamps older than window
    chatbot_rate_limit[ip] = [t for t in chatbot_rate_limit[ip] if now - t < RATE_LIMIT_WINDOW]
    if len(chatbot_rate_limit[ip]) >= MAX_REQUESTS_PER_WINDOW:
        return True
    chatbot_rate_limit[ip].append(now)
    return False

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

@app.context_processor
def inject_theme():
    return dict()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()
        service_interest = data.get('service_interest', '').strip()

        # Server-side validation
        errors = []
        if not name:
            errors.append("Name is required.")
        if not email or not validate_email(email):
            errors.append("Valid email is required.")
        if phone and not validate_phone(phone):
            errors.append("Invalid phone number.")
        if not subject:
            errors.append("Subject is required.")
        if not message:
            errors.append("Message is required.")
        if not service_interest:
            errors.append("Please select a service interest.")

        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('contact'))

        # Save to MongoDB
        contact_doc = {
            "name": name,
            "email": email,
            "phone": phone,
            "subject": subject,
            "message": message,
            "service_interest": service_interest,
            "timestamp": datetime.datetime.utcnow()
        }
        contacts_collection.insert_one(contact_doc)

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

    return render_template('contact.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    ip = request.remote_addr
    if is_rate_limited(ip):
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429

    user_message = request.json.get('message', '').strip()
    if not user_message:
        return jsonify({"error": "Message is required."}), 400

    # Here, integrate with Gemini API (google-generativeai)
    # For demonstration, echo back the message
    # TODO: Replace with actual Gemini API call
    bot_response = f"Echo: {user_message}"

    # Save chat log
    chatlogs_collection.insert_one({
        "ip": ip,
        "user_message": user_message,
        "bot_response": bot_response,
        "timestamp": datetime.datetime.utcnow()
    })

    return jsonify({"response": bot_response})

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if username == ADMIN_USERNAME and bcrypt.checkpw(password.encode('utf-8'), ADMIN_PASSWORD_HASH.encode('utf-8')):
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/logout')
@admin_required
def admin_logout():
    session.pop('admin_logged_in', None)
    flash("Logged out successfully", "success")
    return redirect(url_for('admin_login'))

@app.route('/admin')
@admin_required
def admin_panel():
    contacts = list(contacts_collection.find().sort("timestamp", -1))
    chats = list(chatlogs_collection.find().sort("timestamp", -1))
    return render_template('admin.html', contacts=contacts, chats=chats)

@app.route('/admin/export/<string:data_type>')
@admin_required
def admin_export(data_type):
    if data_type == 'contacts':
        data = list(contacts_collection.find())
        filename = "contacts.csv"
        fields = ["name", "email", "phone", "subject", "service_interest", "message", "timestamp"]
    elif data_type == 'chats':
        data = list(chatlogs_collection.find())
        filename = "chatlogs.csv"
        fields = ["ip", "user_message", "bot_response", "timestamp"]
    else:
        flash("Invalid export type", "danger")
        return redirect(url_for('admin_panel'))

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(fields)
    for item in data:
        row = [item.get(field, "") for field in fields]
        cw.writerow(row)

    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)

    return send_file(output, mimetype='text/csv', as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True)
