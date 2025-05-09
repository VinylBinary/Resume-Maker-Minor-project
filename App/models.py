from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.

class resume_index(models.Model):
    user = models.ForeignKey(User,unique = True, on_delete=models.CASCADE, default=1)
    data = models.JSONField()
    def __str__(self):
        return self.user.username