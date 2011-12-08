from django.contrib.gis.db import models

class Hydrant(models.Model):
    number = models.IntegerField()
    location = models.PointField()
    pressure = models.FloatField()
    pipeline = models.ForeignKey('Pipeline')

    objects = models.GeoManager()

class Pipeline(models.Model):
    material = models.CharField(max_length=25)
    path = models.LineStringField()
    diameter = models.FloatField()
    reservoir = models.ForeignKey('Reservoir')

    objects = models.GeoManager()

class Reservoir(models.Model):
    name = models.CharField(max_length=25)
    volume = models.FloatField()
    coastline = models.PolygonField()

    objects = models.GeoManager()
