# data-collection-pipeline
AiCore project to learn about data collection pipelines using web scraping example. The website chosen was 'https://www.justgiving.com'.

This README documents the actions taken and decisions made during each step of the project.

Technologies used: Python (math, os, selenium, time, unicodedata, urllib, uuid)

## Milestone 1 - Decide Target Website
Chose 'https://www.justgiving.com' to scrape due to the amount of different types of data on the website. The charitable sectors is very large and data insights could help maximise fundraising by understanding donor and fundraiser behaviours.

## Milestone 2 - Prototype Finding Target Pages
Environment set up and creating an initial scraper using Selenium to load a webpage and navigate through it to obtain the URLS of pages with the desired information. Two classes were created: a logger for logging errors to a text file, and the scraper class containing the methods (each doing on task) to obtain the urls of the first n (user decision) fundraising pages in each category.

This has been a good opportunity to practice object oriented programming, implement expeption handling and gain more insight into how the frontend of a website is structured.

## Milestone 3 - Retrieve Data From Target Pages
Added methods to the scraper class to retrieve the relevant data from each of the fundraiser pages and save this locally. Thought was put into deciding which data may be relevant and how best to get these e.g. using more robust XPATHs rather than defaults. During this milestone, methods were refactored seveal times to ensure that each one was not reliant on previous, but only dealt with one problem focused on data structures. Work was also put in to remove the need for nest for loops for time efficiency. 

The section has pushed me to consider how my code is working, not just that it does work, and appreciate the traits of different data structures to allow efficient implementation.

## Milestone 4 - Documentation and Testing
The code has a dedicated refactor (rather than just doing it along the way) to further optimise the code. Doc strings have been addeed to all public methods in the Google layout and a combination of unit and end to end tests have been written. Tests have been written only to test the code logic written, leaving out those functions that merely implement python built-in functions. The project structure, including creating build files, was also updated to be more distribution ready.

This milestone has allowed me to understand some of the developer benefits of encapsulation and OOP (in terms of writing test and doc strings!), as well the computational benefits. There are many ways to test the same method and code is always a work in progress, and optimisation/refactoring is an ongoing process.

## Milestone 5 - Scalably Store the Data
Sets up AWS to save image data to S3 bucket and tabular data to a PostgreSQL database on the cloud. Code was updated to implement an AWS port in its own class, and the Scraper methods were updated to save to the cloud rather than locally. Scraper runs successfully with data saving to the cloud. Additional tests were written for the AWS methods using mocking. 
