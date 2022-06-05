from django.db import models
from Q_and_A.models import Questions, Answers
from django.contrib.auth.models import User

# Create your models here.

class Notify(models.Model):
    USER_CHOICES = (
        ('', '------'),
        ('Q', 'Questioner'),
        ('A', 'Answerer'),
    )
    
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    user_type = models.CharField(max_length=50, choices=USER_CHOICES)
    question = models.ForeignKey(Questions, null=True, blank=True, on_delete=models.PROTECT)
    answer = models.ForeignKey(Answers, null=True, blank=True, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'notify'
        verbose_name = 'Notify'
        verbose_name_plural = 'Notify'
        
    def __str__(self):
        return self.user.username + '-' + self.question.title + '-' + str(self.created.date())