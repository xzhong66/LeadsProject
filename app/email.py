import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()


def send_email(recipient, subject, body):
    api_key = os.environ.get("SENDGRID_API_KEY")
    sender = "zxfrankgt@gmail.com"

    message = Mail(
        from_email=sender,
        to_emails=recipient,
        subject=subject,
        html_content=body,
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(f"Email sent to {recipient}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email to {recipient}: {str(e)}")

# def send_email(recipient, subject, body):
#     # Print the email details instead of sending the email for now
#     print(f"To: {recipient}")
#     print(f"Subject: {subject}")
#     print(f"Body: {body}")
#     print("------------------------")
#     return recipient
