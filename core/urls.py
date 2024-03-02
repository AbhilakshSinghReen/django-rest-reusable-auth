from django.urls import path

from core.views.auth import RegisterUserAPIView


urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='auth_register'),
]
