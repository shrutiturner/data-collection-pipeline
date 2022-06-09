import sys
sys.path.append("..")

import unittest

from src.scraper import Scraper

class ScraperTestCase(unittest.TestCase):
    
    def setUp(self) -> None:
        self.scraper = Scraper()


    def test_get_category_urls(self):
        
        self.scraper.load_page('https://www.justgiving.com')

        actual_categories = self.scraper.get_category_urls()
        self.assertEqual(list, type(actual_categories))

        actual_first_category = actual_categories[0]
        self.assertEqual(dict, type(actual_first_category))

        self.assertIn('category', actual_first_category)
        self.assertIn('url', actual_first_category)

        self.assertAlmostEqual('Animals and pets', actual_first_category['category'])
        self.assertAlmostEqual('https://www.justgiving.com/search?q=animals%20and%20pets&type=onesearch', actual_first_category['url'])


    def test_get_fundraiser_info(self):
        
        test_url = 'https://www.justgiving.com/fundraising/benenden-health'
        self.scraper.load_page(test_url)

        actual_fundraiser_info = self.scraper.get_fundraiser_info()
        self.assertEqual(dict, type(actual_fundraiser_info))

        self.assertIn('charity', actual_fundraiser_info)
        self.assertIn('charity_image', actual_fundraiser_info)
        self.assertIn('total', actual_fundraiser_info)
        self.assertIn('donor_num', actual_fundraiser_info)
        self.assertIn('fundraiser_image', actual_fundraiser_info)

        self.assertAlmostEqual('York Mind (Incorporating Our Celebration) Ltd', actual_fundraiser_info['charity'])
        self.assertAlmostEqual('https://images.jg-cdn.com/image/d58408fb-1d2f-4968-8706-cb916864c231.jpg?template=PagesUIFeatureImage', actual_fundraiser_info['fundraiser_image'])
        self.assertAlmostEqual('https://images.jg-cdn.com/image/54f9b6b0-375e-4259-ad29-1f663a996343.jpg?template=Size120x120', actual_fundraiser_info['charity_image'])


    def test_get_fundraisers(self):
        
        test_url = 'https://www.justgiving.com/search?q=animals%20and%20pets&type=onesearch'
        self.scraper.load_page(test_url)
        
        test_n = 10

        actual_fundraisers = self.scraper.get_fundraisers('Animals and pets', test_n)

        actual_fundraiser = actual_fundraisers[0]

        self.assertEqual(test_n, len(actual_fundraisers))
        self.assertIn('slug', actual_fundraiser)
        self.assertIn('url', actual_fundraiser)
        self.assertIn('category', actual_fundraiser)
        self.assertIn('id', actual_fundraiser)

        self.assertIs(str, type(actual_fundraiser['slug']))
        self.assertIs(str, type(actual_fundraiser['url']))
        self.assertIs(str, type(actual_fundraiser['category']))
        self.assertIs(str, type(actual_fundraiser['id']))


    def tearDown(self) -> None:
        self.scraper.driver.close()

unittest.main(argv=[''], verbosity=0, exit=False)
