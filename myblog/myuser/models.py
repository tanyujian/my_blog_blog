from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):
    nickname = models.CharField(blank=True, max_length=50,verbose_name='昵称')
    chart_heads = models.ImageField(blank=True,upload_to='user_image',verbose_name='头像')
    class Meta:
        verbose_name_plural='myuser'

