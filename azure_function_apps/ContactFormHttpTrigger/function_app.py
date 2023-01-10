import os
import smtplib
import email.message as e
import azure.functions as func
from helpers import validate_email
from azure.communication.email import (EmailClient, EmailContent,
                                       EmailRecipients, EmailAddress,
                                       EmailMessage)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

CC = 'contact@accesstothecloud.com'
SENDER = 'no-reply@accesstothecloud.com'


# Send email to local development SMTP server
def send_local_email(name, email, email_subject,
                     email_content) -> func.HttpResponse:
    message = e.EmailMessage()
    message['Subject'] = email_subject
    message['From'] = SENDER
    message['To'] = email
    message['Cc'] = CC
    message.set_content(email_content)
    try:
        smtpObj = smtplib.SMTP('localhost', 1025)
        smtpObj.send_message(message)
        return func.HttpResponse("Development Email success", status_code=200)
    except smtplib.SMTPException:
        return func.HttpResponse("Development Email failed", status_code=500)


@app.function_name(name="attc-website-email-trigger")
@app.route(route="send-email")  # HTTP Trigger
def main(req: func.HttpRequest) -> func.HttpResponse:
    # Check email is not null
    name = req.params.get('name')
    email = validate_email(req.params.get('email'))
    message = req.params.get('message')

    # Fail and do nothing if bad inputs
    if email is None:
        return func.HttpResponse("Please enter a valid email address",
                                 status_code=400)
    if name is None:
        return func.HttpResponse("Please enter your name.", status_code=400)
    if message is None:
        return func.HttpResponse("Please enter your message.", status_code=400)

    # Formatting for the email body
    email_subject = f"New Contact Form Submission | {name}"
    email_content = f"""
Hi {name},

Thank you for your submission, we'll be in touch with you shortly.

All the best,

Tom
ATTC | Access To The Cloud
contact@accesstothecloud.com

----------------------

{message}

"""

    if os.environ['AZURE_FUNCTION_ENV'] == 'development':
        return send_local_email(name, email, email_subject, email_content)

    email_client = EmailClient.from_connection_string(
        os.environ['AZURE_EMAIL_CONNECTION_STRING'])
    response = email_client.send(
        EmailMessage(sender=SENDER,
                     content=EmailContent(subject=email_subject,
                                          plain_text=email_content),
                     recipients=EmailRecipients(
                         to=[
                             EmailAddress(email=email),
                         ],
                         cc=[
                             EmailAddress(email=CC),
                         ],
                     )))

    status = email_client.get_send_status(response.message_id)
    return func.HttpResponse(response.message_id, status_code=status)
