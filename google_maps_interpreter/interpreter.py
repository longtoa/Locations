import googlemaps
import time
from ..chunker import Chunker


class GoogleInterpreter(googlemaps.Client):
    """This class simply decorates the Python client for Google Maps API Services which can be found
    here: https://github.com/googlemaps/google-maps-services-python. This class processes the raw return values from
    the client in a more user friendly manner."""

    def geocode(self, origins, *args, **kwargs):
        """Takes a list of addresses and returns a dict, using the address as key and the geo coordinates in a dict as
        value: {address: {'geo': {'lat':x, 'lng':y}, 'place_id': place_id}}"""
        if isinstance(origins, str):
            raw_result = super().geocode(origins, *args, **kwargs)
            if len(raw_result) == 0:
                raise ValueError("{} not found".format(origins))
            result = {origins: {'geo': raw_result[0]['geometry']['location'], 'place_id': raw_result[0]['place_id']}}
            return result

        chunker = Chunker(origins)
        chunked_origins = chunker.get_chunks(50)  # Need to chunk to not exceed Google's QPS limit of 50.
        result = {}

        for n, chunk in enumerate(chunked_origins):
            raw_result = super().geocode(chunk, *args, **kwargs)
            temp_result = {chunk[i]: {'geo': raw_result[i]['geometry']['location'],
                                      'place_id': raw_result[i]['place_id']}
                           for i in chunk}

            if len(temp_result) < chunk:  # python client simply throws not found errors out.
                raise ValueError("Origin not found in between element {} and {}".format(n*50, n*50 + 50))

            result = {**result, **temp_result}
            time.sleep(1)

        return result

    def reverse_geocode(self, origins, *args, **kwargs):
        """Takes a dict of geocode parameters and returns the address. Multiple geocodes not yet implemented."""
        pass

    def dist_matrix(self, origins, destinations, *args, **kwargs):
        """Takes a list of origins and destinations and a set of parameters (please check the Python client for
        Google maps API to get more info on the parameters) and returns a nested dictionary storing the origin as key
        with another dict as value which in turn has each destination as key with another dict as value storing both
        time to travel and distance between the two. e.g. {origin: {destination: {'time':x, 'dist':y}, dest2...},
        origin2...}"""

        if destinations > 25:
            raise ValueError("Can't calculate to more than 25 destinations at a time")

        origin_chunk_size = 100//len(destinations) if len(destinations) < 4 else 25
        chunker = Chunker(origins)
        chunked_origins = chunker.get_chunks(origin_chunk_size)

        result = {}
        for chunk in chunked_origins:
            raw_result = super().distance_matrix(chunk, destinations, *args, **kwargs)
            for i, dest in enumerate(raw_result['rows']):
                result[chunk[i]] = {destinations[n]: {'dist': dest['elements'][n]['distance']['value'],
                                                      'time': dest['elements'][n]['times']['value']}
                                    for n in dest['elements']}

        return result
