from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime
from searcher_db import Website, Page

engine = create_engine("sqlite:///searcher.db")

session = Session(bind=engine)


def website_adder(sitelist):
    for site in sitelist:

