import csv
import threading
from io import StringIO
from chatbot.messanger import send_template
from chatbot.models import Batch, Number, MessageLog
from background_task import background
import time


@background
def batch_send(csv_data, template, language, data):
    # time.sleep(60)
    decoded_file = StringIO(csv_data)
    reader = csv.DictReader(decoded_file)
    batch = Batch(template=template, language=language)
    batch.save()
    print(f"Is current thread alive: {threading.current_thread().is_alive()}")
    for row in reader:
        phone_number = row.get('phone_number')
        if phone_number:
            number = None
            if Number.objects.filter(phone_number=phone_number).exists():
                number = Number.objects.filter(phone_number=phone_number).first()
            else:
                number = Number(phone_number=phone_number)
                number.save()
            print(phone_number)
            send_template(template=template, language=language, data=data, phone_number=phone_number)
            message_log = MessageLog(batch=batch, number=number)
            message_log.save()

