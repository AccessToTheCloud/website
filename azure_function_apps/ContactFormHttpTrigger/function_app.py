import os
import azure.functions as func
from helpers import validate_email
from azure.communication.email import EmailClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.function_name(name="attc-website-email-trigger")
@app.route(route="send-email")  # HTTP Trigger
def main(req: func.HttpRequest) -> func.HttpResponse:
    # Check email is not null
    name = req.params.get('name')
    email = validate_email(req.params.get('email'))
    body = req.params.get('body')

    # Fail and do nothing if bad inputs
    if email is None:
        return func.HttpResponse("Please enter a valid email address",
                                 status_code=400)
    if name is None:
        return func.HttpResponse("Please enter your name.", status_code=400)
    if body is None:
        return func.HttpResponse("Please enter your message.", status_code=400)

    email_client = EmailClient.from_connection_string(
        os.environ['AZURE_EMAIL_CONNECTION_STRING'])
    message = {
        "content": {
            "subject":
            f"New Contact Form Submission | {name}",
            "plainText":
            f"""
Hi {name},

Thank you for your submission, we'll be in touch with you shortly.

All the best,

Tom
ATTC | Access To The Cloud
contact@accesstothecloud.com

----------------------

{body}

""",
        },
        "recipients": {
            "to": [
                {
                    "email": "contact@accesstothecloud.com",
                },
                {
                    "email": email
                },
            ]
        },
        "sender": "no-reply@accesstothecloud.com"
    }

    response = email_client.send(message)
    status = email_client.get_send_status(response.message_id)

    return func.HttpResponse(response.message_id, status_code=status)

    # return func.HttpResponse("success", status_code=200)
