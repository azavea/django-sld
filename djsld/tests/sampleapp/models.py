from django.contrib.gis.db import models

class Hydrant(models.Model):
    number = models.IntegerField()
    location = models.PointField()
    pressure = models.FloatField()

    objects = models.GeoManager()

class Pipeline(models.Model):
    material = models.CharField(max_length=25)
    path = models.LineStringField()
    pressure = models.FloatField()

    objects = models.GeoManager()

