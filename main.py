import os
from dotenv import load_dotenv
from email_services import EmailServices
from datetime import datetime

load_dotenv()

def main():
    email_service = EmailServices()

    # Data for the report
    assets = {
        "Savings Account": 237000.50,
        "Checking Account": 34216.75
    }

    liabilities = {
        "Credit Card": -1263.24
    }

    transactions = [
        {"account": "Checking Account", "amount": -54.12, "description": "Grocery Store", "date": "2024-01-06"},
        {"account": "Savings Account", "amount": -102.07, "description": "Online Transfer", "date": "2024-01-05"},
        {"account": "Credit Card", "amount": 62.14, "description": "Restaurant", "date": "2024-01-04"}
    ]

    # Paths to the HTML template and CSS files
    template_path = 'templates/briefing_email_template.html'
    css_path = 'templates/email_styles.css'

    # Generate HTML content with inlined CSS
    html_report = email_service.generate_html_content(template_path, css_path, assets, liabilities, transactions)

    # Send the email with the HTML report
    recipient_email = os.getenv('SEND_TO')

    if not recipient_email:
        print("Recipient email not set in environment variables.")
        return

    current_date = datetime.now().strftime('%b %d')
    email_subject = f"[{current_date}] Financial Report  - {datetime.now().strftime('%H:%M:%S')}"
    response = email_service.send_email(recipient_email, email_subject, html_report)

    print(response)

if __name__ == "__main__":
    main()
