from rest_framework import viewsets
from .models import Template, TemplatePage, TemplateOption
from .serealizers import TemplateSerializer, TemplatePageSerializer, TemplateOptionSerializer


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


class TemplatePageViewSet(viewsets.ModelViewSet):
    queryset = TemplatePage.objects.all()
    serializer_class = TemplatePageSerializer


class TemplateOptionViewSet(viewsets.ModelViewSet):
    queryset = TemplateOption.objects.all()
    serializer_class = TemplateOptionSerializer
