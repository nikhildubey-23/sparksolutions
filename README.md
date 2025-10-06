# Spark Solution Website

## Overview
This is a modern, responsive website for Spark Solution, a freelancing company. It includes a Flask backend, MongoDB Atlas integration, Gmail SMTP email notifications, and a Gemini API-powered chatbot.

## Features
- Home, Services, Portfolio, Contact, and Admin pages
- Light and Dark theme toggle
- Contact form saving data to MongoDB and sending email notifications
- Floating chatbot widget integrated with Gemini API and MongoDB logging
- Secure admin panel to view and export contact and chat data
- Responsive design with Bootstrap
- SEO-friendly and accessible

## Setup Instructions

1. Clone the repository.

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following variables:
   ```
   FLASK_SECRET_KEY=your_secret_key_here
   EMAIL_USER=your_gmail_here
   EMAIL_APP_PASSWORD=your_app_password_here
   MONGODB_URI=your_mongodb_atlas_uri_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=hashed_password_here  # Use bcrypt to hash your password
   ```

5. Run the Flask app:
   ```bash
   flask run
   ```

6. Open your browser at `http://localhost:5000`

## Notes
- Ensure MongoDB Atlas cluster is set up and accessible.
- Generate a Google App Password for Gmail SMTP.
- Obtain Gemini API key from Google Generative AI.
- Admin panel is protected; use credentials from `.env`.

## License
MIT License
