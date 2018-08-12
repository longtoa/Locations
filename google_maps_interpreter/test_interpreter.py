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
        # Check if works for single value passed through
        geo_dict = self.interpreter.geocode(self.address1)
        check_geo_dict = {self.address1: self.geocode1}
        self.assertEqual(geo_dict, check_geo_dict)

        with self.assertRaises(ValueError):
            self.interpreter.geocode('bhskyf')

        # Check if works for multiple items sent through
        geo_dict = self.interpreter.geocode(self.address1, self.address2)
        check_geo_dict = {self.address1: self.geocode1, self.address2: self.geocode2}
        self.assertEqual(geo_dict, check_geo_dict)

        # Check if still returns list when only one value has been passed through.
        geo_dict = self.interpreter.geocode(self.address1, 'bhskyf')
        check_geo_dict = {self.address1: self.geocode1, 'bhskyf': 'NA'}
        self.assertEqual(geo_dict, check_geo_dict)

    def test_reverse_geocode(self):
        self.assertEqual(self.interpreter.reverse_geocode(self.geocode1), self.address1)
        self.assertEqual(self.interpreter.reverse_geocode(self.geocode2), self.address2)

        with self.assertRaises(ValueError):
            self.interpreter.reverse_geocode('hbhd')

        with self.assertRaises(KeyError):
            self.interpreter.reverse_geocode({'lat': 115, 'lon': 158})

    def test_distance(self):
        dist_dict = self.interpreter.dist_matrix(self.address1, self.address2)
        check_dist_dict = {self.address1: {self.address2: {'time': 1543, 'distance': 6833}}}
        self.assertEqual(dist_dict, check_dist_dict)

        origins = ["Carrer de Mallorca, 401, 08013 Barcelona, Catalunya",
                   "Carrer d'Olot, 08024 Barcelona, Catalunya",
                   "Passeig de Lluís Companys, 08003 Barcelona, Catalunya",
                   "C/ Palau de la Música, 4-6, 08003 Barcelona, Catalunya"]

        destinations = ["Plaça de Catalunya, 08002 Barcelona, Catalunya",
                        self.address1,
                        self.address2]

        check_dist_dict = {
            "Carrer de Mallorca, 401, 08013 Barcelona, Catalunya":
                {"Plaça de Catalunya, 08002 Barcelona, Catalunya": {'time': 595, 'dist': 3079},
                 self.address1: {'time': 1339, 'dist': 7343},
                 self.address2: {'time': 907, 'dist': 3907}},
            "Carrer d'Olot, 08024 Barcelona, Catalunya":
                {"Plaça de Catalunya, 08002 Barcelona, Catalunya": {'time': 1078, 'dist': 5404},
                 self.address1: {'time': 1083, 'dist': 6107},
                 self.address2: {'time': 1390, 'dist': 6232}},
            "Passeig de Lluís Companys, 08003 Barcelona, Catalunya":
                {"Plaça de Catalunya, 08002 Barcelona, Catalunya": {'time': 322, 'dist': 1240},
                 self.address1: {'time': 1371, 'dist': 7021},
                 self.address2: {'time': 652, 'dist': 2068}},
            "C/ Palau de la Música, 4-6, 08003 Barcelona, Catalunya":
                {"Plaça de Catalunya, 08002 Barcelona, Catalunya": {'time': 228, 'dist': 776},
                 self.address1: {'time': 1280, 'dist': 6502},
                 self.address2: {'time': 355, 'dist': 867}},
        }

        self.assertEqual(self.interpreter.dist_matrix(origins, destinations), check_dist_dict)


if __name__ == '__main__':
    unittest.main()