import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    logger.debug(event)
    logger.debug(event["sessionState"]["intent"])
    logger.debug(event["sessionState"]["intent"]["slots"])

    intent_name = event["sessionState"]["intent"]["name"]

    if intent_name == "get-info":
        return notification_email(event, intent_name)
    # elif (add more intents here for multi-intent bots)
    else:
        raise Exception("Intent with name %s not supported" % intent_name)


def notification_email(event, intent_name):
    slots = event["sessionState"]["intent"]["slots"]

    try:
        lead_name = slots.get("patient-name")
        lead_phone = slots.get("phone")
        lead_email = slots.get("email")

        logger.debug(lead_name)
        logger.debug(lead_phone)
        logger.debug(lead_email)

        # TODO call notification function
        confirmation_number = email(lead_name, lead_phone, lead_email)

        message = (
            "Thanks, I have let our staff know and they will reach out to you shortly. Your confirmation number is "
            + str(confirmation_number)
        )
        fulfillment_state = "Fulfilled"

    except:
        raise Exception("Unsupported slot included %s", slot)
        logger.debug("Unsupported slot included %s", slot)

    return close(
        intent_name,
        fulfillment_state,
        message,
    )


def close(intent_name, fulfillment_state, message):
    response = {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": {
                "confirmationState": "Confirmed",
                "name": "get-info",
                "state": "Fulfilled",
            },
        }
    }
    return response


def email(lead_name, lead_phone, lead_email):
    confirmation_number = "A12345"

    return confirmation_number


# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
                # "location": ip.text.replace("\n", "")
            }
        ),
    }
