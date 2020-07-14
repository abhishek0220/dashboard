from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Member(AbstractUser):
   gender = models.CharField(max_length = 6 ,blank=False)
   class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
   def name(self):
      return self.first_name + " " + self.last_name

class Pin(models.Model):
   author=models.ForeignKey(Member,on_delete=models.CASCADE)
   content = models.CharField(max_length=1000)
   pub_date = models.DateTimeField('date published')
   likes = models.IntegerField(default=0)
   def __str__(self):
      return self.content[:10]
   def names(self):
      return self.author.username

   
   
