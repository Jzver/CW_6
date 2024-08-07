# mailings/serializers.py
from rest_framework import serializers
from .models import Client, Message, Mailing, MailingAttempt


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = '__all__'


class MailingAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingAttempt
        fields = '__all__'
