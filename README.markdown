django-sld
==========

A django library that generates SLD documents from geographic models.

Requirements
============

  - *django* Required for models and spatial fields.
  - *python-sld* Required for reading and generating SLD XML files.
  - *pysal* Required for classification algorithms.
  - *colorbrewer* Required for color lookup definitions.

To install these requirements, you may use pip to install these packages
(except for django) with this command:

    > sudo pip install -r requirements.txt

Installation
============

    > easy_install django-sld

    OR

    > pip install django-sld

Usage
=====

This library implements a single module named "generator" that contains all
the methods of interacting with the classification algorithms. Assuming that
you have a geographic model in geodjango, you may classify your distribution
with by constructing a queryset, and feeding it to the generator.

Assuming you have a spatial model named *MySpatialModel*, with a data field 
of *population*, you can classify all your data into 10 quantile classes with:

    from djsld import generator

    qs = MySpatialModel.objects.all()
    sld = generator.as_quantiles(qs, 'population', 10)

You may also any queryset to generate classes, such as a filtered queryset:

    qs = MySpatialModel.objects.filter(owner__name = 'David')
    sld = generator.as_quantiles(qs, 'population', 10)

If your spatial model has a different geometry column name other than 'geom',
you may specify that field as the *geofield* keyword:

    sld = generator.as_quantiles(qs, 'population', 10, geofield='state')

The data field may also be distantly related to the queryset in question. For
this example, assume that *MySpatialModel* has a foreign key to a model named
*Route*, and that the data value you would like to classify is a field of the 
*Route* model:

    sld = generater.as_quantiles(qs, 'route__traffic', 10)

By default, all the generator methods use a plain black-to-white color ramp.
The number of classes must match an available color scheme, or the color ramp
will default to black-to-white. You may specify a colorbrewer ramp name with 
the *colorbrewername* keyword:

    sld = generator.as_quantiles(qs, 'population', 9, colorbrewername='Greys')

You may also reverse the order of the ramp, by specifying the *invertgradient*
keyword:

    sld = generator.as_quantiles(qs, 'population', 9, colorbrewername='Reds',
        invertgradient=True)


Support
=======

If you have any problems, questions, or comments, please visit the django-sld
project on github: https://github.com/azavea/django-sld/
