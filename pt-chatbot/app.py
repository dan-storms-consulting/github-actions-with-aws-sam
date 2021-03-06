import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    # logger.debug(event)
    # logger.debug(event["sessionState"]["intent"])
    # logger.debug(event["sessionState"]["intent"]["slots"])

    intent_name = event["sessionState"]["intent"]["name"]

    if intent_name == "GetContactInfoIntent":
        response_parameters = parse_get_contact_info_intent(event, intent_name)

        message = response_parameters[0]
        fulfillment_state = response_parameters[1]

        return close(intent_name, fulfillment_state, message)

    else:
        raise Exception("Intent with name %s not supported" % intent_name)


# retrieves contact info from the GetContactInfoIntent Lex intent and returns
def parse_get_contact_info_intent(event, intent_name):  # rename function
    slots = event["sessionState"]["intent"]["slots"]

    try:  # TODO need to figure out how None is based from Lex
        # Required fields

        # dict format {'first_name_slot': {'originalValue': 'dan', 'interpretedValue': 'dan', 'resolvedValues': []},

        try:
            first_name_interpreted = (
                slots.get("FirstNameSlot").get("value").get("interpretedValue")
            )
            last_name_interpreted = (
                slots.get("LastNameSlot").get("value").get("interpretedValue")
            )
            email_interpreted = (
                slots.get("EmailSlot").get("value").get("interpretedValue")
            )
            phone_interpreted = (
                slots.get("PhoneSlot").get("value").get("interpretedValue")
            )
        except:
            raise Exception("Required field not provided")

        # Optional fields
        try:
            # TODO might need if None
            insurance_company_interpreted = (
                slots.get("InsuranceCompanySlot").get("value").get("interpretedValue")
            )
            insurance_number_interpreted = (
                slots.get("InsuranceNumberSlot").get("value").get("interpretedValue")
            )
            date_of_birth_interpreted = (
                slots.get("DateOfBirthSlot").get("value").get("interpretedValue")
            )
        except:
            raise Exception(
                "is this really an exception?"
            )  # does lex just provide nulls by default?

        # dict to return
        contact_info = {
            "first_name_interpreted": first_name_interpreted,
            "last_name_interpreted": last_name_interpreted,
            "email_interpreted": email_interpreted,
            "phone_interpreted": phone_interpreted,
            "insurance_company_interpreted": insurance_company_interpreted,
            "insurance_number_interpreted": insurance_number_interpreted,
            "date_of_birth_interpreted": date_of_birth_interpreted,
        }

        logger.debug(contact_info)

        # TODO call notification function
        confirmation_number = send_email(contact_info)

        # f'Hello, {name}!'
        message = f"Thanks, I have let our staff know and they will reach out to you shortly. Your confirmation number is {confirmation_number}"  # TODO str format
        fulfillment_state = "Fulfilled"

        return message, fulfillment_state

    except Exception as e:

        # raise Exception("tbd")
        logger.debug("tbd")
        print(e)


def send_email(contact_info):

    # TODO SES stuff
    confirmation_number = "A12345"

    import boto3
    from botocore.exceptions import ClientError
    import os
    import string
    import random

    # Generate a confirmation code to pass to Lex and SES
    confirmation_number = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=5)
    )
    logger.debug(confirmation_number)

    sender_email = os.environ[
        "SENDER"
    ]  # This address must be verified with Amazon SES.
    recipient_email = os.environ[
        "RECIPIENT"
    ]  # If your account is still in the sandbox, this address must be verified.

    SENDER = sender_email  # "Sender Name <" + sender_email + ">"
    RECIPIENT = recipient_email

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"  # TODO could be useful for analytics https://docs.aws.amazon.com/ses/latest/dg/using-configuration-sets.html

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "PT-Chatbot Test"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (
        "PT-Chatbot Test\r\n"
        "PT chatbot here! A patient has a question or would like to schedule an appointment "
        + f"""First Name: {contact_info.get("first_name_interpreted")}\r\n
        Last Name: {contact_info.get("last_name_interpreted")}\r\n
        Email: {contact_info.get("email_interpreted")}\r\n
        Phone: {contact_info.get("phone_interpreted")}\r\n
        Insurance Company: {contact_info.get("insurance_company_interpreted")}\r\n
        Insurance Number: {contact_info.get("insurance_number_interpreted")}\r\n
        Date of Birth: {contact_info.get("date_of_birth_interpreted")}\r\n
        Confirmation Number: {confirmation_number}"""
    )

    # "first_name_interpreted": first_name_interpreted,
    # "last_name_interpreted": last_name_interpreted,
    # "email_interpreted": email_interpreted,
    # "phone_interpreted": phone_interpreted,
    # "insurance_company_interpreted": insurance_company_interpreted,
    # "insurance_number_interpreted": insurance_number_interpreted,
    # "date_of_birth_interpreted": date_of_birth_interpreted,

    # The HTML body of the email.
    BODY_HTML = f"""<html>
    <head></head>
    <body>
    <h1>PT-Chatbot Test</h1>
    <p>
    <br>PT chatbot here! A patient has a question or would like to schedule an appointment. <br>
    <br>First Name: {contact_info.get("first_name_interpreted")}
    <br>Last Name: {contact_info.get("last_name_interpreted")}
    <br>Email: {contact_info.get("email_interpreted")}
    <br>Phone: {contact_info.get("phone_interpreted")}
    <br>Insurance Company: {contact_info.get("insurance_company_interpreted")}
    <br>Insurance Number: {contact_info.get("insurance_number_interpreted")}
    <br>Date of Birth: {contact_info.get("date_of_birth_interpreted")}
    <br>Confirmation Number: {confirmation_number}
    </p>
    </body>
    </html>
                """

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client("ses", region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                "ToAddresses": [
                    RECIPIENT,
                ],
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": CHARSET,
                        "Data": BODY_HTML,
                    },
                    "Text": {
                        "Charset": CHARSET,
                        "Data": BODY_TEXT,
                    },
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        print("Email sent! Message ID:"),
        print(response["MessageId"])
        logger.debug(response["MessageId"])

        return confirmation_number


def close(intent_name, fulfillment_state, message):
    response = {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": {
                "confirmationState": "Confirmed",
                "name": intent_name,
                "state": "Fulfilled",
            },
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message,
            }
        ],
    }
    return response
