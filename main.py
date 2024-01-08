import os
from dotenv import load_dotenv
from email_services import EmailServices
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

load_dotenv()

def main():
    email_service = EmailServices()

    # Data for the report
    assets = [
        {"account": "Savings Account", "amount": 237000.82, "change": 5554.25},
        {"account": "Checking Account", "amount": 34216.37, "change": 2164.84},
    ]

    liabilities = [
        {"account": "Credit Card", "amount": -1263.24, "change": -62.14},
    ]

    transactions = [
        {"account": "Checking Account", "amount": -54.12, "description": "Grocery Store", "date": "1/6"},
        {"account": "Savings Account", "amount": -102.07, "description": "Online Transfer", "date": "1/5"},
        {"account": "Credit Card", "amount": -62.14, "description": "Restaurant", "date": "1/4"}
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

    # Current UTC time
    utc_now = datetime.now(timezone.utc)

    # Convert UTC to EST using zoneinfo
    est_time = utc_now.astimezone(ZoneInfo("America/New_York"))

    current_date = est_time.strftime('%b %d')
    email_subject = f"[{current_date}] Daily Briefing  - {est_time.strftime('%-I:%M %p')}"

    response = email_service.send_email(recipient_email, email_subject, html_report)

    print(response)

if __name__ == "__main__":
    main()
