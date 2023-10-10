import requests
import logging
import re
import time 
from bs4 import BeautifulSoup

from .models import Book

class WebScraping:

    base_url = 'https://books.toscrape.com/'
    catalog_url = f'{base_url}/catalogue/'

    # Configuração do logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    @classmethod
    def get_book(cls):
        page_number = 1
        
        while True:
            url = f'{cls.catalog_url}/page-{page_number}.html'
            response_page = cls._fetch_page(url)

            if not response_page:
                break

            soup_page = BeautifulSoup(response_page, 'html.parser')
            books = soup_page.find_all('h3')

            if not books:
                break

            for book in books:
                book_url = f'{cls.catalog_url}/{book.find("a")["href"]}'
                book_data = cls._parse_book_data(book_url)
                if book_data:
                    yield book_data

            page_number += 1

    @classmethod
    def _fetch_page(cls, url):
        response = requests.get(url)
        if response.status_code != 200:
            logging.info(f"request status: {url} Cannot be accessed.")
            return None
        return response.content


    @classmethod
    def _parse_book_data(cls, book_url):
        book_response = requests.get(book_url)
        book_soup = BeautifulSoup(book_response.content, 'html.parser')

        _upc = book_soup.find("td", string=re.compile(r'^\w{16}$')).text
        _title = book_soup.find('h1').text 
        _category = book_soup.find('ul', class_='breadcrumb').find_all('a')[2].text.strip()
        _rating = book_soup.find('p', class_='star-rating')['class'][1]
        _price = book_soup.find("th", string="Price (excl. tax)").find_next_sibling("td").text
        _in_stock = book_soup.find('p', class_='availability').text.strip()

        return Book(upc=_upc, title=_title, category=_category, rating=_rating, price=_price, in_stock=_in_stock)

