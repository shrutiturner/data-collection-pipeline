import json
import os

from logger import Logger
from math import ceil
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from unicodedata import category
from urllib.request import urlretrieve
from uuid import uuid4


class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
    

    def load_page(self, url) -> None:
        self.driver.get(url)

        sleep(2) # there is a slight delay for cookie frame to appear on justgiving
        
        self.accept_cookies()

        return None


    def get_elements(self, locator) -> list:
        
        elements = self.driver.find_elements(by=By.XPATH, value=locator)

        return elements

    
    def get_element(self, locator) -> object:
        
        element = self.driver.find_element(by=By.XPATH, value=locator)

        return element


    def accept_cookies(self) -> None:
        try:
            accept_button = self.get_element('//*[@id="accept-all-Cookies"]')
            accept_button.click()

        except AttributeError:
            pass # if accept cookies button isn't there, move on

        except Exception as e:
            Logger.log_error(str(e))
            pass
    

    def get_category_urls(self) -> list:

        categories_locator = "//*[text()='Browse by fundraising category']//following-sibling::ul//descendant::a"
        categories = self.get_elements(categories_locator)
        category_urls = [{'category': category.text, 'url': category.get_attribute('href')} for category in categories]

        return category_urls


    def get_fundraiser_urls(self, n) -> list:

        if n > 6:

            num_clicks = ceil(n / 6)
            count = 0

            load_more_locator = "//*[@data-testid='jg-search-load-next-page--fundraiser']"
            load_more_button = self.get_element(load_more_locator)

            while count < num_clicks:
                sleep(2)
                try:
                    load_more_button.click()
                    count += 1
                except AttributeError:
                    Logger.log_error("There are no more fundraisers!")
                    break
                except Exception as e:
                    Logger.log_error(str(e))
                    pass
        
        fundraisers_locator = "//*[text()='Fundraisers']/parent::div//following-sibling::div//descendant::a"
        fundraisers = self.get_elements(fundraisers_locator)
        fundraiser_urls = [fundraiser.get_attribute('href') for fundraiser in fundraisers][:n]

        return fundraiser_urls


    def get_slug(self, url_string) -> str:

        slug = url_string.rpartition('/')[-1]

        return slug


    def get_fundraisers(self, category, num_pages) -> list:

        fundraiser_urls = self.get_fundraiser_urls(num_pages)
        fundraisers = [{'slug': self.get_slug(url), 'url': url, 'category': category, 'id' : str(uuid4())} for url in fundraiser_urls]

        return fundraisers


    def get_fundraiser_charity(self) -> str:
        try:
            charity_locator = "(//*[@data-qa='relationship-name-link'])[1]"
            charity = self.get_element(charity_locator)

            return charity.text

        except Exception as e:
            Logger.log_error(str(e))

            return None


    def get_fundraiser_total(self) -> str:
        try:
            total_locator = "(//*[@data-qa='totaliser-total'])"
            total = self.get_element(total_locator)

            return total.text.replace('£', '')

        except Exception as e:
            Logger.log_error(str(e))

            return None


    def get_fundraiser_donor_num(self) -> str:
        try:
            donor_num_locator = "(//*[@data-qa='totaliser-message']/span[contains(text(), 'supporter')])"
            donor_num = self.get_element(donor_num_locator)
            number = donor_num.text.rpartition(' ')[0] # remove the ' supporter(s)' and get only number

            return number

        except Exception as e:
            Logger.log_error(str(e))

            return None


    def get_fundraiser_image_url(self) -> str:
        try:
            image_locator = "(//*[@data-qa='app']//img)[1]"
            image_url = self.get_element(image_locator).get_attribute('src')

            return image_url

        except Exception as e:
            Logger.log_error(str(e))

            return None

    
    def get_charity_image_url(self) -> str:
        try:
            charity_image_locator = "(//*[@data-qa='owner-logo']//img)[1]"            
            charity_image_url = self.get_element(charity_image_locator).get_attribute('src')

            return charity_image_url

        except Exception as e:
            Logger.log_error(str(e))

            return None

    
    def get_fundraiser_info(self) -> dict:
        
        data = {'charity': self.get_fundraiser_charity(),
        'charity_image': self.get_charity_image_url(), 'total': self.get_fundraiser_total(), 
        'donor_num': self.get_fundraiser_donor_num(), 'fundraiser_image': self.get_fundraiser_image_url()}

        return data

    
    def write_json(self, data, path) -> None:

        with open(path + '/data.json', 'a') as data_file:
            json.dump(data, data_file)

        return None

    
    def download_image(self, path, image_url, image_name) -> None:

        try:
            urlretrieve(image_url, path + '/' + image_name)
        
        except Exception as e:
            Logger.log_error(str(e))

        finally:
            return None



if __name__ == "__main__":
    scraper = Scraper()

    try:
        scraper.load_page('https://www.justgiving.com')
        
        category_urls = scraper.get_category_urls()

        fundraisers = []

        for category in category_urls:
            scraper.load_page(category['url'])
            fundraisers = fundraisers + scraper.get_fundraisers(category['category'], 2) #input argument = number of urls wanted

        for fundraiser in fundraisers:
            scraper.load_page(fundraiser['url'])
            fundraiser = {**fundraiser, **scraper.get_fundraiser_info()}

            path = f"raw_data/{fundraiser['category']}/{fundraiser['slug']}"

            if not os.path.exists(path):
                os.makedirs(path)

            scraper.write_json(fundraiser, path)
            scraper.download_image(path, fundraiser['charity_image'], 'charity_image.jpg')
            scraper.download_image(path, fundraiser['fundraiser_image'], 'fundraiser_image.jpg')
        
    except:

    finally:
        scraper.driver.close()