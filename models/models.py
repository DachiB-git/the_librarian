import re

from bs4 import BeautifulSoup


class Book:
    __constants = {
        "BASE_URL": "https://openlibrary.org",
        "BOOK_COVER_CLASS": "book-cover"
    }

    def __init__(self, node):
        self.__data = {}
        self.__construct_book(node)

    def __construct_book(self, node: BeautifulSoup):
        try:
            cover = node.find("div", class_=self.__constants["BOOK_COVER_CLASS"])
            link = cover.find("a")
            meta = cover.find("img")
            self.__data["title"] = meta["title"]
            author = re.search(".+ by (.+)", meta["title"])
            if author:
                author = author.group(1)
            self.__data["author"] = author
            cover = re.search("(^//covers.+)", meta["src"])
            if cover:
                cover = "https:" + cover.group(1)
            self.__data["cover"] = cover
            self.__data["link"] = self.__constants["BASE_URL"] + link["href"]
        except TypeError or KeyError:
            print(node)

    def get(self, key):
        return self.__data.get(key)

    def __str__(self):
        return self.__data.__str__()

    def to_dict(self):
        return self.__data

    @staticmethod
    def keys():
        return ["title", "author", "category", "cover", "link"]
