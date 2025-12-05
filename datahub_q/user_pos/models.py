from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser): 
    # добавь свои поля, если нужно
    pass
