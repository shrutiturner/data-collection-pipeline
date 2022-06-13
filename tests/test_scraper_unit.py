import sys
sys.path.append("..")

import unittest

from src.scraper import Scraper
from unittest.mock import patch, MagicMock

class ScraperTestCase(unittest.TestCase):
    
    def setUp(self) -> None:
        self.scraper = Scraper()


    @patch('urllib.request.urlretrieve')
    def test_download_image(self, mock_urlretrieve):
        mock_urlretrieve.return_value = MagicMock()

        self.scraper.get_image('test-image-path', 'test-image-url', 'test-image-name')

        mock_urlretrieve.assert_called_once_with('test-image-url', 'test-image-path/test-image-name')


    def tearDown(self) -> None:
        self.scraper.driver.close()

unittest.main(argv=[''], verbosity=0, exit=False)
