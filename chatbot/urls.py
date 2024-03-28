from django.urls import path
from .views import webhook, CSVUploadView

urlpatterns = [
    path('webhook/', webhook, name='webhook'),
    path('bulk/', CSVUploadView.as_view(), name='upload-csv'),
]