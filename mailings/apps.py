from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

class MailingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailings'

    def ready(self):
        # Импортируем send_mailing здесь, чтобы избежать циклических зависимостей и проблем с импортом
        from .tasks import send_mailing

        if settings.SCHEDULER_AUTOSTART:
            start(send_mailing)

def start(send_mailing):
    scheduler = BackgroundScheduler()
    # Убедитесь, что функция send_mailing передана в scheduler
    scheduler.add_job(send_mailing, 'interval', minutes=1)
    scheduler.start()
