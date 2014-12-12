from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKey

Base = declarative_base()


class Website(Base):
    __tablename__ = "website"
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    #up_time = Column(DateTime)
    #html_version = Column(String)
    #is_ssl = Column(Boolean)


class Page(Base):
    __tablename__ = "page"
    id = Column(Integer, primary_key=True)
    website_id = Column(Integer, ForeignKey("website.id"))
    url = Column(String, unique=True)
    title = Column(String)
    #dirty_words = Column(Boolean)
