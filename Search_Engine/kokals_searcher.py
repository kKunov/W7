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
    searchwords = request.args.get('search', '')
    words_list = []
    results = []
    for word in searchwords.split():
        words_list.append(word)
        results_for_one_word = session.query(Page.url, Page.title
                                             ).filter(Page.url.
                                                      like("%{}%".format(word))
                                                      ).all()
        for result in results_for_one_word:
            results.append(result)

    return render_template('search.html', pages=results, words_list=words_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

