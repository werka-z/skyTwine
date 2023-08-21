import unittest
from weather.services import fetch_openweather_data, fetch_weatherapi_data


class FetchDataSets(unittest.TestCase):
    def setUp(self):
        self.city_1 = "Krakow"
        self.city_2 = "Cracow"

    def test_fetch_weatherapi_data(self):
        data = fetch_weatherapi_data(self.city_2)
        print("weatherapi:")
        print(data)
        self.assertNotIn('error', data)

    def test_fetch_openweather_data(self):
        data = fetch_openweather_data(self.city_1)
        # print("openweather:")
        print(data)
        self.assertNotIn('error', data)


if __name__ == '__main__':
    unittest.main()
