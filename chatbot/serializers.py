from rest_framework import serializers

from chatbot.models import MessageLog


class MessageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageLog
        fields = "__all__"
        read_only_fields = ['created_at']
        depth = 1
