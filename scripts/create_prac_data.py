from prac.models import Reporter, Article
from datetime import date


def run():
    # Reporter data
    r = Reporter.objects.create(
        first_name="John", last_name="Smith", email="john@example.com"
    )
    r2 = Reporter.objects.create(
        first_name="Paul", last_name="Jones", email="paul@example.com"
    )

    # Article data (belongs to reporter)
    a = Article.objects.create(
        id=None, headline="This is a test", pub_date=date(2005, 7, 27), reporter=r
    )
    a2 = Article.objects.create(
        id=None, headline="This is a test22222", pub_date=date(2005, 7, 27), reporter=r
    )
