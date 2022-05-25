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

        # going to have to deal with popups, as justgiving has them sometimes when changing page - most close with esc
        sleep(2) # there is a slight delay for cookie frame to appear on justgiving
        self.accept_cookies()


    def accept_cookies(self) -> None:
        try:
            accept_button = self.driver.find_element(by=By.XPATH, value='//*[@id="accept-all-Cookies"]')
            accept_button.click()

        except Exception as e:
            Logger.log_error(e)
            pass

    
    def find_category_urls(self) -> dict:

        categories_location = "//*[text()='Browse by fundraising category']//following-sibling::ul//descendant::a"

        categories = self.driver.find_elements(by=By.XPATH, value=categories_location)

        category_urls = {category.text: category.get_attribute('href') for category in categories}

        return(category_urls)


    def get_fundraisers(self, n=6): # n=6 to remove need for load more button click for initial code
        # find the urls for the top n fundraisers listed and put them in a list
        pass

    def run(self):
        self.load_page('https://www.justgiving.com')
        self.find_category_urls()


scraper = Scraper()
scraper.run()


