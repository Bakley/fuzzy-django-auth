from django.urls import path

from .views import RegistrationAPIView, LoginAPIView

urlpatterns = [
    path("users/register", RegistrationAPIView.as_view(), name='registration'),
    path("users/login", LoginAPIView.as_view(), name='login'),
]
