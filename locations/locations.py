class Location:
    """A Location is a class that holds location information (obviously). That information is address, postcode,
    geo codes and information around travel times to other locations."""

    def __init__(self, postcode=None, address=None, geo=None):
        if not postcode and not address:
                raise TypeError('Either a postcode or an address should be provided')
        self.postcode = postcode
        self.address = address
        self.geo = geo
        self._geo = None
        self.modes = {'fastest', 'public transport', 'car'}
        self._mode = None
        self._times = {mode: {} for mode in self.modes}
        self._impact_times = {mode: {} for mode in self.modes}

    @property
    def geo(self):
        return self._geo

    @geo.setter
    def geo(self, value):
        """geo should be set by passing a dict with keys 'lat', 'lng'"""
        if value is None:
            return

        if not isinstance(value, dict):
            raise TypeError("geo should be set by passing a dict got {} instead".format(value.__class__.__name__))

        try:
            lat = value['lat']
            lng = value['lng']
        except KeyError:
            raise KeyError("geo should be set by passing a dict with keys 'lat', 'lng'")

        self._geo = {'lat': lat,
                     'lng': lng}

    def lat(self):
        return self.geo['lat']

    def lng(self):
        return self.geo['lng']

    @property
    def times(self):
        return self.get_times()

    @times.setter
    def times(self, value):
        raise AttributeError('Times should be set using the set_times method')

    @property
    def impact_times(self):
        """Not using a property here because args should be accepted."""
        return self.get_impacts()

    @impact_times.setter
    def impact_times(self, value):
        raise AttributeError('Impact should be set using the set_impacts method')

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if value not in self.modes:
            raise TypeError('Type should be either: fastest, public transport or car not '+value)
        self._mode = value

    def check_params(self, mode, value, location):
        """The base function that checks if the parameters that are going to be set are valid inputs."""
        if mode not in self.modes:
            raise TypeError('Mode should be either: fastest, public transport or car not ' + mode)
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError('value represents minutes and should be an integer. got ' + value.__class__.__name__)
        if not isinstance(location, Location) or location == self:
            raise TypeError('destination should be of class Location. got ' + value.__class__.__name__)

    def set_times(self, mode, value, to_location, mirror=True):
        """The mirror boolean is used to identify from where the function was called. It is needed to prevent locations
        from calling each other infinetly."""

        self.check_params(mode, value, to_location)
        self._times[mode][to_location] = value
        if mirror:
            to_location.set_times(mode, value, self, mirror=False)

    def set_impacts(self, mode, value, to_location, mirror=True):
        """The mirror boolean is used to identify from where the function was called. It is needed to prevent locations
        from calling each other infinetly."""

        self.check_params(mode, value, to_location)
        self._impact_times[mode][to_location] = value
        if mirror:
            to_location.set_impacts(mode, value, self, mirror=False)

    def attribute_getter(fn):
        def wrapped(self, mode=None, to_location=None):
            mode = self._mode if mode is None else mode
            if to_location:
                resp = fn(self)[mode][to_location]
            else:
                resp = [value for value in fn(self)[mode].values()]
            return resp
        return wrapped

    @attribute_getter
    def get_times(self):
        return self._times

    @attribute_getter
    def get_impacts(self):
        return self._impact_times


class Origin(Location):
    """Takes in address/postcode or/and geo-codes. The relation with a destination only exists through the times dict.
    the destination objects are used as keys for the times"""
    def __init__(self, postcode=None, address=None, geo=None):
        super().__init__(postcode, address, geo)
        self._current_destination = None

    @property
    def current_destination(self):
        return self.current_destination

    @current_destination.setter
    def current_destination(self, destination):
        if not isinstance(destination, Destination):
            raise TypeError('Current_destination should be of the class Destination got ' + value.__class__.__name__)

        if not all(destination in d for d in self.times.values()):
            raise TypeError('You can only set a destination as this origins current destination if all times '
                            '("fastest", "public transport", "car") are calculated for this destination.')

        self._current_destination = destination

        for mode, dict in self.times.items():
            for dest, time in dict.items():
                impact = time - dict[destination]
                self._impact_times[mode][dest] = impact
                destination.set_impacts(mode, impact, self)


class Destination(Location):
    """The relation with origins is ket within the origin objects. Destination objects only keep times, not a
    reference to the origin."""

    def __init__(self, address=None, postcode=None, geo=None):
        super().__init__(address, postcode, geo)

    def check_mode(self, mode):
        if mode is None:
            return self._mode

        if mode not in self.modes:
            raise TypeError
        else:
            return mode

    def avg_time(self, mode=None):
        mode = self.check_mode(mode)
        return sum(self._times[mode].values())/len(self._times[mode])

    def avg_impact(self, mode=None):
        mode = self.check_mode(mode)
        return sum(self._impact_times[mode].values())/len(self._impact_times[mode])
