from django.db import models
from django.apps import apps

# Create your models here.

class SignUp (models.Model):

    name = models.CharField(max_length=100, primary_key=False)
    phone = models.IntegerField(primary_key = False)
    user_id = models.IntegerField(primary_key = True)
    street = models.CharField(max_length=100, primary_key=False)
    city = models.CharField(max_length=100, primary_key=False)
    state = models.CharField(max_length=100, primary_key=False)
    zip = models.IntegerField( primary_key=False)
    password = models.CharField(max_length=100, primary_key=False)

class data (models.Model):

    item = models.CharField(max_length=100, primary_key=False)
    price = models.FloatField(max_length=100, primary_key=False)
    item_id = models.IntegerField(max_length=10, primary_key=True)

class accepted (models.Model):

    item = models.CharField(max_length=100, primary_key=False)
    user = models.ForeignKey(SignUp, on_delete=models.CASCADE)

class currentQuests (models.Model):

    item = models.CharField(max_length = 100, primary_key = True)
    user = models.ForeignKey(SignUp, on_delete=models.CASCADE)
    valid = models.CharField(max_length = 100, primary_key = False)


