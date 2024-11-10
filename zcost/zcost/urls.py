from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('settings.urls', namespace='settings')),
    path('install/', include('core.urls', namespace='core')),
    path('dealcard/', include('task.urls', namespace='dealcard')),
]