import azure.functions as func
from helpers import validate_email

app = func.FunctionApp()


@app.function_name(name="ContactFormHttpTrigger")
@app.route(route="send-email")  # HTTP Trigger
def send_email(req: func.HttpRequest) -> func.HttpResponse:
    # Check email is not null
    name = req.params.get('name')
    email = validate_email(req.params.get('email'))
    body = req.params.get('body')

    # Fail and do nothing if a bad email
    if email is None:
        return func.HttpResponse(
            f"Email '{req.params.get('email')}' is invalid", status_code=400)

    return func.HttpResponse(response.body,
                             status_code=response.status_code,
                             headers=response.headers)
