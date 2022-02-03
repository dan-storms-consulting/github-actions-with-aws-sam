import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    logger.debug(event)
    logger.debug(event["sessionState"]["intent"])
    logger.debug(event["sessionState"]["intent"]["slots"])

    intent_name = event["sessionState"]["intent"]["name"]

    if intent_name == "GetContactInfoIntent":
        return parse_get_contact_info_intent(event, intent_name)
    # elif (add more intents here for multi-intent bots)
    else:
        raise Exception("Intent with name %s not supported" % intent_name)


# retrieves contact info from the GetContactInfoIntent Lex intent and returns
def parse_get_contact_info_intent(event, intent_name):  # rename function
    slots = event["sessionState"]["intent"]["slots"]

    try:  # TODO need to figure out how None is based from Lex
        # Required fields
        try:
            first_name_slot = slots.get("FirstNameSlot")
            last_name_slot = slots.get("LastNameSlot")
            email_slot = slots.get("EmailSlot")
            phone_slot = slots.get("PhoneSlot")
        except:
            raise Exception("Required field not provided")

        # Optional fields
        try:
            # TODO might need if None
            insurance_company_slot = slots.get("InsuranceCompanySlot")
            insurance_number_slot = slots.get("InsuranceNumberSlot")
            date_of_birth_slot = slots.get("DateOfBirthSlot")
        except:
            raise Exception(
                "is this really an exception?"
            )  # does lex just provide nulls by default?

        # dict to return
        contact_info = {
            "first_name_slot": first_name_slot,
            "last_name_slot": last_name_slot,
            "email_slot": email_slot,
            "phone_slot": phone_slot,
            "insurance_company_slot": insurance_company_slot,
            "insurance_number_slot": insurance_number_slot,
            "date_of_birth_slot": date_of_birth_slot,
        }

        logger.debug(contact_info)

        # TODO call notification function
        confirmation_number = send_email(contact_info)

        message = (
            "Thanks, I have let our staff know and they will reach out to you shortly. Your confirmation number is "
            + str(confirmation_number)
        )
        fulfillment_state = "Fulfilled"

    except:
        raise Exception("tbd")
        logger.debug("tbd")

    # return close(
    #     intent_name,
    #     fulfillment_state,
    #     message,
    # )


# def close(intent_name, fulfillment_state, message):
#     response = {
#         "sessionState": {
#             "dialogAction": {"type": "Close"},
#             "intent": {
#                 "confirmationState": "Confirmed",
#                 "name": "get-info",
#                 "state": "Fulfilled",
#             },
#         }
#     }
#     #return response
#     #return intent_name


def send_email(contact_info):

    # TODO SES stuff
    confirmation_number = "A12345"

    return confirmation_number

    # return {
    #     "statusCode": 200,
    #     "body": json.dumps(
    #         {
    #             "intent_name": event
    #             # "message": "hello world",
    #             # "location": ip.text.replace("\n", "")
    #         }
    #     ),
    # }
