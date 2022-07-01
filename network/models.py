from tkinter.messagebox import RETRY
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    follow = models.ManyToManyField('self' , blank=True , related_name='followers' , symmetrical=False)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE , related_name='posts')
    desc = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User,blank=True , related_name='user_likes')




    def __str__(self) :
        return f'{self.author} {self.desc} {self.date}'

    def likes(self):
        return self.like.all().count()
    class Meta:
        ordering = ('-date',)

