import csv
import json
import re

import requests
from bs4 import BeautifulSoup
from utils.parser import JSON
from models.models import Book


class Librarian:
    __constants = {
        "BASE_URL": "https://openlibrary.org",
        "CAROUSEL_CLASS": "carousel-section",
        "CAROUSEL_HEADER_CLASS": "carousel-section-header",
        "CAROUSEL_CONTAINER_CLASS": "carousel-container",
        "CAROUSEL_ITEM_CLASS": "book",
    }

    def __get_home_page_content(self):
        try:
            res = requests.get(self.__constants["BASE_URL"], verify=True)
            if not res.ok:
                raise requests.exceptions.RequestException(f"Error: {res.status_code}. Please try again later.")
            return BeautifulSoup(res.text, "html.parser")
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def __get_categories(self, node: BeautifulSoup):
        categories = []
        sections = node.find_all("div", class_=self.__constants["CAROUSEL_CLASS"])
        for section in sections:
            try:
                header = section.find("div", class_=self.__constants["CAROUSEL_HEADER_CLASS"]).find("h2")
                ref = header.find("a")["href"]
                ref = ref if re.match("^https://.*", ref) else self.__constants["BASE_URL"] + ref
                categories.append({"name": header.text.strip(), "ref": ref})
            except TypeError:
                continue
        return categories

    def __get_books(self, node: BeautifulSoup):
        all_books = []
        sections = node.find_all("div", class_=self.__constants["CAROUSEL_CLASS"])
        for section in sections:
            books = section.find_all("div", class_=self.__constants["CAROUSEL_ITEM_CLASS"])
            for book in books:
                all_books.append(Book(book))
        return all_books

    def __save_to_json(self, data):
        with open("data/data.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

    def __save_to_csv(self, data):
        with open("data/data.csv", "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow([key.capitalize() for key in Book.keys()])
            for item in data:
                w.writerow(item.values())

    def __load_json(self, fn):
        return JSON().parsef(fn)

    def __load_csv(self, fn):
        data = []
        with open(fn, "r", encoding="utf-8") as f:
            r = csv.reader(f)
            for row in r:
                data.append(row)
        return data

    def run(self):
        dom = self.__get_home_page_content()
        books = self.__get_books(dom)
        self.__save_to_json([book.to_dict() for book in books])
        self.__save_to_csv([book.to_dict() for book in books])
        parser = JSON()
        json = parser.parsef("data/data.json")
        csv = self.__load_csv("data/data.csv")
        books_from_csv = [Book.from_list(row) for row in csv]
        books_from_json = [Book.from_dict(item) for item in json]
        for book in books_from_json:
            print(book)
