from django.db import models
from django.contrib.auth.models import User


class XlsxFile(models.Model):
    file_name = models.CharField(max_length=13, primary_key=True, unique=True)

    def __str__(self):
        return self.file_name


class Ship(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    code = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=2048)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class LatLngHistory(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    dt = models.DateTimeField()
    lat = models.FloatField()
    lng = models.FloatField()
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)

    def __str__(self):
        return self.ship.name
