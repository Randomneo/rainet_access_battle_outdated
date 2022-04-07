from django.urls import re_path

from . import views

websocket_urlpatterns = [
    re_path('game/', views.GameConsumer.as_asgi()),
]
