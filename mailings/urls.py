from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet, MessageViewSet, MailingViewSet, MailingAttemptViewSet,
    home, message_list, message_detail, message_create, message_update, message_delete,
    mailing_list, mailing_detail, mailing_create, mailing_update, mailing_delete,
    mailing_attempt_list, mailing_attempt_detail, mailing_attempt_create,
    mailing_attempt_update, mailing_attempt_delete, client_list, client_detail,
    client_create, client_update, client_delete, send_mailing, update_mailing_settings,
)
from . import views

app_name = 'mailings'

# Router for viewsets
router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'mailings', MailingViewSet)
router.register(r'mailing-attempts', MailingAttemptViewSet)

urlpatterns = [
    path('', views.home, name='home'),

    # API routes
    path('api/', include(router.urls)),

    # Messages routes
    path('messages/', message_list, name='message_list'),
    path('messages/create/', message_create, name='message_create'),
    path('messages/<int:pk>/', message_detail, name='message_detail'),
    path('messages/<int:pk>/update/', message_update, name='message_update'),
    path('messages/<int:pk>/delete/', message_delete, name='message_delete'),

    # Mailings routes
    path('mailings/', mailing_list, name='mailing_list'),
    path('mailings/create/', mailing_create, name='mailing_create'),
    path('mailings/send/', send_mailing, name='send_mailing'),
    path('mailings/settings/update/', update_mailing_settings, name='update_mailing_settings'),
    path('mailings/<int:pk>/', mailing_detail, name='mailing_detail'),
    path('mailings/<int:pk>/update/', mailing_update, name='mailing_update'),
    path('mailings/<int:pk>/delete/', mailing_delete, name='mailing_delete'),

    # Mailing attempts routes
    path('mailing_attempts/', mailing_attempt_list, name='mailing_attempt_list'),
    path('mailing_attempts/create/', mailing_attempt_create, name='mailing_attempt_create'),
    path('mailing_attempts/<int:pk>/', mailing_attempt_detail, name='mailing_attempt_detail'),
    path('mailing_attempts/<int:pk>/update/', mailing_attempt_update, name='mailing_attempt_update'),
    path('mailing_attempts/<int:pk>/delete/', mailing_attempt_delete, name='mailing_attempt_delete'),

    # Clients routes
    path('clients/', client_list, name='client_list'),
    path('clients/create/', client_create, name='client_create'),
    path('clients/<int:pk>/', client_detail, name='client_detail'),
    path('clients/<int:pk>/update/', client_update, name='client_update'),
    path('clients/<int:pk>/delete/', client_delete, name='client_delete'),
    path('blog/', views.article_list, name='article_list'),
]
