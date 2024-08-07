from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from django.core.mail import send_mail
from .models import Client, Message, Mailing, MailingAttempt, CustomUser
from .forms import ClientForm, MessageForm, MailingForm, MailingAttemptForm
from .serializers import ClientSerializer, MessageSerializer, MailingSerializer, MailingAttemptSerializer
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from users.forms import CustomUserCreationForm
from users.views import RegisterView
from rest_framework.permissions import IsAuthenticated
from users.models import User
from django.http import JsonResponse
from blog.models import Article
from blog.views import article_list
import random


def home(request):
    articles = list(Article.objects.all())
    random_articles = random.sample(articles, min(len(articles), 3))
    return render(request, 'home.html', {'random_articles': random_articles})


# Client views
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()  # Добавлено
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@login_required
def client_list(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)

    if not isinstance(request.user, CustomUser):
        return JsonResponse({'message': 'User is not an instance of CustomUser'}, status=400)

    clients = Client.objects.filter(owner=request.user)
    return render(request, 'clients/client_list.html', {'clients': clients})


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk, owner=request.user)
    return render(request, 'clients/client_detail.html', {'client': client})


@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.owner = request.user
            client.save()
            return redirect(reverse('mailings:client_list'))
    else:
        form = ClientForm()
    return render(request, 'clients/client_form.html', {'form': form})


@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect(reverse('mailings:client_detail', args=[pk]))
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/client_form.html', {'form': form})


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk, owner=request.user)
    if request.method == 'POST':
        client.delete()
        return redirect(reverse('mailings:client_list'))
    return render(request, 'clients/client_confirm_delete.html', {'client': client})


# Message views
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()  # Добавлено
    serializer_class = MessageSerializer


def message_list(request):
    messages = Message.objects.all()
    return render(request, 'message/message_list.html', {'messages': messages})


def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    return render(request, 'message/message_detail.html', {'message': message})


def message_create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('mailings:message_list'))
    else:
        form = MessageForm()
    return render(request, 'message/message_form.html', {'form': form})


def message_update(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect(reverse('mailings:message_detail', args=[pk]))
    else:
        form = MessageForm(instance=message)
    return render(request, 'message/message_form.html', {'form': form})


def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        message.delete()
        return redirect(reverse('mailings:message_list'))
    return render(request, 'message/message_confirm_delete.html', {'message': message})


# Mailing views
class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()  # Добавлено
    serializer_class = MailingSerializer


def mailing_list(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.save()
            form.save_m2m()  # Сохранение связей many-to-many (например, клиентов)
            return redirect(reverse('mailings:mailing_list'))  # Перенаправление на список рассылок
    else:
        form = MailingForm()

    mailings = Mailing.objects.all()
    return render(request, 'mailing_create.html', {'form': form, 'mailings': mailings})


def send_mailing(request):
    if request.method == 'POST':
        clients = request.POST.get('clients').split(',')
        message = request.POST.get('message')
        frequency = request.POST.get('frequency')

        for client in clients:
            send_mail(
                'Ваше сообщение',
                message,
                'from@example.com',
                [client],
            )

        return redirect(reverse('mailings:mailing_list'))
    else:
        return redirect(reverse('mailings:mailing_list'))


def mailing_detail(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    return render(request, 'mailing/mailing_detail.html', {'mailing': mailing})


def mailing_create(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.save()
            form.save_m2m()
            return redirect(reverse('mailings:mailing_list'))
    else:
        form = MailingForm()
    return render(request, 'mailing_create.html', {'form': form})


def mailing_update(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.method == 'POST':
        form = MailingForm(request.POST, instance=mailing)
        if form.is_valid():
            form.save()
            return redirect(reverse('mailings:mailing_detail', args=[pk]))
    else:
        form = MailingForm(instance=mailing)
    return render(request, 'mailing/mailing_form.html', {'form': form})


def mailing_delete(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.method == 'POST':
        mailing.delete()
        return redirect(reverse('mailings:mailing_list'))
    return render(request, 'mailing/mailing_confirm_delete.html', {'mailing': mailing})


@login_required
def update_mailing_settings(request):
    if request.method == 'POST':
        frequency = request.POST.get('frequency')
        request.session['mailing_frequency'] = frequency  # Пример сохранения в сессии
        messages.success(request, 'Mailing settings updated successfully.')
        return redirect(reverse('mailings:mailing_list'))
    else:
        return redirect(reverse('mailings:mailing_list'))  # Перенаправление при GET-запросе


# MailingAttempt views
class MailingAttemptViewSet(viewsets.ModelViewSet):
    queryset = MailingAttempt.objects.all()  # Добавлено
    serializer_class = MailingAttemptSerializer


def mailing_attempt_list(request):
    mailing_attempts = MailingAttempt.objects.all()
    return render(request, 'mailing_attempt/mailing_attempt_list.html', {'mailing_attempts': mailing_attempts})


def mailing_attempt_detail(request, pk):
    mailing_attempt = get_object_or_404(MailingAttempt, pk=pk)
    return render(request, 'mailing_attempt/mailing_attempt_detail.html', {'mailing_attempt': mailing_attempt})


def mailing_attempt_create(request):
    if request.method == 'POST':
        form = MailingAttemptForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('mailings:mailing_attempt_list'))
    else:
        form = MailingAttemptForm()
    return render(request, 'mailing_attempt/mailing_attempt_form.html', {'form': form})


def mailing_attempt_update(request, pk):
    mailing_attempt = get_object_or_404(MailingAttempt, pk=pk)
    if request.method == 'POST':
        form = MailingAttemptForm(request.POST, instance=mailing_attempt)
        if form.is_valid():
            form.save()
            return redirect(reverse('mailings:mailing_attempt_detail', args=[pk]))
    else:
        form = MailingAttemptForm(instance=mailing_attempt)
    return render(request, 'mailing_attempt/mailing_attempt_form.html', {'form': form})


def mailing_attempt_delete(request, pk):
    mailing_attempt = get_object_or_404(MailingAttempt, pk=pk)
    if request.method == 'POST':
        mailing_attempt.delete()
        return redirect(reverse('mailings:mailing_attempt_list'))
    return render(request, 'mailing_attempt/mailing_attempt_confirm_delete.html', {'mailing_attempt': mailing_attempt})
