from django.urls import path
from .apis import QuestionAPIView, AnswerAPIView


urlpatterns = [
    path('question', QuestionAPIView.as_view()),
    path('question/<int:id>', QuestionAPIView.as_view()),
    path('answer', AnswerAPIView.as_view()),
]
