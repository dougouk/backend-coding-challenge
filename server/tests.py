import algorithm
import app
import city
import unittest

class Test_Lat_Long_Distance_Calculation(unittest.TestCase):
    
    def test_origin_pair(self):
        pair_1 = [0, 0]
        pair_2 = [0, 0]
        self.assertEqual(algorithm.lat_long_d(pair_1[0], pair_1[1], pair_2[0], pair_2[1]), 0)

    def test_lat_long_d(self):
        pair_1 = [44.5544837, -78.7165327]
        pair_2 = [45.5016889, -73.567256]
        self.assertEqual(418, int(algorithm.lat_long_d(pair_1[0], pair_1[1], pair_2[0], pair_2[1])))

class Test_Edit_Distance(unittest.TestCase):
    def test_exponential_polynomial(self):
        result = algorithm.edge_d('exponential', 'polynomial')
        self.assertEqual(result[-1][-1], 6)

    def test_empty(self):
        result = algorithm.edge_d('Montreal', '')
        self.assertEqual(result, 8)

    def test_both_empty(self):
        result = algorithm.edge_d('', '')
        self.assertEqual(result, 0)

    def test_snow_know(self):
        result = algorithm.edge_d('Snow', 'Know')
        self.assertEqual(result[-1][-1], 1)

class Test_Confidence_Level(unittest.TestCase):
    def test_0_edit(self):
        c = city.City('Montreal', None, None)
        c.edit_distance = 0
        algorithm.calc_confidence_level(c, 'Montreal')
        self.assertEqual(c.confidence_level, 1)

    def test_0_edit_0_physical(self):
        c = city.City('Montreal', 0, 0)
        c.edit_distance = 0
        c.physical_distance = 0
        algorithm.calc_confidence_level(c, 'Montreal')
        self.assertEqual(c.confidence_level, 1)    

class Test_Database(unittest.TestCase):

    def test_database_rows(self):
        # Test that db has 7237 rows
        self.assertEqual(algorithm.rows_in_database(), 7237)

class Test_Search(unittest.TestCase):
    def test_londo(self):
        results = algorithm.search('londo', 43.70011, -79.4163)
        sorted_search = sorted(results, key=lambda x: x.confidence_level, reverse=True)
        first_city = sorted_search[0]
        self.assertEqual(first_city.name, 'London')
        self.assertEqual(first_city.confidence_level, 0.8362086332750764)

    def test_calgary(self):
        results = algorithm.search('Calgary', 51.012782, -114.3543368)
        sorted_search = sorted(results, key=lambda x: x.confidence_level, reverse=True)
        sorted_search
        first_city = sorted_search[0]
        self.assertEqual(first_city.name, 'Calgary')
        self.assertEqual(first_city.confidence_level, 0.9824211409812602)
        self.assertEqual(first_city.physical_distance, 19.272830905652228)

def main():
    unittest.main()

if __name__ == '__main__':
    main()