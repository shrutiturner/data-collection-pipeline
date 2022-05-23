from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep


class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome()

    
    def load_page(self, url):
        self.driver.get(url)

        # going to have to deal with popups, as justgiving has them sometimes when changing page - most close with esc
        sleep(2) # there is a slight delay for cookie frame to appear on justgiving
        self.accept_cookies()


    def accept_cookies(self):
        try:
            accept_button = self.driver.find_element(by=By.XPATH, value='//*[@id="accept-all-Cookies"]')
            accept_button.click()

        # need proper exception handling here
        except Exception as e:
            print('Unable to find accept button')
            print(e)
            pass


    def run(self):
        self.load_page('https://www.justgiving.com')
        


scraper = Scraper()
scraper.run()


