# data-collection-pipeline
AiCore project to learn about data collection pipelines using web scraping example. The website chosen was 'https://www.justgiving.com'.

This README documents the actions taken and decisions made during each step of the project.

Technologies used: Python (time, selenium, math, unicodedata)

## Milestone 1
Chose 'https://www.justgiving.com' to scrape due to the amount of different types of data on the website. The charitable sectors is very large and data insights could help maximise fundraising by understanding donor and fundraiser behaviours.

## Milestone 2
Environment set up and creating an initial scraper using Selenium to load a webpage and navigate through it to obtain the URLS of pages with the desired information. Two classes were created: a logger for logging errors to a text file, and the scraper class containing the methods (each doing on task) to obtain the urls of the first n (user decision) fundraising pages in each category.

This has been a good opportunity to practice object oriented programming, implement expeption handling and gain more insight into how the frontend of a website is structured.
