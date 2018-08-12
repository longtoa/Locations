import unittest
from chunker import Chunker


class TestChunker(unittest.TestCase):

    def test_even_chunk(self):
        lijst = [i for i in range(300)]
        lijst_chunker = Chunker(lijst)

        lijst50 = list(lijst_chunker(50))

        self.assertEqual(len(lijst50[0]), 50)
        self.assertEqual(lijst50[1][0], 50)
        self.assertEqual(len(lijst50), 6)
        self.assertEqual(lijst50[5][49], 299)


    def test_small_chunk(self):
        new_lijst = [i for i in range(20)]
        new_lijst_chunker = Chunker(new_lijst)

        new_lijst50 = list(new_lijst_chunker(50))

        self.assertEqual(len(new_lijst50), 1)
        self.assertEqual(new_lijst50[0][19], 19)

    def test_odd_chunk(self):
        lijst = [i for i in range(253)]
        lijst_chunker = Chunker(lijst)

        lijst47 = list(lijst_chunker(47))

        self.assertEqual(len(lijst47[0]), 47)
        self.assertEqual(lijst47[1][0], 47)
        self.assertEqual(len(lijst47), 6)
        self.assertEqual(lijst47[5][17], 252)

    def test_not_list_passed(self):

        with self.assertRaises(TypeError):
            dict = {'test': 15, 'test2': 16}
            Chunker(dict)


if __name__ == '__main__':
    unittest.main()