import datetime

from django.db import models
from django.utils import timezone

class Test(models.Model):
    text = models.CharField(max_length=200)
    def __str__(self):
        return self.text
