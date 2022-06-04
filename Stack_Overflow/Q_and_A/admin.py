from django.contrib import admin

from Q_and_A.models import Answers, Questions

# Register your models here.

admin.site.register(Questions)
admin.site.register(Answers)