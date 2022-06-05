from django.urls import path
from .apis import QuestionAPIView, AnswerAPIView, QuestionAnswerList


urlpatterns = [
    path('question', QuestionAPIView.as_view()),
    path('question/<int:id>', QuestionAPIView.as_view()),
    path('answer', AnswerAPIView.as_view()),
    path('question-answer-list', QuestionAnswerList.as_view())
]
