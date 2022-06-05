from django.contrib import admin

from Q_and_A.models import AnswerUserVotes, Answers, QuestionUserVotes, Questions

# Register your models here.

admin.site.register(Questions)
admin.site.register(Answers)
admin.site.register(QuestionUserVotes)
admin.site.register(AnswerUserVotes)