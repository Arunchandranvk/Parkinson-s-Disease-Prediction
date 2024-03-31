from django.urls import path
from .views import *

urlpatterns = [
    path('chatbot/',Chatbot,name='bot'),
]