import unittest
from locations import Location, Origin, Destination


class TestLocation(unittest.TestCase):

    def setUp(self):
        self.location1 = Location(postcode='EC4M 8AD',
                                  address="St. Paul's Churchyard, London",
                                  geo={'lat': 51.513723, 'lng': -0.099858})
        self.location2 = Location(postcode='EC4M 8AD',
                                  address="St. Paul's Churchyard, London",
                                  geo={'lat': 51.513723, 'lng': -0.099858})
        self.location3 = Location(postcode='EC4M 8AD',
                                  address="St. Paul's Churchyard, London",
                                  geo={'lat': 51.513723, 'lng': -0.099858})

    def test_check_params(self):
        with self.assertRaises(TypeError):
            self.location1.set_times(mode='strongest', value=15, to_location=self.location2)
        with self.assertRaises(TypeError):
            self.location1.set_impacts(mode='fastest', value='15.8', to_location=self.location2)
        with self.assertRaises(TypeError):
            self.location1.set_times(mode='fastest', value=15, to_location='dest')
        with self.assertRaises(TypeError):
            self.location1.set_impacts(mode='fastest', value=15, to_location=self.location1)
        with self.assertRaises(AttributeError):
            self.location1.times = 15

    def test_times(self):
        self.location1.set_times(mode='fastest', value=15, to_location=self.location2)
        self.location1.set_times(mode='fastest', value=30.0, to_location=self.location3)
        self.location1.set_times('fastest', 18, self.location2)  # Should overwrite the previous 15

        self.assertEqual(self.location1.times, [18, 30.0])
        self.assertEqual(self.location1.get_times(), [18, 30.0])
        self.assertEqual(self.location1.get_times(to_location=self.location2), 18)
        self.assertEqual(self.location1.get_times(to_location=self.location3), 30.0)
        self.assertEqual(self.location2.get_times(to_location=self.location1), 18)

    def test_impact_times(self):
        self.location1.set_impacts(mode='fastest', value=5, to_location=self.location2)
        self.location1.set_impacts(mode='fastest', value=-5, to_location=self.location3)
        self.location1.set_impacts('fastest', 8, self.location2)  # Should overwrite the previous 15

        self.assertEqual(self.location1.impact_times, [8, -5])
        self.assertEqual(self.location1.get_impacts(), [8, -5])
        self.assertEqual(self.location1.get_impacts(to_location=self.location2), 8)
        self.assertEqual(self.location1.get_impacts(to_location=self.location3), -5)
        self.assertEqual(self.location2.get_impacts(to_location=self.location1), 8)

    def test_geo(self):
        with self.assertRaises(TypeError):
            self.location1.geo = 15

        with self.assertRaises(KeyError):
            self.location1.geo = {'lat': 5, 'lon': 5}

    def test_mode(self):
        self.location1.set_times('public transport', 15, self.location2)
        self.location1.set_times('car', 23, self.location2)
        self.location1.set_impacts('public transport', 8, self.location2)
        self.location1.set_impacts('car', 11, self.location2)

        with self.assertRaises(TypeError):
            self.location1.mode = 'test'

        self.assertEquals(self.location1.times, [])
        with self.assertRaises(KeyError):
            self.location1.get_times(to_location=self.location2)

        self.location1.mode = 'car'
        self.assertEquals(self.location1.get_times(to_location=self.location2), 23)
        self.assertEquals(self.location1.get_impacts(to_location=self.location2), 11)

        self.location1.mode = 'public transport'
        self.assertEquals(self.location1.get_times(to_location=self.location2), 15)
        self.assertEquals(self.location1.get_impacts(to_location=self.location2), 8)


class TestOrigin(unittest.TestCase):
    def setUp(self):
        self.origin = Origin(postcode='EC4M 8AD',
                             address="St. Paul's Churchyard, London",
                             geo={'lat': 51.513723, 'lng': -0.099858})
        self.destination1 = Destination(postcode='EC4M 8AD',
                                        address="St. Paul's Churchyard, London",
                                        geo={'lat': 51.513723, 'lng': -0.099858})
        self.destination2 = Destination(postcode='EC4M 8AD',
                                        address="St. Paul's Churchyard, London",
                                        geo={'lat': 51.513723, 'lng': -0.099858})

    def test_times(self):
        self.origin.set_times(mode='fastest', value=15, to_location=self.destination1)
        self.origin.set_times(mode='fastest', value=30.0, to_location=self.destination2)

        self.assertEqual(self.origin.times, [15, 30.0])
        self.assertEqual(self.origin.get_times(), [15, 30.0])
        self.assertEqual(self.origin.get_times(to_location=self.destination1), 15)
        self.assertEqual(self.origin.get_times(to_location=self.destination2), 30.0)

    def test_impact(self):
        self.origin.set_impacts(mode='fastest', value=-5, to_location=self.destination1)
        self.origin.set_impacts(mode='fastest', value=5, to_location=self.destination2)

        self.assertEqual(self.origin.get_impacts(), [-5, 5])
        self.assertEqual(self.origin.get_impacts(to_location=self.destination1), -5)
        self.assertEqual(self.origin.get_impacts(to_location=self.destination2), 5)

    def test_current_destination(self):
        self.origin.set_times(mode='fastest', value=30, to_location=self.destination1)
        self.origin.set_times(mode='fastest', value=25, to_location=self.destination2)

        with self.assertRaises(TypeError):
            self.origin.current_destination = self.destination1

        self.origin.set_times(mode='car', value=30, to_location=self.destination1)

        with self.assertRaises(TypeError):
            self.origin.current_destination = self.destination1

        self.origin.set_times(mode='public transport', value=45, to_location=self.destination1)

        self.origin.current_destination = self.destination1
        self.assertEqual(self.origin.current_destination, self.destination1)
        self.assertEqual(self.origin.get_impacts(to_location=self.destination2, mode='fastest'), 5)
        self.assertEquals(self.destination2.get_impacts(to_location=self.origin, mode='fastest'), 5)


class TestDestination(unittest.TestCase):

    def setUp(self):
        self.destination = Destination(postcode='EC4M 8AD',
                                       address="St. Paul's Churchyard, London",
                                       geo={'lat': 51.513723, 'lng': -0.099858})
        self.origin1 = Origin(postcode='EC4M 8AD',
                              address="St. Paul's Churchyard, London",
                              geo={'lat': 51.513723, 'lng': -0.099858})
        self.origin2 = Origin(postcode='EC4M 8AD',
                              address="St. Paul's Churchyard, London",
                              geo={'lat': 51.513723, 'lng': -0.099858})

        self.origin1.set_times(mode='car', value=30, to_location=self.destination)
        self.destination.set_times(mode='car', value=25, to_location=self.origin2)
        self.destination.set_impacts(mode='car', value=10, to_location=self.origin1)
        self.origin2.set_impacts(mode='car', value=5, to_location=self.destination)

    def test_times(self):
        self.destination.mode = 'car'
        self.assertEqual(self.destination.times, [30, 25])

    def test_impact(self):
        self.destination.mode = 'car'
        self.assertEqual(self.destination.impact_times, [10, 5])

    def test_avg_time(self):
        self.assertEquals(self.destination.avg_time(), 27.5)

    def test_avg_impact(self):
        self.assertEquals(self.destination.avg_impact(), 7.5)


if __name__ == '__main__':
    unittest.main()
