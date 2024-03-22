from rest_framework import serializers
from .models import Template, TemplatePage, TemplateOption


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = "__all__"
        read_only_fields = ['created_at']


class TemplatePageSerializer(serializers.ModelSerializer):
    templateId = serializers.PrimaryKeyRelatedField(queryset=Template.objects.all(), write_only=True)
    template = TemplateSerializer(read_only=True)

    class Meta:
        model = TemplatePage
        fields = "__all__"
        read_only_fields = ['created_at']
        depth = 1

    def create(self, validated_data):
        templateId = validated_data.pop('templateId')
        template_page = TemplatePage.objects.create(template=templateId, **validated_data)
        return template_page

    def update(self, instance, validated_data):
        # If 'templateId' is in validated_data, update the 'template' field
        if 'templateId' in validated_data:
            templateId = validated_data.pop('templateId')
            instance.template = templateId

        # Update other fields if they are in validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the updated instance
        instance.save()

        return instance


class TemplateOptionSerializer(serializers.ModelSerializer):
    template_pageId = serializers.PrimaryKeyRelatedField(queryset=TemplatePage.objects.all(), write_only=True)
    template_page = TemplatePageSerializer(read_only=True)

    class Meta:
        model = TemplateOption
        fields = "__all__"
        read_only_fields = ['created_at']
        depth = 1

    def create(self, validated_data):
        template_pageId = validated_data.pop('template_pageId')
        template_option = TemplateOption.objects.create(template_page=template_pageId, **validated_data)
        return template_option

    def update(self, instance, validated_data):
        # If 'templateId' is in validated_data, update the 'template' field
        if 'template_pageId' in validated_data:
            template_pageId = validated_data.pop('template_pageId')
            instance.template_page = template_pageId

        # Update other fields if they are in validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the updated instance
        instance.save()

        return instance




