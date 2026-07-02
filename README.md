# 📧 Bulk Email with Specific Detail from Excel

Bulk Email with Specific Detail from Excel is a Python-based automation tool that sends personalized emails to multiple recipients using data stored in an Excel spreadsheet. Instead of sending the same message to everyone, the application automatically replaces placeholders (such as **Name, Company, Invoice Number, Employee ID,** or any custom field) with the corresponding values from each row, ensuring every recipient receives a customized email.

## ✨ Features

- Send personalized bulk emails
- Read recipient details from Excel (`.xlsx`)
- Dynamic placeholders for custom data
- HTML and plain text email support
- Attachment support
- SMTP authentication
- Error handling and email logging

## 🛠 Technologies Used

- Python
- pandas
- openpyxl
- smtplib
- python-dotenv

## 🚀 Getting Started

```bash
Run terminal
cd FOLDER
pip install -r requirements.txt
python main.py
```

## 📊 Sample Excel Format

| Name | Email | Company | Invoice |
|------|-------|---------|---------|
| John Doe | john@example.com | ABC Ltd | INV-001 |

## 🎯 Use Cases

- HR notifications
- Invoice distribution
- Customer communication
- Event invitations
- Educational announcements
- Employee updates

## 📄 License

This project is licensed under the MIT License.

⭐ If you found this project useful, consider giving it a star on GitHub!
