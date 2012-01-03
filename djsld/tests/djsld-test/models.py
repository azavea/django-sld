"""
Test models for django-sld unit tests.

License
=======
Copyright 2011 David Zwarg <U{dzwarg@azavea.com}>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

U{http://www.apache.org/licenses/LICENSE-2.0}

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@author: David Zwarg
@contact: dzwarg@azavea.com
@copyright: 2011, Azavea
@license: Apache 2.0
@version: 1.0.4
"""

from django.contrib.gis.db import models

class Hydrant(models.Model):
    """
    A sample point-based geographic model.
    """

    number = models.IntegerField()
    """The number of the Hydrant. Not the primary key or object id."""

    location = models.PointField()
    """The geographic location of this Hydrant."""

    pressure = models.FloatField()
    """The pressure measured at this Hydrant."""

    pipeline = models.ForeignKey('Pipeline')
    """The L{Pipeline} that this Hydrant is connected to."""

    objects = models.GeoManager()
    """The geographic object manager."""

class Pipeline(models.Model):
    """
    A sample line-based geographic model.
    """

    material = models.CharField(max_length=25)
    """The material used to build this pipeline."""

    path = models.LineStringField()
    """The geographic representation of this pipeline, as a line."""

    diameter = models.FloatField()
    """The diameter of this Pipeline."""

    reservoir = models.ForeignKey('Reservoir')
    """The L{Reservoir} that this Pipeline feeds from."""

    objects = models.GeoManager()
    """The geographic object manager."""

class Reservoir(models.Model):
    """
    A sample polygon-based geographic model.
    """

    name = models.CharField(max_length=25)
    """The name of this reservoir."""

    volume = models.FloatField()
    """The volume of water stored."""

    coastline = models.PolygonField()
    """The geographic coverage of this reservoir."""

    objects = models.GeoManager()
    """The geographic object manager."""
