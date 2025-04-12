import re

import requests
from bs4 import BeautifulSoup
from utils.parser import JSON


class Librarian:
    __constants = {
        "BASE_URL": "https://openlibrary.org",
        "CAROUSEL_CLASS": "carousel-section",
        "CAROUSEL_HEADER_CLASS": "carousel-section-header"
    }

    def __get_home_page_content(self):
        try:
            res = requests.get(self.__constants["BASE_URL"], verify=True)
            return BeautifulSoup(res.text, "html.parser")
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def __get_categories(self, node: BeautifulSoup):
        categories = []
        sections = node.find_all("div", class_=self.__constants["CAROUSEL_CLASS"])
        print(node)
        for section in sections:
            try:
                header = section.find("div", class_=self.__constants["CAROUSEL_HEADER_CLASS"]).find("h2")
                ref = header.find("a")["href"]
                ref = ref if re.match("^https://.*", ref) else self.__constants["BASE_URL"] + ref
                categories.append({"name": header.text.strip(), "ref": ref})
            except TypeError:
                continue
        return categories

    def run(self):
        dom = self.__get_home_page_content()
        categories = self.__get_categories(dom)
        print(categories)
