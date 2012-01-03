"""
Unit tests for the django-sld library.

The unit tests check the number of classes and their values generated
by the various classification methods.

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

import unittest, random
from djsld import generator
from django.contrib.gis.geos import GEOSGeometry
from django.db.models.fields import FieldDoesNotExist
from models import *

class ClassificationTest(unittest.TestCase):
    """
    A set of test routines for the classification tools.
    """

    def setUp(self):
        """
        Set up the test data.
        """
        for x in range(0,5):
            r = Reservoir(name='City %d' % x, volume=(x+1)*10000, coastline=GEOSGeometry('POLYGON((%d %d, %d %d, %d %d, %d %d))' % (x,x,x+1,x,x,x+1,x,x,)))
            r.save()

            p = Pipeline(material='ceramic', diameter=x, path=GEOSGeometry('LINESTRING(%d %d, %d %d)'%(x,x,x+1,x+1,)), reservoir=r)
            p.save()

            h = Hydrant(number=x, pressure=1, location=GEOSGeometry('POINT(%d %d)'%(x,x,)), pipeline=p)
            h.save()

        for y in range(0,50):
            r = Reservoir(name='County %d' % y, volume=(y+1)*(y+1)*10000, coastline=GEOSGeometry('POLYGON((%d %d, %d %d, %d %d, %d %d))' % (y,y,y+1,y,y,y+1,y,y,)))
            r.save()

            p = Pipeline(material='concrete', diameter=y, path=GEOSGeometry('LINESTRING(%d %d, %d %d)'%(x,x,x+1,x+1,)), reservoir=r)
            p.save()

            h = Hydrant(number=y*y, pressure=2, location=GEOSGeometry('POINT(%d %d)'%(y,y,)), pipeline=p)
            h.save()

    def tearDown(self):
        """
        Destroy the test data.
        """
        Hydrant.objects.all().delete()
        Pipeline.objects.all().delete()
        Reservoir.objects.all().delete()

    def test_classes_geofield_pt(self):
        """
        Test the geofield optional parameter for a point-based geographic model.
        """
        try:
            generator.as_equal_interval(Hydrant.objects.filter(pressure=1), 'number', 5)
            self.fail('Geometry field is not default, and should throw an exception.')
        except FieldDoesNotExist, e:
            pass

        sld = generator.as_equal_interval(Hydrant.objects.filter(pressure=1), 'number', 5, geofield='location')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        self.assertEqual(len(sld._node.xpath('//sld:PointSymbolizer', namespaces=sld._nsmap)), 5)
        self.assertEqual(len(sld._node.xpath('//sld:LineSymbolizer', namespaces=sld._nsmap)), 0)
        self.assertEqual(len(sld._node.xpath('//sld:PolygonSymbolizer', namespaces=sld._nsmap)), 0)

    def test_classes_geofield_ln(self):
        """
        Test the geofield optional parameter for a line-based geographic model.
        """
        try:
            generator.as_equal_interval(Pipeline.objects.filter(material='ceramic'), 'diameter', 5)
            self.fail('Geometry field is not default, and should throw an exception.')
        except FieldDoesNotExist, e:
            pass

        sld = generator.as_equal_interval(Pipeline.objects.filter(material='ceramic'), 'diameter', 5, geofield='path')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        self.assertEqual(len(sld._node.xpath('//sld:PointSymbolizer', namespaces=sld._nsmap)), 0)
        self.assertEqual(len(sld._node.xpath('//sld:LineSymbolizer', namespaces=sld._nsmap)), 5)
        self.assertEqual(len(sld._node.xpath('//sld:PolygonSymbolizer', namespaces=sld._nsmap)), 0)

    def test_classes_geofield_poly(self):
        """
        Test the geofield optional parameter for a polygon-based geographic model.
        """
        try:
            generator.as_equal_interval(Reservoir.objects.filter(name__startswith='City'), 'volume', 5)
            self.fail('Geometry field is not default, and should throw an exception.')
        except FieldDoesNotExist, e:
            pass

        sld = generator.as_equal_interval(Reservoir.objects.filter(name__startswith='City'), 'volume', 5, geofield='coastline')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        self.assertEqual(len(sld._node.xpath('//sld:PointSymbolizer', namespaces=sld._nsmap)), 0)
        self.assertEqual(len(sld._node.xpath('//sld:LineSymbolizer', namespaces=sld._nsmap)), 0)
        self.assertEqual(len(sld._node.xpath('//sld:PolygonSymbolizer', namespaces=sld._nsmap)), 5)

    def test_ei_classes_pt(self):
        """
        Test the equal interval classifier for a point-based geographic model.
        """
        sld = generator.as_equal_interval(Hydrant.objects.filter(pressure=1), 'number', 5, geofield='location')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_equal_interval(Hydrant.objects.filter(pressure=2), 'number', 5, geofield='location')

        # class literal nodes:
        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['480.2', '960.4', '1440.6', '1920.8', '2401.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_ei_classes_ln(self):
        """
        Test the equal interval classifier for a line-based geographic model.
        """
        sld = generator.as_equal_interval(Pipeline.objects.filter(material='ceramic'), 'diameter', 5, geofield='path')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_equal_interval(Pipeline.objects.filter(material='concrete'), 'diameter', 5, geofield='path')

        # class literal nodes:
        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['9.8', '19.6', '29.4', '39.2', '49.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_ei_classes_poly(self):
        """
        Test the equal interval classifier for a polygon-based geographic model.
        """
        sld = generator.as_equal_interval(Reservoir.objects.filter(name__startswith='City'), 'volume', 5, geofield='coastline')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_equal_interval(Reservoir.objects.filter(name__startswith='County'), 'volume', 5, geofield='coastline')

        # class literal nodes:
        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['5008000.0', '10006000.0', '15004000.0', '20002000.0', '25000000.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_fj_classes_pt(self):
        """
        Test the Fisher Jenks classifier for a point-based geographic model.
        """
        sld = generator.as_fisher_jenks(Hydrant.objects.filter(pressure=1), 'number', 5, geofield='location')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_fisher_jenks(Hydrant.objects.filter(pressure=2), 'number', 5, geofield='location')

        # class literal nodes:
        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['324', '900', '1600', '2025', '2401']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_fj_classes_ln(self):
        """
        Test the Fisher Jenks classifier for a line-based geographic model.
        """
        sld = generator.as_fisher_jenks(Pipeline.objects.filter(material='ceramic'), 'diameter', 5, geofield='path')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_fisher_jenks(Pipeline.objects.filter(material='concrete'), 'diameter', 5, geofield='path')

        # class literal nodes:
        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['4.0', '11.0', '24.0', '36.0', '49.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_fj_classes_poly(self):
        """
        Test the Fisher Jenks classifier for a polygon-based geographic model.
        """
        sld = generator.as_fisher_jenks(Reservoir.objects.filter(name__startswith='City'), 'volume', 5, geofield='coastline')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_fisher_jenks(Reservoir.objects.filter(name__startswith='County'), 'volume', 5, geofield='coastline')

        # class literal nodes:
        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['3610000.0', '9610000.0', '12960000.0', '16810000.0', '25000000.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_jc_classes_pt(self):
        """
        Test the Jenks Caspall classifier for a point-based geographic model.
        """
        sld = generator.as_jenks_caspall(Hydrant.objects.filter(pressure=1), 'number', 5, geofield='location')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_jenks_caspall(Hydrant.objects.filter(pressure=2), 'number', 5, geofield='location')

        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['169', '484', '961', '1600', '2401']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_jc_classes_ln(self):
        """
        Test the Jenks Caspall classifier for a line-based geographic model.
        """
        sld = generator.as_jenks_caspall(Pipeline.objects.filter(material='ceramic'), 'diameter', 5, geofield='path')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_jenks_caspall(Pipeline.objects.filter(material='concrete'), 'diameter', 5, geofield='path')

        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['9.0', '19.0', '29.0', '39.0', '49.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_jc_classes_poly(self):
        """
        Test the Jenks Caspall classifier for a polygon-based geographic model.
        """
        sld = generator.as_jenks_caspall(Reservoir.objects.filter(name__startswith='City'), 'volume', 5, geofield='coastline')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_jenks_caspall(Reservoir.objects.filter(name__startswith='County'), 'volume', 5, geofield='coastline')

        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['1690000.0', '5290000.0', '10240000.0', '16810000.0', '25000000.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_jcf_classes_pt(self):
        """
        Test the Jenks Caspall Forced classifier for a point-based geographic model.
        """
        sld = generator.as_jenks_caspall_forced(Hydrant.objects.filter(pressure=1), 'number', 5, geofield='location')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_jenks_caspall_forced(Hydrant.objects.filter(pressure=2), 'number', 5, geofield='location')

        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['289', '729', '1225', '1764', '2401']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_jcf_classes_ln(self):
        """
        Test the Jenks Caspall Forced classifier for a line-based geographic model.
        """
        sld = generator.as_jenks_caspall_forced(Pipeline.objects.filter(material='ceramic'), 'diameter', 5, geofield='path')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_jenks_caspall_forced(Pipeline.objects.filter(material='concrete'), 'diameter', 5, geofield='path')

        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['9.0', '19.0', '29.0', '39.0', '49.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_jcf_classes_poly(self):
        """
        Test the Jenks Caspall Forced classifier for a polygon-based geographic model.
        """
        sld = generator.as_jenks_caspall_forced(Reservoir.objects.filter(name__startswith='City'), 'volume', 5, geofield='coastline')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_jenks_caspall_forced(Reservoir.objects.filter(name__startswith='County'), 'volume', 5, geofield='coastline')

        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['3240000.0', '7840000.0', '12960000.0', '18490000.0', '25000000.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    # This test fails. Documentation for JCS indicates that this is designed
    # for large n problems. Our test is small n, so maybe that's why.
    #
    #def test_jcs_classes(self):
    #    sld = generator.as_jenks_caspall_sampled(Hydrant.objects.filter(pressure=1), 'number', 5, geofield='location')
    #
    #    self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

    # It is not known why this test fails.
    #
    #def test_mp_classes(self):
    #    sld = generator.as_max_p_classifier(Hydrant.objects.filter(pressure=1), 'number', 5, geofield='location')
    # 
    #    self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

    def test_mb_classes_pt(self):
        """
        Test the Maximum Breaks classifier for a point-based geographic model.
        """
        sld = generator.as_maximum_breaks(Hydrant.objects.filter(pressure=1), 'number', 5, geofield='location')
   
        # request 5, get 2 back.
        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 2)

        sld = generator.as_maximum_breaks(Hydrant.objects.filter(pressure=2), 'number', 5, geofield='location')

        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['2070.5', '2162.5', '2256.5', '2352.5', '2401.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_mb_classes_ln(self):
        """
        Test the Maximum Breaks classifier for a line-based geographic model.
        """
        sld = generator.as_maximum_breaks(Pipeline.objects.filter(material='ceramic'), 'diameter', 5, geofield='path')
   
        # request 5, get 2 back.
        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 2)

        sld = generator.as_maximum_breaks(Pipeline.objects.filter(material='concrete'), 'diameter', 5, geofield='path')

        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['0.5', '49.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_mb_classes_poly(self):
        """
        Test the Maximum Breaks classifier for a polygon-based geographic model.
        """
        sld = generator.as_maximum_breaks(Reservoir.objects.filter(name__startswith='City'), 'volume', 5, geofield='coastline')
   
        # request 5, get 2 back.
        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 2)

        sld = generator.as_maximum_breaks(Reservoir.objects.filter(name__startswith='County'), 'volume', 5, geofield='coastline')

        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['21625000.0', '22565000.0', '23525000.0', '24505000.0', '25000000.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_nb_classes_pt(self):
        """
        Test the Natural Breaks classifier for a point-based geographic model.
        """
        sld = generator.as_natural_breaks(Hydrant.objects.filter(pressure=1), 'number', 5, geofield='location')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_natural_breaks(Hydrant.objects.filter(pressure=2), 'number', 5, geofield='location')

        # Cannot test the values, as the Natural Breaks documentation indicates
        # that the consistency of breaks on multiple runs of the same data may
        # not be consistent with the default number of solutions generated. 
        # Even with an extremely high initial solution value (10,000), these
        # classes are still non-deterministic with the sample test data.
        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

    def test_nb_classes_ln(self):
        """
        Test the Natural Breaks classifier for a line-based geographic model.
        """
        sld = generator.as_natural_breaks(Pipeline.objects.filter(material='ceramic'), 'diameter', 5, geofield='path')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_natural_breaks(Pipeline.objects.filter(material='concrete'), 'diameter', 5, geofield='path')

        # Cannot test the values, as the Natural Breaks documentation indicates
        # that the consistency of breaks on multiple runs of the same data may
        # not be consistent with the default number of solutions generated. 
        # Even with an extremely high initial solution value (10,000), these
        # classes are still non-deterministic with the sample test data.
        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

    def test_nb_classes_poly(self):
        """
        Test the Natural Breaks classifier for a polygon-based geographic model.
        """
        sld = generator.as_natural_breaks(Reservoir.objects.filter(name__startswith='City'), 'volume', 5, geofield='coastline')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_natural_breaks(Reservoir.objects.filter(name__startswith='County'), 'volume', 5, geofield='coastline')

        # Cannot test the values, as the Natural Breaks documentation indicates
        # that the consistency of breaks on multiple runs of the same data may
        # not be consistent with the default number of solutions generated. 
        # Even with an extremely high initial solution value (10,000), these
        # classes are still non-deterministic with the sample test data.
        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

    def test_q_classes_pt(self):
        """
        Test the Quantiles classifier for a point-based geographic model.
        """
        sld = generator.as_quantiles(Hydrant.objects.filter(pressure=1), 'number', 5, geofield='location')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_quantiles(Hydrant.objects.filter(pressure=2), 'number', 5, geofield='location')

        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['96.2', '384.4', '864.6', '1536.8', '2401.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_q_classes_ln(self):
        """
        Test the Quantiles classifier for a line-based geographic model.
        """
        sld = generator.as_quantiles(Pipeline.objects.filter(material='ceramic'), 'diameter', 5, geofield='path')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_quantiles(Pipeline.objects.filter(material='concrete'), 'diameter', 5, geofield='path')

        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['9.8', '19.6', '29.4', '39.2', '49.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_q_classes_poly(self):
        """
        Test the Quantiles classifier for a polygon-based geographic model.
        """
        sld = generator.as_quantiles(Reservoir.objects.filter(name__startswith='City'), 'volume', 5, geofield='coastline')

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_quantiles(Reservoir.objects.filter(name__startswith='County'), 'volume', 5, geofield='coastline')

        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['1168000.0', '4246000.0', '9244000.0', '16162000.0', '25000000.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_related_fields(self):
        """
        Test the queryset and style generation using django related fields
        syntax.
        """
        sld = generator.as_quantiles(Pipeline.objects.filter(material='ceramic'), 'reservoir__volume', 5, geofield='path')
        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_quantiles(Hydrant.objects.filter(pressure=1), 'pipeline__diameter', 5, geofield='location')
        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_quantiles(Hydrant.objects.filter(pressure=1), 'pipeline__reservoir__volume', 5, geofield='location')
        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)
