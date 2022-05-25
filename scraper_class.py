import logging
from nis import cat
from unicodedata import category

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep


class Logger:
    def __init__(self):
        pass

    @staticmethod
    def log_error(exception) -> None:
        with open('error_log.txt', 'a') as file:
            file.write(exception)


class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
    
    def load_page(self, url) -> None:
        self.driver.get(url)

        sleep(2) # there is a slight delay for cookie frame to appear on justgiving
        
        try:
            self.accept_cookies()
        except:
            pass


    def accept_cookies(self) -> None:
        try:
            accept_button = self.driver.find_element(by=By.XPATH, value='//*[@id="accept-all-Cookies"]')
            accept_button.click()

        except Exception as e:
            Logger.log_error(str(e))
            pass

    
    def get_category_urls(self) -> dict:

        categories_location = "//*[text()='Browse by fundraising category']//following-sibling::ul//descendant::a"

        categories = self.driver.find_elements(by=By.XPATH, value=categories_location)

        category_urls = {category.text: category.get_attribute('href') for category in categories}

        return(category_urls)


    def get_fundraiser_urls(self, n=6) -> list: # n=6 to remove need for load more button click for initial code

        #if n>6:
        #calculate how many times (x) to click load more and how many of the urls to save
        #click load more x times
        
        fundraisers_location = "//*[text()='Fundraisers']/parent::div//following-sibling::div//descendant::a"

        fundraisers = self.driver.find_elements(by=By.XPATH, value=fundraisers_location)

        fundraiser_urls = [fundraiser.get_attribute('href') for fundraiser in fundraisers] #add indexing here related to load more

        return(fundraiser_urls)


    def run(self):
        self.load_page('https://www.justgiving.com')
        category_urls = self.get_category_urls()

        fundraisers_dict = {}

        for category, url in category_urls.items():
            self.load_page(url)
            fundraiser_urls = self.get_fundraiser_urls()

            fundraisers_dict[category] = fundraiser_urls  

        print(fundraisers_dict)


scraper = Scraper()
scraper.run()


