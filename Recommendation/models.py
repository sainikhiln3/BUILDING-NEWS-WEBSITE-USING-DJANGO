from django.db import models
from django.contrib.auth.models import User
import numpy as np


# Create your models here.
  
class Recommended_Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_vector = models.TextField(default='nthg') # "nthg"
    recommended_text = models.TextField(default = "nthg") #"nthg"
    interest = models.TextField(null=True)
    

