from django.urls import path
from .apis import ListNotification

urlpatterns = [
    path('answer', ListNotification.as_view())
]
