from django.contrib.auth.models import User
from django.db import models


class Poll(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(default=' ')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class ForgotPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField()
    is_active = models.BooleanField(default=True)

