from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Member(AbstractUser):
   gender = models.CharField(max_length = 6 ,blank=False)
   class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'