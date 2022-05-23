from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep


class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome()

    
    def goto_url(self, url):
        self.driver.get(url)


    def run(self):
        self.goto_url('https://www.justgiving.com')


scraper = Scraper()
scraper.run()


