import os
from premailer import transform
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
from string import Template

load_dotenv()

class EmailServices:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))
        self.sender_email = os.getenv('EMAIL_ADDRESS')
        self.sender_password = os.getenv('EMAIL_PASSWORD')

    def inline_css(self, html_path, css_path):
        # Read the CSS file and store its contents as a string
        with open(css_path, 'r') as css_file:
            css_string = css_file.read()

        # Read the HTML file
        with open(html_path, 'r') as html_file:
            html_string = html_file.read()

        # Inline the CSS using the CSS string
        inlined_html = transform(html_string, css_text=css_string)

        return inlined_html
    
    def generate_html_content(self, template_path, css_path, assets, liabilities, transactions):
        # 100,000.00 or +100,000.00
        def format_number(value, sign=False):
            return "{:+,.2f}".format(value) if sign else "{:,.2f}".format(value)
        
        # Function to generate table rows for dictionary data
        def generate_asset_table_rows(data):
            return "\n".join(
                [f"<tr>
                    <td>{item['account']}</td>
                    <td>${format_number(item['amount'])} ({format_number(item['change'], True)})</td>
                    </tr>" for item in data
                ]
            )

        # Function to generate table rows for list of dictionary data
        def generate_transaction_table_rows(data):
            return "\n".join(
                [f"<tr>
                    <td>{item['date']}</td>
                    <td>{item['account']}</td>
                    <td>{item['description']}</td>
                    <td>${item['amount']}</td>
                    </tr>" for item in data
                ]
            )

        # Inline CSS into the HTML template
        html_template_str = self.inline_css(template_path, css_path)

        # Replace placeholders in the template with actual data using string.Template
        html_template = Template(html_template_str)
        html_content = html_template.substitute(
            assets=generate_asset_table_rows(assets),
            liabilities=generate_asset_table_rows(liabilities),
            transactions=generate_transaction_table_rows(transactions)
        )
        return html_content

    def send_email(self, recipient_email, subject, html_content, sender_name="Personal Assistant"):
        message = MIMEMultipart("alternative")
        message['From'] = f"{sender_name} <{self.sender_email}>"
        message['To'] = recipient_email
        message['Subject'] = subject

        # Attach HTML content
        part = MIMEText(html_content, 'html')
        message.attach(part)

        # Create SMTP session for sending the mail
        session = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        session.login(self.sender_email, self.sender_password)
        session.sendmail(self.sender_email, recipient_email, message.as_string())
        session.quit()

if __name__ == "__main__":
    email_service = EmailServices()

    # Paths to your HTML and CSS files
    html_path = 'path/to/email_template.html'
    css_path = 'path/to/email_styles.css'

    # Your data for assets, liabilities, and transactions
    assets = {...}
    liabilities = {...}
    transactions = [...]

    # Generate HTML content with inlined CSS
    html_content = email_service.generate_html_content(html_path, css_path, assets, liabilities, transactions)

    # Send the email
    recipient_email = "recipient@example.com"
    subject = "Daily Financial Report"
    email_service.send_email(recipient_email, subject, html_content)
