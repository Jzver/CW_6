

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mailings import views as mailings_views  # Импортируем представления из mailings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', mailings_views.home, name='home'),  # Главная страница
    path('api/', include('mailings.urls', namespace='mailings')),
    path('blog/', include('blog.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

