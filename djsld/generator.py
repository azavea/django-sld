"""
Generate StyledLayerDescriptor objecs for django querysets.

This generator uses the python-sld and pysal libraries to generate classes
for map classification, and returns a StyledLayerDescriptor class object. This
class object may be serialized to an SLD XML file, which is useful for many
GIS and mapping software packages.

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

from sld import *
from numpy import array, ndarray
from pysal.esda.mapclassify import *
from django.contrib.gis.db.models import fields

def as_equal_interval(*args, **kwargs):
    """
    Generate equal interval classes from the provided queryset. If the queryset
    is empty, no class breaks are returned. For more information on the Equal
    Interval classifier, please visit:
    
    U{http://pysal.geodacenter.org/1.2/library/esda/mapclassify.html#pysal.esda.mapclassify.Equal_Interval}

    @type  queryset: QuerySet
    @param queryset: The query set that contains the entire distribution of
        data values.
    @type  field: string
    @param field: The name of the field on the model in the queryset that 
        contains the data values.
    @type  nclasses: integer
    @param nclasses: The number of class breaks desired.
    @type  geofield: string
    @param geofield: The name of the geometry field. Defaults to 'geom'.
    @rtype: L{sld.StyledLayerDescriptor}
    @returns: An SLD object that represents the class breaks.
    """
    return _as_classification(Equal_Interval, *args, **kwargs)

def as_fisher_jenks(*args, **kwargs):
    """
    Generate Fisher-Jenks classes from the provided queryset. If the queryset
    is empty, no class breaks are returned. For more information on the Fisher
    Jenks classifier, please visit:

    U{http://pysal.geodacenter.org/1.2/library/esda/mapclassify.html#pysal.esda.mapclassify.Fisher_Jenks}

    @type  queryset: QuerySet
    @param queryset: The query set that contains the entire distribution of
        data values.
    @type  field: string
    @param field: The name of the field on the model in the queryset that 
        contains the data values.
    @type  nclasses: integer
    @param nclasses: The number of class breaks desired.
    @type  geofield: string
    @param geofield: The name of the geometry field. Defaults to 'geom'.
    @rtype: L{sld.StyledLayerDescriptor}
    @returns: An SLD object that represents the class breaks.
    """
    return _as_classification(Fisher_Jenks, *args, **kwargs)

def as_jenks_caspall(*args, **kwargs):
    """
    Generate Jenks-Caspall classes from the provided queryset. If the queryset
    is empty, no class breaks are returned. For more information on the Jenks
    Caspall classifier, please visit:

    U{http://pysal.geodacenter.org/1.2/library/esda/mapclassify.html#pysal.esda.mapclassify.Jenks_Caspall}

    @type  queryset: QuerySet
    @param queryset: The query set that contains the entire distribution of
        data values.
    @type  field: string
    @param field: The name of the field on the model in the queryset that 
        contains the data values.
    @type  nclasses: integer
    @param nclasses: The number of class breaks desired.
    @type  geofield: string
    @param geofield: The name of the geometry field. Defaults to 'geom'.
    @rtype: L{sld.StyledLayerDescriptor}
    @returns: An SLD object that represents the class breaks.
    """
    return _as_classification(Jenks_Caspall, *args, **kwargs)

def as_jenks_caspall_forced(*args, **kwargs):
    """
    Generate Jenks-Caspall Forced classes from the provided queryset. If the queryset
    is empty, no class breaks are returned. For more information on the Jenks
    Caspall Forced classifier, please visit:

    U{http://pysal.geodacenter.org/1.2/library/esda/mapclassify.html#pysal.esda.mapclassify.Jenks_Caspall_Forced}

    @type  queryset: QuerySet
    @param queryset: The query set that contains the entire distribution of
        data values.
    @type  field: string
    @param field: The name of the field on the model in the queryset that 
        contains the data values.
    @type  nclasses: integer
    @param nclasses: The number of class breaks desired.
    @type  geofield: string
    @param geofield: The name of the geometry field. Defaults to 'geom'.
    @rtype: L{sld.StyledLayerDescriptor}
    @returns: An SLD object that represents the class breaks.
    """
    return _as_classification(Jenks_Caspall_Forced, *args, **kwargs)

def as_jenks_caspall_sampled(*args, **kwargs):
    """
    Generate Jenks-Caspall Sampled classes from the provided queryset. If the queryset
    is empty, no class breaks are returned. For more information on the Jenks
    Caspall Sampled classifier, please visit:

    U{http://pysal.geodacenter.org/1.2/library/esda/mapclassify.html#pysal.esda.mapclassify.Jenks_Caspall_Sampled}

    @type  queryset: QuerySet
    @param queryset: The query set that contains the entire distribution of
        data values.
    @type  field: string
    @param field: The name of the field on the model in the queryset that 
        contains the data values.
    @type  nclasses: integer
    @param nclasses: The number of class breaks desired.
    @type  geofield: string
    @param geofield: The name of the geometry field. Defaults to 'geom'.
    @rtype: L{sld.StyledLayerDescriptor}
    @returns: An SLD object that represents the class breaks.
    """
    return _as_classification(Jenks_Caspall_Sampled, *args, **kwargs)

def as_max_p_classifier(*args, **kwargs):
    """
    Generate Max P classes from the provided queryset. If the queryset
    is empty, no class breaks are returned. For more information on the Max P
    classifier, please visit:

    U{http://pysal.geodacenter.org/1.2/library/esda/mapclassify.html#pysal.esda.mapclassify.Max_P_Classifier}

    @type  queryset: QuerySet
    @param queryset: The query set that contains the entire distribution of
        data values.
    @type  field: string
    @param field: The name of the field on the model in the queryset that 
        contains the data values.
    @type  nclasses: integer
    @param nclasses: The number of class breaks desired.
    @type  geofield: string
    @param geofield: The name of the geometry field. Defaults to 'geom'.
    @rtype: L{sld.StyledLayerDescriptor}
    @returns: An SLD object that represents the class breaks.
    """
    return _as_classification(Max_P_Classifier, *args, **kwargs)

def as_maximum_breaks(*args, **kwargs):
    """
    Generate Maximum Breaks classes from the provided queryset. If the queryset
    is empty, no class breaks are returned. For more information on the Maximum
    Breaks classifier, please visit:

    U{http://pysal.geodacenter.org/1.2/library/esda/mapclassify.html#pysal.esda.mapclassify.Maximum_Breaks}

    @type  queryset: QuerySet
    @param queryset: The query set that contains the entire distribution of
        data values.
    @type  field: string
    @param field: The name of the field on the model in the queryset that 
        contains the data values.
    @type  nclasses: integer
    @param nclasses: The number of class breaks desired.
    @type  geofield: string
    @param geofield: The name of the geometry field. Defaults to 'geom'.
    @rtype: L{sld.StyledLayerDescriptor}
    @returns: An SLD object that represents the class breaks.
    """
    return _as_classification(Maximum_Breaks, *args, **kwargs)

def as_natural_breaks(*args, **kwargs):
    """
    Generate Natural Breaks classes from the provided queryset. If the queryset
    is empty, no class breaks are returned. For more information on the Natural
    Breaks classifier, please visit:

    U{http://pysal.geodacenter.org/1.2/library/esda/mapclassify.html#pysal.esda.mapclassify.Natural_Breaks}

    @type  queryset: QuerySet
    @param queryset: The query set that contains the entire distribution of
        data values.
    @type  field: string
    @param field: The name of the field on the model in the queryset that 
        contains the data values.
    @type  nclasses: integer
    @param nclasses: The number of class breaks desired.
    @type  geofield: string
    @param geofield: The name of the geometry field. Defaults to 'geom'.
    @rtype: L{sld.StyledLayerDescriptor}
    @returns: An SLD object that represents the class breaks.
    """
    return _as_classification(Natural_Breaks, *args, **kwargs)

def as_quantiles(*args, **kwargs):
    """
    Generate Quantile classes from the provided queryset. If the queryset
    is empty, no class breaks are returned. For more information on the Quantile
    classifier, please visit:

    U{http://pysal.geodacenter.org/1.2/library/esda/mapclassify.html#pysal.esda.mapclassify.Quantiles}

    @type  queryset: QuerySet
    @param queryset: The query set that contains the entire distribution of
        data values.
    @type  field: string
    @param field: The name of the field on the model in the queryset that 
        contains the data values.
    @type  nclasses: integer
    @param nclasses: The number of class breaks desired.
    @type  geofield: string
    @param geofield: The name of the geometry field. Defaults to 'geom'.
    @rtype: L{sld.StyledLayerDescriptor}
    @returns: An SLD object that represents the class breaks.
    """
    return _as_classification(Quantiles, *args, **kwargs)

def _as_classification(classification, queryset, field, nclasses, geofield='geom', 
    propertyname=None, userstyletitle=None, featuretypestylename=None, **kwargs):
    """
    Accept a queryset of objects, and return the values of the class breaks 
    on the data distribution. If the queryset is empty, no class breaks are
    computed.

    @type  classification: pysal classifier
    @param classification: A classification class defined in 
        pysal.esda.mapclassify. As of version 1.0.1, this list is comprised of:

          - Equal_Interval
          - Fisher_Jenks
          - Jenks_Caspall
          - Jenks_Caspall_Forced
          - Jenks_Caspall_Sampled
          - Max_P_Classifier
          - Maximum_Breaks
          - Natural_Breaks
          - Quantiles

    @type  queryset: QuerySet
    @param queryset: The query set that contains the entire distribution of data values.
    @type     field: string
    @param    field: The name of the field on the model in the queryset that contains the data values.
    @type  nclasses: integer
    @param nclasses: The number of class breaks desired.
    @type  geofield: string
    @param geofield: The name of the geography column on the model. Defaults to 'geom'
    @type  propertyname: string
    @param propertyname: The name of the filter property name, if different from the model field.
    @type  userstyletitle: string
    @param userstyletitle: The title of the UserStyle element.
    @type  featuretypestylename: string
    @param featuretypestylename: The name of the FeatureTypeStyle element.
    @type    kwargs: keywords
    @param   kwargs: Additional keyword arguments for the classifier.
    @rtype: L{sld.StyledLayerDescriptor}
    @returns: An SLD class object that represents the classification scheme 
        and filters.
    """
    thesld = StyledLayerDescriptor()

    ftype = queryset.model._meta.get_field_by_name(geofield)[0]
    if isinstance(ftype, fields.LineStringField) or isinstance(ftype, fields.MultiLineStringField):
        symbolizer = LineSymbolizer
    elif isinstance(ftype, fields.PolygonField) or isinstance(ftype, fields.MultiPolygonField):
        symbolizer = PolygonSymbolizer
    else:
        # PointField, MultiPointField, GeometryField, or GeometryCollectionField
        symbolizer = PointSymbolizer

    if propertyname is None:
        propertyname = field

    datavalues = array(queryset.order_by(field).values_list(field, flat=True))
    q = classification(datavalues, nclasses, **kwargs)

    nl = thesld.create_namedlayer('%d breaks on "%s" as %s' % (nclasses, field, classification.__name__))
    us = nl.create_userstyle()
    if not userstyletitle is None:
        us.Title = str(userstyletitle)
    fts = us.create_featuretypestyle()
    if not featuretypestylename is None:
        fts.Name = str(featuretypestylename)

    for i,qbin in enumerate(q.bins):
        if type(qbin) == ndarray:
            qbin = qbin[0]

        title = '<= %s' % qbin
        rule = fts.create_rule(title, symbolizer=symbolizer)

        shade = float(i) / (q.k - 1.0) * 255
        if i == q.k:
            shade = 255

        shade = '#%02x%02x%02x' % (shade, shade, shade,)

        if symbolizer == PointSymbolizer:
            rule.PointSymbolizer.Graphic.Mark.Fill.CssParameters[0].Value = shade
        elif symbolizer == LineSymbolizer:
            rule.LineSymbolizer.Stroke.CssParameters[0].Value = shade
        elif symbolizer == PolygonSymbolizer:
            rule.PolygonSymbolizer.Fill.CssParameters[0].Value = shade

        # now add the filters
        if i > 0:
            f_low = Filter(rule)
            f_low.PropertyIsGreaterThan = PropertyCriterion(f_low, 'PropertyIsGreaterThan')
            f_low.PropertyIsGreaterThan.PropertyName = propertyname
            f_low.PropertyIsGreaterThan.Literal = str(q.bins[i-1])

        f_high = Filter(rule)
        f_high.PropertyIsLessThanOrEqualTo = PropertyCriterion(f_high, 'PropertyIsLessThanOrEqualTo')
        f_high.PropertyIsLessThanOrEqualTo.PropertyName = propertyname
        f_high.PropertyIsLessThanOrEqualTo.Literal = str(qbin)

       
        if i > 0:
            rule.Filter = f_low + f_high
        else:
            rule.Filter = f_high
           
    thesld.normalize()

    return thesld
