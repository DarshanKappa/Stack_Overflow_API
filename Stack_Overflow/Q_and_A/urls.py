from django.urls import path
from .apis import VoteToAnswer, AnswerApproval, QuestionAPIView, AnswerAPIView, QuestionAnswerList, QuestionsOfUser, SearchQuestions, VoteToQuestion


urlpatterns = [
    path('question', QuestionAPIView.as_view()),
    path('question/<int:id>', QuestionAPIView.as_view()),
    path('questions/', QuestionsOfUser.as_view()),
    path('answer', AnswerAPIView.as_view()),
    path('question-answer-list', QuestionAnswerList.as_view()),
    path('answer-approval', AnswerApproval.as_view()),
    path('questions/tag', SearchQuestions.as_view()),
    path('vote/question', VoteToQuestion.as_view()),
    path('vote/answer', VoteToAnswer.as_view()),
]
