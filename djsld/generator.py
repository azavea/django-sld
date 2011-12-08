"""
A class break generator.
"""
from sld import *
from numpy import array, ndarray
from pysal.esda.mapclassify import *
from django.contrib.gis.db.models import fields

def as_equal_interval(*args, **kwargs):
    """
    Generate equal interval classes from the provided queryset. If the queryset
    is empty, no class breaks are returned.

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
    return _as_classification(Fisher_Jenks, *args, **kwargs)

def as_jenks_caspall(*args, **kwargs):
    return _as_classification(Jenks_Caspall, *args, **kwargs)

def as_jenks_caspall_forced(*args, **kwargs):
    return _as_classification(Jenks_Caspall_Forced, *args, **kwargs)

def as_jenks_caspall_sampled(*args, **kwargs):
    return _as_classification(Jenks_Caspall_Sampled, *args, **kwargs)

def as_max_p_classifier(*args, **kwargs):
    return _as_classification(Max_P_Classifier, *args, **kwargs)

def as_maximum_breaks(*args, **kwargs):
    return _as_classification(Maximum_Breaks, *args, **kwargs)

def as_natural_breaks(*args, **kwargs):
    return _as_classification(Natural_Breaks, *args, **kwargs)

def as_quantiles(*args, **kwargs):
    return _as_classification(Quantiles, *args, **kwargs)

def _as_classification(classification, queryset, field, nclasses, geofield='geom'):
    """
    Accept a queryset of objects, and return the values of the class breaks 
    on the data distribution. If the queryset is empty, no class breaks are
    computed.

    @type  classification: pysal classifier
    @param classification: A classification class defined in 
        pysal.esda.mapclassify. As of 12/2011, this list is comprised of:

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

    datavalues = array(queryset.order_by(field).values_list(field, flat=True))
    q = classification(datavalues, nclasses)

    nl = thesld.create_namedlayer('%d breaks on "%s" as %s' % (nclasses, field, classification.__name__))
    us = nl.create_userstyle()
    fts = us.create_featuretypestyle()

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
            f_low.PropertyIsGreaterThan.PropertyName = field
            f_low.PropertyIsGreaterThan.Literal = str(q.bins[i-1])

        f_high = Filter(rule)
        f_high.PropertyIsLessThanOrEqualTo = PropertyCriterion(f_high, 'PropertyIsLessThanOrEqualTo')
        f_high.PropertyIsLessThanOrEqualTo.PropertyName = field
        f_high.PropertyIsLessThanOrEqualTo.Literal = str(qbin)

       
        if i > 0:
            rule.Filter = f_low + f_high
        else:
            rule.Filter = f_high
           
    thesld.normalize()

    return thesld
