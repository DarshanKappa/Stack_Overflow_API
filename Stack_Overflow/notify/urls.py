from django.urls import path
from .apis import AnswerNotification, ApprovedNotification

urlpatterns = [
    path('answer', AnswerNotification.as_view()),
    path('approved', ApprovedNotification.as_view())
]
