from django.urls import path
from .apis import RegistrationAPIView


urlpatterns = [
    path('signup', RegistrationAPIView.as_view()),
]
