import csv
from io import StringIO

from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .messanger import handle_payload, send_button, send_text, send_list, verify_webhook, page_builder, send_template, \
    extract_status_and_phone
from .models import Batch, Number, MessageLog
from .serializers import MessageLogSerializer
from .tasks import batch_send


@api_view(['GET', 'POST'])
def webhook(request):
    if request.method == 'GET':
        return verify_webhook(request)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        category, message, phone_number = handle_payload(data)
        number = None
        if phone_number is not None:
            if Number.objects.filter(phone_number=phone_number).exists():
                number = Number.objects.filter(phone_number=phone_number).first()
            else:
                number = Number(phone_number=phone_number)
                number.save()

        if category is not None:
            page_type, text, options = page_builder(category, message)
            if page_type == "text":
                send_text(text=text, phone_number=phone_number)
            elif page_type == "button":
                send_button(text=text, buttons=options, phone_number=phone_number)
            elif page_type == "list":
                send_list(text=text, list_items=options, phone_number=phone_number)
        else:
            try:
                msg_status, phone = extract_status_and_phone(data)
                print(msg_status)
                if number is not None:
                    if MessageLog.objects.filter(number=number).exists():
                        message_log = MessageLog.objects.filter(number=number).latest('created_at')
                        message_log.status = msg_status
                        message_log.save()
            except() as e:
                print(e)
        return Response(status=status.HTTP_200_OK)


class CSVUploadView(APIView):
    def get(self, request, *args, **kwargs):
        instances = MessageLog.objects.all().order_by('-created_at')
        # Serialize the queryset
        serializer = MessageLogSerializer(instances, many=True)
        return Response(data={'message_logs': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return JsonResponse({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data.get('variable')
        template = request.data.get('template')
        language = request.data.get('language')
        if data == "":
            data = None

        # Read the file into memory
        csv_file.seek(0)
        csv_data = csv_file.read().decode('UTF-8')

        # task = batch_send.delay(csv_data=csv_data, template=template, language=language, data=data)
        # return JsonResponse({'status': 'Batch process started','task':task.id}, status=status.HTTP_201_CREATED)
        batch_send(csv_data=csv_data, template=template, language=language, data=data)
        return JsonResponse({'status': 'Batch process started'}, status=status.HTTP_201_CREATED)



