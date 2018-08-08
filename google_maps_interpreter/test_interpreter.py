import unittest
from interpreter import GoogleInterpreter


class TestGoogleInterpreter(unittest.TestCase):

    def setUp(self):
        self.interpreter = GoogleInterpreter(key=key)
        self.address1 = "C. d'Aristides Maillol, 12, 08028 Barcelona, Catalunya"
        self.geocode1 = {'lat': 41.3800475, 'lng': 2.1200696}
        self.address2 = "Plaça de Sant Miquel, 1, 08002 Barcelona, Catalunya"
        self.geocode2 = {'lat': 41.3822152, 'lng': 2.1769328}

    def test_geocode(self):
        self.assertEqual(self.interpreter.geocode(self.address1), self.geocode1)
        self.assertEqual(self.interpreter.geocode(self.address1), self.geocode2)

        with self.assertRaises(ValueError):
            self.interpreter.geocode('bhskyf')

        geo_list = self.interpreter.geocode(self.address1, self.address2)
        geo_reverse = self.interpreter.geocode(self.address2, self.address1)
        check_geo_list = [self.geocode1, self.geocode2]

        self.assertEqual(geo_list, check_geo_list)
        self.assertNotEqual(geo_list, geo_reverse)

    def test_reverse_geocode(self):
        self.fail()

    def test_distance(self):
        self.fail()