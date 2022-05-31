import logging
from nis import cat
from unicodedata import category

from math import ceil
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from uuid import uuid4



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

        categories_locator = "//*[text()='Browse by fundraising category']//following-sibling::ul//descendant::a"

        categories = self.driver.find_elements(by=By.XPATH, value=categories_locator)

        category_urls = {category.text: category.get_attribute('href') for category in categories}

        return(category_urls)


    def get_fundraiser_urls(self, n) -> list:

        if n > 6:

            num_clicks = ceil(n / 6)
            count = 0

            load_more_locator = "//*[@data-testid='jg-search-load-next-page--fundraiser']"
            load_more_button = self.driver.find_element(by=By.XPATH, value=load_more_locator)

            while count < num_clicks:
                sleep(2)
                try:
                    load_more_button.click()
                    count += 1
                except AttributeError:
                    print("There are no more fundraisers!")
                    break

        
        fundraisers_locator = "//*[text()='Fundraisers']/parent::div//following-sibling::div//descendant::a"
        fundraisers = self.driver.find_elements(by=By.XPATH, value=fundraisers_locator)
        fundraiser_urls = [fundraiser.get_attribute('href') for fundraiser in fundraisers][:n]

        return(fundraiser_urls)


    def get_identifiers(self, url_string) -> str:

        dict_id = url_string.rpartition('/')[-1]

        return(dict_id)


    def get_fundraisers(self, category, num_pages) -> dict:

        fundraiser_urls = self.get_fundraiser_urls(num_pages)

        fundraisers_dict = {self.get_identifiers(url): {'url': url, 'category': category, 'id' : uuid4()} for url in fundraiser_urls}

        return(fundraisers_dict)



if __name__ == "__main__":

    scraper = Scraper()

    scraper.load_page('https://www.justgiving.com')
    
    category_urls = scraper.get_category_urls()

    fundraisers_dict = {}

    for category, url in category_urls.items():
        scraper.load_page(url)
        fundraisers_dict = {**scraper.get_fundraisers(category, 6), **fundraisers_dict} #input argument = number of urls wanted

    print(fundraisers_dict)

    scraper.driver.close()