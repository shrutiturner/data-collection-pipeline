# import out unittest library 
from re import A
import unittest

# import sys to allow us to append the system path
import sys
import boto3

from unittest import mock 
# append the parent folder
sys.path.append('../') 

from src.scraper import Scraper
from unittest.mock import ANY, patch, MagicMock
from sqlalchemy import create_engine


class ScraperTestCaseUnit(unittest.TestCase):
    
    @patch('selenium.webdriver.Chrome')
    def setUp(self, _) -> None:
        self.scraper = Scraper()


    @patch('boto3.client')
    @patch('urllib.request.urlretrieve')
    def test_get_image(self, mock_urlretrieve, mock_boto_client) -> None:
        
        mock_urlretrieve.return_value = mock_urlretrieve

        mock_s3_client = MagicMock()
        mock_s3_client.upload_file.return_value = None
        mock_boto_client.return_value = mock_s3_client

        actual = self.scraper.get_image('fundraiser_name', 'test-image-url', 'test-image-name')
        
        mock_boto_client.assert_called_once_with('s3')
        mock_urlretrieve.assert_called_once_with('test-image-url', '/tmp/test-image-name')
        mock_s3_client.upload_file.assert_called_once_with('/tmp/test-image-name', 'justgiving-scraper', 'fundraiser_name/test-image-name')
        self.assertEqual("s3://justgiving-scraper/fundraiser_name/test-image-name", actual)


    @patch('sqlalchemy.create_engine')
    @patch('pandas.DataFrame')
    def test_save_data(self, mock_df, mock_engine) -> None:
        mock_DataFrame = MagicMock()
        mock_DataFrame.to_sql.return_value = None
        mock_df.return_value = mock_DataFrame

        mock_rds = MagicMock()
        mock_rds.connect.return_value = None

        mock_rds_execute = MagicMock()
        mock_rds_execute.fetchall.return_value = None

        mock_rds.execute.return_value = mock_rds_execute
        mock_engine.return_value = mock_rds

        self.scraper.save_data({'key': 'value', 'key2': 'value2', 'slug': 'test-slug'})
        
        mock_df.assert_called_once_with({'key': 'value', 'key2': 'value2', 'slug': 'test-slug'}, index=[ANY])
        mock_DataFrame.to_sql.assert_called_once_with('fundraisers', ANY, if_exists='append')


unittest.main(argv=[''], verbosity=0, exit=False)
