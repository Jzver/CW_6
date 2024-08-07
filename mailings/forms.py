# forms.py

from django import forms
from .models import Client, Message, Mailing, MailingAttempt
from utils.forms_mixins import StyleFormMixin


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']


class MailingForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        label="Дата и время начала"
    )

    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Выберите клиентов"
    )

    class Meta:
        model = Mailing
        fields = ['start_datetime', 'periodicity', 'status', 'message', 'clients']


class MailingAttemptForm(forms.ModelForm):
    class Meta:
        model = MailingAttempt
        fields = ['mailing', 'status', 'server_response']
