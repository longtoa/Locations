class Chunker:
    """Accepts a list to initialise the object. Used to return the list chopped in 'chunks' and returned in a list of
    lists."""

    def __init__(self, to_chunk_list):

        try:
            to_chunk_list[0:5]
        except (KeyError, TypeError):
            raise TypeError('{} object is not subscriptable'.format(to_chunk_list.__class__.__name__))

        self.list = to_chunk_list

    def __call__(self, size):
        """Takes a size as argument and returns a list of list with the inner list being the size passed as argument.
        All inner lists together form the original list."""

        chunks, last_chunk = len(self.list)//size, len(self.list)%size

        first_elem = 0
        for chunk in range(chunks):
            last_elem = first_elem + size
            yield self.list[first_elem:last_elem]
            first_elem = last_elem

        if last_chunk:
            last_elem = first_elem + last_chunk
            yield self.list[first_elem:last_elem]
