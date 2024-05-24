from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(recipient, subject, body):
    api_key = "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"
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

# 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
