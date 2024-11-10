from django.urls import path

from task import views

app_name = 'dealcard'

urlpatterns = [
    path('', views.index, name='index'),
]