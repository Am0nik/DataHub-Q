from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from university.models import University

class CustomUser(AbstractUser): 
    # добавь свои поля, если нужно
    pass
class Comment(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='comments')
    nickname = models.CharField("Ник", max_length=50)
    text = models.TextField("Сообщение")
    created_at = models.DateTimeField("Время отправки", auto_now_add=True)

    def __str__(self):
        return f"{self.nickname}: {self.text[:30]}"