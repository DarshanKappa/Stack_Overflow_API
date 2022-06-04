from django.db import models

# Create your models here.


class Questions(models.Model):
    
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