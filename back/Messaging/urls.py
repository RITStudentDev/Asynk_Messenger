from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('messages/send/', views.send_message, name='send_message'),
    path('messages/', views.get_messages, name='get_messages'),
    path('<str:room_name>/', views.room, name='room'),
    ]