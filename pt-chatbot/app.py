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

    except:
        raise Exception("tbd")
        logger.debug("tbd")


def send_email(contact_info):

    # TODO SES stuff
    confirmation_number = "A12345"

    # send contact_info

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
