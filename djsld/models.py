from django.contrib.gis.db import models

class Hydrant(models.Model):
    number = models.IntegerField()
    location = models.PointField()
    pressure = models.FloatField()

    objects = models.GeoManager()
