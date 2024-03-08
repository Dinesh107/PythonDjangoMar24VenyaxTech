from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Heading(models.Model):
    name = models.CharField(max_length=200)


    def __str__(self):
        return self.name

class Space(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    heading = models.ForeignKey(Heading, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null = True, blank = True)
    #participants =
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Communicate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

   

    def __str__(self):
        return self.body[0:50]
