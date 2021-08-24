import requests
from bs4 import BeautifulSoup

from common.util import fetch_user_agent


class Soup:
    def __init__(self, url: str) -> None:
        self.soup = self.fetch_soup(url)

    def fetch_soup(self, url: str):
        headers = {"User-Agent": fetch_user_agent()}
        resp = requests.get(url, headers=headers)
        return BeautifulSoup(resp.text, "html.parser")

    def selects(self, selector: str):
        return self.soup.select(selector)

    def select(self, selector: str):
        return self.soup.select_one(selector)
