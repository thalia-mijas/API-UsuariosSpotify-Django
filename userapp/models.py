from django.db import models

# Create your models here.
class User(models.Model):
  name = models.TextField(max_length=250)
  email = models.EmailField(max_length=250, unique=True)
  preferences = models.TextField(max_length=250)

  def __str__(self):
      return {self.name, self.email, self.preferences}