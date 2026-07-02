## Copyright @ Ali Aziz GITHUB
#
from flask import Flask, render_template, request
import pandas as pd
import smtplib
import os
import traceback

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =====================================
# SMTP SETTINGS FOR OFFICE365 Accounts
# =====================================
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def send():

    sender_email = request.form["sender_email"].strip()
    sender_password = request.form["sender_password"]

    email_subject = request.form["email_subject"]
    email_body = request.form["email_body"]

    file = request.files["excel_file"]

    if file.filename == "":
        return "No Excel file selected."

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        df = pd.read_excel(filepath)

        # Normalize column names
        df.columns = df.columns.str.strip().str.lower()

        if "username" not in df.columns:
            return "Excel file must contain a 'username' column."

        if "password" not in df.columns:
            return "Excel file must contain a 'password' column."

        # Connect SMTP
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(sender_email, sender_password)

        success = 0
        failed = 0
        failed_users = []

        for _, row in df.iterrows():

            try:
                username = str(row["username"]).strip()
                password = str(row["password"]).strip()

                body = (
                    email_body
                    .replace("{username}", username)
                    .replace("{password}", password)
                )

                msg = MIMEMultipart()
                msg["From"] = sender_email
                msg["To"] = username
                msg["Subject"] = email_subject

                msg.attach(MIMEText(body, "plain"))

                server.send_message(msg)

                success += 1

            except Exception as e:
                failed += 1
                failed_users.append(
                    f"{username} - {str(e)}"
                )

        server.quit()

        failed_html = ""

        if failed_users:
            failed_html += "<h3>Failed Users</h3><ul>"

            for user in failed_users:
                failed_html += f"<li>{user}</li>"

            failed_html += "</ul>"

        return f"""
        <html>
        <head>
        <title>Email Result</title>

        <style>
        body {{
            font-family: Segoe UI;
            background:#f5f7fa;
            padding:40px;
        }}

        .card {{
            max-width:800px;
            margin:auto;
            background:white;
            padding:30px;
            border-radius:12px;
            box-shadow:0 5px 20px rgba(0,0,0,.1);
        }}

        .success {{
            color:green;
            font-size:22px;
        }}

        .failed {{
            color:red;
            font-size:22px;
        }}

        a {{
            display:inline-block;
            margin-top:20px;
            text-decoration:none;
            padding:10px 20px;
            background:#1f4e79;
            color:white;
            border-radius:6px;
        }}
        </style>

        </head>

        <body>

        <div class="card">

        <h2>Email Sending Completed</h2>

        <p class="success">
        Successfully Sent: {success}
        </p>

        <p class="failed">
        Failed: {failed}
        </p>

        {failed_html}

        <a href="/">Send More Emails</a>

        </div>

        </body>
        </html>
        """

    except Exception as e:
        return f"""
        <h2>Error</h2>
        <pre>{traceback.format_exc()}</pre>
        """


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
