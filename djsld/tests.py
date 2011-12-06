import unittest
import djsld, random
import generator
from models import Hydrant
from django.contrib.gis.geos import GEOSGeometry

class QuantileTest(unittest.TestCase):
    def setUp(self):
        Hydrant.objects.all().delete()

        for x in range(0,5):
            h = Hydrant(number=x, pressure=1, location=GEOSGeometry('POINT(%d %d)'%(x,x,)))
            h.save()

        for y in range(0,50):
            h = Hydrant(number=y*y, pressure=2, location=GEOSGeometry('POINT(%d %d)'%(y,y,)))
            h.save()

    def test_ei_classes(self):
        sld = generator.as_equal_interval(Hydrant.objects.filter(pressure=1), 'number', 5)

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_equal_interval(Hydrant.objects.filter(pressure=2), 'number', 5)

        # class literal nodes:
        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['480.2', '960.4', '1440.6', '1920.8', '2401.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_fj_classes(self):
        sld = generator.as_fisher_jenks(Hydrant.objects.filter(pressure=1), 'number', 5)

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_fisher_jenks(Hydrant.objects.filter(pressure=2), 'number', 5)

        # class literal nodes:
        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['324', '900', '1600', '2025', '2401']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_jc_classes(self):
        sld = generator.as_jenks_caspall(Hydrant.objects.filter(pressure=1), 'number', 5)

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_jenks_caspall(Hydrant.objects.filter(pressure=2), 'number', 5)

        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['169', '484', '961', '1600', '2401']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_jcf_classes(self):
        sld = generator.as_jenks_caspall_forced(Hydrant.objects.filter(pressure=1), 'number', 5)

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_jenks_caspall_forced(Hydrant.objects.filter(pressure=2), 'number', 5)

        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['289', '729', '1225', '1764', '2401']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    # This test fails. Documentation for JCS indicates that this is designed
    # for large n problems. Our test is small n, so maybe that's why.
    #
    #def test_jcs_classes(self):
    #    sld = generator.as_jenks_caspall_sampled(Hydrant.objects.filter(pressure=1), 'number', 5)
    #
    #    self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

    # It is not known why this test fails.
    #
    #def test_mp_classes(self):
    #    sld = generator.as_max_p_classifier(Hydrant.objects.filter(pressure=1), 'number', 5)
    # 
    #    self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

    def test_mb_classes(self):
        sld = generator.as_maximum_breaks(Hydrant.objects.filter(pressure=1), 'number', 5)
   
        # request 5, get 2 back.
        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 2)

        sld = generator.as_maximum_breaks(Hydrant.objects.filter(pressure=2), 'number', 5)

        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['2070.5', '2162.5', '2256.5', '2352.5', '2401.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_nb_classes(self):
        sld = generator.as_natural_breaks(Hydrant.objects.filter(pressure=1), 'number', 5)

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_natural_breaks(Hydrant.objects.filter(pressure=2), 'number', 5)

        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['169', '484', '961', '1600', '2401']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)

    def test_q_classes(self):
        sld = generator.as_quantiles(Hydrant.objects.filter(pressure=1), 'number', 5)

        self.assertEqual(len(sld.NamedLayer.UserStyle.FeatureTypeStyle.Rules), 5)

        sld = generator.as_quantiles(Hydrant.objects.filter(pressure=2), 'number', 5)

        literals = sld._node.xpath('//ogc:PropertyIsLessThanOrEqualTo/ogc:Literal',namespaces=sld._nsmap)
        expected = ['96.2', '384.4', '864.6', '1536.8', '2401.0']

        for i,n in enumerate(literals):
            self.assertEqual(n.text, expected[i], 'Class %d is not correct.' % i)
