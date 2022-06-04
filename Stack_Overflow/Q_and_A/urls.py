from django.urls import path
from .apis import QuestionAPIView


urlpatterns = [
    path('question', QuestionAPIView.as_view()),
    path('question/<int:id>', QuestionAPIView.as_view())
]
