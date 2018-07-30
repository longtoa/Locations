class Location:
    """A location class that will serve as a template for origins and destinations"""
    def __init__(self, postcode=None, address=None, geo=None):

        if not postcode and not address:
                raise TypeError('Either a postcode or an address should be provided')
        self.postcode = postcode
        self.address = address
        self.geo = geo
        self.times = {'fastest',
                      'public transport',
                      'car'}
        self.impact_time = {'fastest',
                            'public transport',
                            'car'}
        self.mode = 'fastest'

    @property
    def geo(self):
        return self.geo

    @geo.setter
    def geo(self, value):
        """geo should be set by passing a dict with keys 'lat', 'lng'"""
        if not isinstance(value, dict):
            raise TypeError("geo should be set by passing a dict got {} instead".format(value.__class__.__name__))

        try:
            lat = value['lat']
            lng = value['lng']
        except KeyError:
            raise KeyError("geo should be set by passing a dict with keys 'lat', 'lng'")

    def lat(self):
        return self.geo['lat']

    def lng(self):
        return self.geo['lng']

    @property
    def mode(self):
        return self.mode

    @mode.setter
    def mode(self, value):
        if value not in self.times:
            raise TypeError('Type should be either: fastest, public transport or car not '+value)
        self.mode = value


class Origin(Location):
    """Takes in address/postcode or/and geo-codes. The relation with a destination only exists through the times dict.
    the destination objects are used as keys for the times"""
    def __init__(self, postcode=None, address=None, geo=None):
        super().__init__(postcode, address, geo)
        self.current_destination = None
        self.times = {'fastest': {},
                      'public transport': {},
                      'car': {}}
        self.impact_time = {'fastest': {},
                            'public transport': {},
                            'car': {}}

    def get_times(self, mode='fastest', destination=None):
        """Not using a property here because args should be accepted."""
        if destination:
            times = self.times[mode][destination]
        else:
            times = [time for time in self.times[mode].items()]
        return times

    def set_times(self, mode, value, destination):
        if mode not in self.times:
            raise TypeError('Mode should be either: fastest, public transport or car not '+mode)

        if not isinstance(value, int):
            raise TypeError('value represents minutes and should be an integer. got '+value.__class__.__name__)

        if not isinstance(destination, Destination):
            raise TypeError('destination should be of class Destination. got ' + value.__class__.__name__)

        self.times[mode][destination] = value
        destination.set_times(value, mode)

    @property
    def times(self):
        """Not using a property here because args should be accepted."""
        return [time for time in self.times[self.mode].items()]

    @times.setter
    def times(self, value):
        raise AttributeError('Times should be set using the set_times method')

    @property
    def current_destination(self):
        return self.current_destination

    @current_destination.setter
    def current_destination(self, value):
        if not isinstance(value, Destination):
            raise TypeError('Current_destination should be of the class Destination got '+ value.__class__.__name__)

        if not all(value in d for d in self.times.values()):
            raise TypeError('You can only set a destination as this origins current destination if all times '
                            '("fastest", "public transport", "car") are calculated for this destination.')

        self.current_destination = value

        for mode, dict in self.times.items():
            for dest, time in dict.items():
                impact = time - dict[value]
                self.impact_time[mode][dest] = impact
                value.set_impact(mode, impact)


class Destination(Location):
    """The relation with origins is ket within the origin objects. Destination objects only keep times, not a
    reference to the origin."""

    def __init__(self, address=None, postcode=None, geo=None):
        super().__init__(address, postcode, geo)
        self.times = {'fastest': [],
                      'public transport': [],
                      'car': []}

    @property
    def times(self):
        """Not using a property here because args should be accepted."""
        return [time for time in self.times[self.mode].items()]

    @times.setter
    def times(self, value):
        raise AttributeError('Times should be set using the set_times method')

    def set_times(self, mode, time):
        if mode not in self.times:
            raise TypeError('Mode should be either: fastest, public transport or car not ' + mode)
        if not isinstance(time, int):
            raise TypeError('value represents minutes and should be an integer. got ' + value.__class__.__name__)

        self.times[mode].append(time)

    def set_impact(self, mode, impact):
        if mode not in self.times:
            raise TypeError('Mode should be either: fastest, public transport or car not ' + mode)
        if not isinstance(impact, int):
            raise TypeError('value represents minutes and should be an integer. got ' + value.__class__.__name__)

        self.impact_time[mode].append(impact)

    def avg_time(self):
        """Mode is provided through the object (Destination.mode), not the method. To avoid having
        to check whether the right mode is passed or not."""
        return sum(self.times[self.mode])/len(self.times[self.mode])

    def avg_impact(self):
        """Mode is provided through the object (Destination.mode), not the method. To avoid having
        to check whether the right mode is passed or not."""
        return sum(self.impact_time[self.mode])/len(self.impact_time[self.mode])
