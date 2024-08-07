from django.contrib import admin
from .models import Client, Message, Mailing, MailingAttempt, CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from blog.models import Article

admin.site.register(Client)
admin.site.register(Message)
admin.site.register(Mailing)
admin.site.register(MailingAttempt)
admin.site.register(CustomUser)
admin.site.register(User, UserAdmin)
admin.site.register(Article)
