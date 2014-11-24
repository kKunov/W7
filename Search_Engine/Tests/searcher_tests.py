import unittest
import sys
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
sys.path.append("..")
from searcher_db import Website, Page

Base = declarative_base()

engine = create_engine("sqlite:///searcher.db")
Base.metadata.create_all(engine)

session = Session(bind=engine)


class TestWebsite(unittest.TestCase):
    def setUp(self):
        self.site1 = Website(url="test.html", server="no server",
                             up_time=datetime.strptime("24/11/14", "%d/%m/%y"),
                             html_version="html5.0", is_ssl=True)
        session.add(self.site1)
        session.commit()

    def tearDown(self):
        session.query(Website).filter(Website.id == self.site1.id).delete()
        session.commit()

    def test_init(self):
        self.assertEqual(self.site1.url, "test.html")
        self.assertEqual(self.site1.server, "no server")
        self.assertEqual(self.site1.up_time, datetime(2014, 11, 24, 0, 0))
        self.assertEqual(self.site1.html_version, "html5.0")
        self.assertEqual(self.site1.is_ssl, True)

    def test_db(self):
        new_site_url = session.query(Website.url
                                     ).filter(Website.id == self.site1.id
                                              ).one()
        new_site_server = session.query(Website.server
                                        ).filter(Website.id == self.site1.id
                                                 ).one()
        new_site_up_time = session.query(Website.up_time
                                         ).filter(Website.id == self.site1.id
                                                  ).one()
        new_site_html_version = session.query(Website.html_version
                                              ).filter(Website.id ==
                                                       self.site1.id).one()
        new_site_is_ssl = session.query(Website.is_ssl
                                        ).filter(Website.id == self.site1.id
                                                 ).one()
        self.assertEqual(new_site_url[0], "test.html")
        self.assertEqual(new_site_server[0], "no server")
        self.assertEqual(new_site_up_time[0], datetime(2014, 11, 24, 0, 0))
        self.assertEqual(new_site_html_version[0], "html5.0")
        self.assertEqual(new_site_is_ssl[0], True)


class TestPage(unittest.TestCase):
    def setUp(self):
        self.page1 = Page(website="test.html", url="test.html", title="hi",
                          dirty_words=False)
        session.add(self.page1)
        session.commit()

    def tearDown(self):
        session.query(Page).filter(Page.id == self.page1.id).delete()
        session.commit()

    def test_init(self):
        self.assertEqual(self.page1.website, "test.html")
        self.assertEqual(self.page1.url, "test.html")
        self.assertEqual(self.page1.title, "hi")
        self.assertEqual(self.page1.dirty_words, False)

    def test_db(self):
        site = session.query(Page.website).filter(Page.id == self.page1.id
                                                  ).one()
        url = session.query(Page.url).filter(Page.id == self.page1.id).one()
        title = session.query(Page.title).filter(Page.id == self.page1.id
                                                 ).one()
        dirty_words = session.query(Page.dirty_words
                                    ).filter(Page.id == self.page1.id).one()
        self.assertEqual(site[0], "test.html")
        self.assertEqual(url[0], "test.html")
        self.assertEqual(title[0], "hi")
        self.assertEqual(dirty_words[0], False)


if __name__ == '__main__':
    unittest.main()
