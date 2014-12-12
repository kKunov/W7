from flask import Flask
from flask import render_template
from flask import request
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from searcher_db import Base, Page

engine = create_engine("sqlite:///searcher.db")
Base.metadata.create_all(engine)
session = Session(bind=engine)

app = Flask(__name__)


@app.route("/")
def main_page():
    test = open('test.html', 'r')
    test1 = test.read()
    test.close()
    return test1

@app.route('/search/')

@app.route('/search/<search>')
def search(search=None):
    searchword = request.args.get('search', '')
    results = session.query(Page.url).all()

    return render_template('search.html', pages=results, searchword=searchword)


if __name__ == '__main__':
    app.run(debug=True)
