from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Stamp(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    mood = models.CharField(max_length=10)
    notes = models.CharField(max_length=250)
    title = models.CharField(max_length=25, default=mood)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.title)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birthdate = models.DateField("birth day")
