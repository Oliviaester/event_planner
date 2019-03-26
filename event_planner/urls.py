
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('apps.app_1.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
