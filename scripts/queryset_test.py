from random import randint

from prac.models import Article


def run(*args, **kwargs):
    queryset = Article.objects.filter(reporter_id=1)

    # multiple update test
    new_titles = ["AAA", "BBBB", "CCCC", "DDDD"]
    elems = queryset.all()
    for elem in elems:
        elem.headline = f"{new_titles[randint(0,3)]} - {randint(1,100)}"
    Article.objects.bulk_update(objs=elems, fields=("headline",))
