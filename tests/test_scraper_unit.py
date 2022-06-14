# import out unittest library 
from re import A
import unittest

# import sys to allow us to append the system path
import sys
from unittest import mock 
# append the parent folder
sys.path.append('../') 

from src.aws_port import AWS
from src.scraper import Scraper
from unittest.mock import ANY, patch, MagicMock, Mock

from sqlalchemy import create_engine


class ScraperTestCaseUnit(unittest.TestCase):
    
    def setUp(self) -> None:
        self.scraper = Scraper()
        # self.aws = AWS()


    @patch('boto3.client')
    @patch('urllib.request.urlretrieve')
    def test_get_image(self, mock_urlretrieve, mock_boto_client) -> None:
        mock_urlretrieve.return_value = MagicMock()

        # mock_client = MagicMock()
        # mock_client.upload_file.return_value = "test"
        # mock_s3.return_value = mock_client

        mock_boto_client.return_value = mock_boto_client
        mock_boto_client.upload_file.return_value = "test"

        actual = self.scraper.get_image('fundraiser_name', 'test-image-url', 'test-image-name')
        
        mock_urlretrieve.assert_called_once_with('test-image-url', '/tmp/test-image-name')
        
        # mock_boto_client.upload_file.assert_called_once_with('test-image-url', 'bucket-name', 'fundraiser_name/test-image-name')
        
        # self.assertEqual('s3://justgiving-scraper/fundraiser_name/test-image-name', image_url)

        self.assertEqual("test", actual)


    @patch('sqlalchemy.create_engine')
    @patch('pandas.DataFrame')
    def test_save_data(self, mock_df, mock_engine) -> None:
        mock_DataFrame = MagicMock()
        mock_DataFrame.to_sql.return_value = "test"
        mock_df.return_value = mock_DataFrame

        mock_engine.return_value = "engine"

        self.scraper.save_data({'key': 'value', 'key2': 'value2'})
        
        mock_df.assert_called_once_with({'key': 'value', 'key2': 'value2'}, index=[ANY])
        mock_DataFrame.to_sql.assert_called_once_with('fundraisers', ANY, if_exists='append')



    def tearDown(self) -> None:
        self.scraper.driver.close()

unittest.main(argv=[''], verbosity=0, exit=False)
