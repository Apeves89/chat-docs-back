from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.chat, name="chat"),
    path("upload/", views.upload, name="upload"),
]
