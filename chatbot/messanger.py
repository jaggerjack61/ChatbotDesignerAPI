from django.http import JsonResponse, HttpResponseBadRequest
from dotenv import load_dotenv
import requests
import json
import os

from templates.models import TemplatePage, TemplateOption

load_dotenv()
BEARER = "EAAI6mp4cpyIBO6gnqiObSZBOZBT8a4lizlmt8Ng6FX0FTAjxkZBt4YfXpxsLp3D1l0QTno9ZAeIJhHfYdZCYoXo249ZBxTzE4U7pb5dSzk5IhLjD8750St5hntZCJJONXCxM3bbfEQOHyp7UYEI8rJWHSshLPN3bdVEtkdVzhUNarQN17S65xFajl2CJZB71lfUnajbNcxCY7gcXGv2pMw8ZD"
PHONE_ID = os.getenv("PHONE_ID")
TOKEN = os.getenv("VERIFICATION_TOKEN")


def verify_webhook(request):
    if (request.query_params.get('hub.mode') == 'subscribe' and
            request.query_params.get('hub.verify_token') == TOKEN):
        challenge = request.query_params.get('hub.challenge')
        return JsonResponse(int(challenge), safe=False)  # Return as JSON without escaping
    else:
        return HttpResponseBadRequest()


def extract_list_id_and_phone(payload):
    try:
        # Parse the payload to get the list ID and phone number
        list_id = payload['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['list_reply']['id']
        phone_number = payload['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
        return list_id, phone_number
    except (KeyError, IndexError, TypeError) as e:
        # Handle the error if the payload is not structured as expected
        print(f"Error parsing payload: {e}")
        return None, None


def extract_button_id_and_phone(payload):
    try:
        # Parse the payload to get the button ID and phone number
        button_id = payload['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['button_reply']['id']
        phone_number = payload['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
        return button_id, phone_number
    except (KeyError, IndexError, TypeError) as e:
        # Handle the error if the payload is not structured as expected
        print(f"Error parsing payload: {e}")
        return None, None


def extract_message_and_phone(payload):
    try:
        message = payload['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        phone_number = payload['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
        return message, phone_number
    except (KeyError, IndexError, TypeError):
        return None, None


def handle_payload(payload):
    try:
        # Check if the payload has 'interactive' key, indicating an interactive message
        if 'interactive' in payload['entry'][0]['changes'][0]['value']['messages'][0]:
            # Determine the type of interactive message
            interactive_type = payload['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['type']
            if interactive_type == 'button_reply':
                message, phone_number = extract_button_id_and_phone(payload)
                return "button", message, phone_number
            elif interactive_type == 'list_reply':
                message, phone_number = extract_list_id_and_phone(payload)
                return "list", message, phone_number
            else:
                print(f"Unknown interactive message type: {interactive_type}")
                return None, None, None
        # Check if the payload has 'text' key, indicating a text message
        elif 'text' in payload['entry'][0]['changes'][0]['value']['messages'][0]:
            message, phone_number = extract_message_and_phone(payload)
            return "text", message, phone_number
        else:
            print("Unknown message type in payload.")
            return None, None, None
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error parsing payload: {e}")
        return None, None, None


def send_text(text, phone_number):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {BEARER}'
    }
    body = {
        "messaging_product": "whatsapp",
        "preview_url": False,
        "recipient_type": "individual",
        "to": phone_number,
        "type": "text",
        "text": {
            "body": text
        }
    }

    response = requests.post(
        f'https://graph.facebook.com/v13.0/{PHONE_ID}/messages',
        headers=headers,
        json=body
    )
    print(response.text)


def send_button(text, buttons, phone_number):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {BEARER}'
    }

    button_json = [  # Create a list of button dictionaries
        {
            "type": "reply",
            "reply": {
                "id": button['value'],
                "title": button['text']
            }
        } for button in buttons
    ]

    body = {  # Construct the body as a dictionary
        "recipient_type": "individual",
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "header": {
                "type": "text",
                "text": text[0]
            },
            "body": {
                "text": text[1]
            },
            "footer": {
                "text": text[2]
            },
            "action": {
                "buttons": button_json
            }
        }
    }

    response = requests.post(  # Send the POST request
        f'https://graph.facebook.com/v14.0/{PHONE_ID}/messages',
        headers=headers,
        data=json.dumps(body)  # Convert the body to a JSON string
    )

    print(response.text)


def send_list(text, list_items, phone_number):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {BEARER}'
    }

    list_json = [
        {
            "id": item['value'],
            "title": item['text'],
            "description": item['description']
        } for item in list_items
    ]

    body = {
        "recipient_type": "individual",
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": text[0]
            },
            "body": {
                "text": text[1]
            },
            "footer": {
                "text": text[2]
            },
            "action": {
                "button": text[3],
                "sections": [
                    {
                        "rows": list_json
                    }
                ]
            }
        }
    }

    response = requests.post(
        f'https://graph.facebook.com/v14.0/{PHONE_ID}/messages',
        headers=headers,
        data=json.dumps(body)
    )

    print(response.text)

def prebuild(category, value):
    if category == "button" or category == "list":
        page = TemplatePage.objects.get(pk=value)
        return page
    elif category == "text":
        option = TemplateOption.objects.filter(value__iexact=value).first()
        if option is None:
            page = TemplatePage.objects.first()
            return page
        page = TemplatePage.objects.get(pk=option.template_page.id)
        return page
    else:
        page = TemplatePage.objects.filter(is_default=True).filter(template__status=True).first()
        return page


def page_builder(category, message):
    page = prebuild(category, message)
    if page.type == "text":
        return "text", page.body, []
    elif page.type == "button":
        options = TemplateOption.objects.filter(template_page=page).filter(type="button")
        buttons = [{"value": option.value, "text": option.text} for option in options]
        return "button", [page.header, page.body, page.footer], buttons
    elif page.type == "list":
        options = TemplateOption.objects.filter(template_page=page).filter(type="list")
        list_options = [{"value": option.value, "text": option.text, "description":option.description} for option in options]
        return "list", [page.header, page.body, page.footer, page.menu_title], list_options

# def send_button(text, buttons, phone_number):
#     options = []
#     for b in buttons:
#         options.append({"type": "reply",
#                         "reply": {
#                             "id": b['value'],
#                             "title": b['text']
#                         }
#                         })
#     messenger.send_reply_button(
#         recipient_id=phone_number,
#         button={
#             "type": "button",
#             "body": {
#                 "text": text
#             },
#             "action": {
#                 "buttons": options
#             }
#         },
#     )
