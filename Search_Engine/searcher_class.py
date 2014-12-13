from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime
from searcher_db import Website, Page, Base
from bs4 import BeautifulSoup
import requests


engine = create_engine("sqlite:///searcher.db")
Base.metadata.create_all(engine)
session = Session(bind=engine)


class Spider():

    def __init__(self, website):
        self.http = "http://"
        self.https = "https://"
        self.website = self.prepare_website(website)
        self.to_scan = []
        self.scaned = []

    def add_web_to_db(self, website):

        try:
            session.add(Website(url=website))
            session.commit()

        except Exception as e:
            session.rollback()
            print(e)

    def prepare_website(self, website):

        if website.startswith(self.http) or website.startswith(self.https):

            self.add_web_to_db(website)
            return website

        else:
            self.add_web_to_db(self.http + website)
            return self.http + website

    def scan_website(self):
        self.to_scan.append(self.website)

        while len(self.to_scan) != 0:
            self.scan_page(self.to_scan.pop())

    def scan_page(self, link):
        url = ''

        if link != self.website and link.startswith(self.website) is False:
            url = self.prepare_link(link)

        else:
            url = link

        try:
            request = requests.get(url)

        except Exception as e:
            print(e)
            return

        html = request.text
        soup = BeautifulSoup(html)

        self.add_to_to_scan(soup)

        try:
            self.add_to_db(url, soup)
            print("added url: {0}".format(url))

        except Exception:
            session.rollback()
            print("Bad url")
            print(" ")
            print(" ")

        self.scaned.append(url)

    def add_to_db(self, url, soup):

        web_id = session.query(Website.id).filter(Website.url == self.website
                                                  ).one()

        try:
            title = soup.title.string.encode('utf-8')

        except Exception:
            title = "N/A"

        session.add(Page(url=url, website_id=web_id[0], title=title))
        session.commit()

    def add_to_to_scan(self, soup):

        for link in soup.find_all('a'):
            new_link = link.get('href')

            if (new_link is not None and
                    new_link not in self.to_scan and
                    self.website + new_link not in self.scaned and
                    new_link not in self.scaned and
                    new_link.endswith('.jpg') is False and
                    new_link.endswith('.png') is False and
                    (new_link.startswith('/') or
                        new_link.startswith(self.website)) and
                    "#" not in new_link):

                self.to_scan.append(new_link)

    def prepare_link(self, link):
        return self.website + link
