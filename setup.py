from setuptools import setup
from setuptools import find_packages

setup(
    name='justgiving_web_scraper',
    version='0.0.1',
    description='Package allows you to scrape data about the different fundraisers on justgiving.com',
    url='https://github.com/shrutiturner/data-collection-pipeline',
    author='Shruti Turner',
    license='MIT',
    packages=find_packages(),
    install_requires=['boto3', 'math', 'os', 'pandas', 'pscopg2-binary', 'selenium', 'sqlalchemy' 'time', 'unicodedata', 'urllib.request', 'uuid'],
)