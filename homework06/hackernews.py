from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()

    new_id = request.query['id']
    label  = request.query['label']

    new = s.query(News).get(new_id)
    new.label = label

    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    news_list = get_news('https://news.ycombinator.com/newest', n_pages=1)
    for new in news_list:
        q = s.query(News).filter(
                        News.title  == new["title"],
                        News.author == new["author"])

        if not s.query(q.exists()):
            news = News(title=new["title"],
                        author=new["author"],
                        url=new["url"],
                        comments=new["comments"],
                        points=new["points"])
            s.add(news)
            s.commit()

    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    train_news = s.query(News).filter(News.label != None).all()
    X_train = [new.title for new in train_news]
    y_train = [new.label for new in train_news]

    clf = NaiveBayesClassifier()
    clf.fit(X_train, y_train)

    classified_news = s.query(News).filter(News.label == None)
    labels = clf.predict([new.title for new in classified_news])
    labels = [(labels[i], new) for i, new in enumerate(classified_news)]
    labels.sort(key = lambda x: x[0])
    print(labels)
    rows = [new[1] for new in labels]

    return template('news_template', rows=rows)

if __name__ == "__main__":
    run(host="localhost", port=8080)
