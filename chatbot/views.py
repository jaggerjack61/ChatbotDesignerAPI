from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .messanger import handle_payload, send_button, send_text, send_list, verify_webhook, page_builder


@api_view(['GET', 'POST'])
def webhook(request):
    if request.method == 'GET':
        return verify_webhook(request)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        category, message, phone_number = handle_payload(data)

        if message and phone_number:
            page_type, text, options = page_builder(category, message)
            if page_type == "text":
                send_text(text=text, phone_number=phone_number)
            elif page_type == "button":
                send_button(text=text, buttons=options, phone_number=phone_number)
            elif page_type == "list":
                send_list(text=text,list_items=options, phone_number=phone_number)
        else:
            print(data)
        return Response(status=status.HTTP_200_OK)
