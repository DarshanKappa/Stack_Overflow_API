from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Questions(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    tag = models.CharField(null=True, blank=True, max_length=100)
    vote = models.IntegerField(default=0)
    
    class Meta:
        app_label = 'Q_and_A'
        verbose_name = 'Questions'
        verbose_name_plural = 'Questions'
        
    def __str__(self):
        return self.title


class Answers(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    vote = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'Q_and_A'
        verbose_name = 'Answers'
        verbose_name_plural = 'Answers'
        
    def __str__(self):
        return self.question.title
    

VOTE_CHOICES = (
        ('UP', 'UP'),
        ('', '-----'),
        ('DOWN', 'DOWN')
    )
class QuestionUserVotes(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey(Questions, related_name="question_votes", on_delete=models.PROTECT)
    up_down_vote = models.CharField(max_length=50, choices=VOTE_CHOICES)
    
    class Meta:
        app_label = 'Q_and_A'
        verbose_name = 'Question and User'
        verbose_name_plural = 'Question and User'


class AnswerUserVotes(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    answer = models.ForeignKey(Answers, related_name="answer_votes", on_delete=models.PROTECT)
    up_down_vote = models.CharField(max_length=50, choices=VOTE_CHOICES)
    
    class Meta:
        app_label = 'Q_and_A'
        verbose_name = 'Answer and User'
        verbose_name_plural = 'Answer and User'
        