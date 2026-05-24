from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('energy/', include('apps.energy.urls')),
    path('optimization/', include('apps.optimization.urls')),
    path('analytics/', include('apps.analytics.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
