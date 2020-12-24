# python manage.py runscript create_prac_data
import random

from prac.models import Reporter, Article
from datetime import date


def run():
    # Reporter data
    r1 = Reporter.objects.create(
        first_name="John", last_name="Smith", email="john@example.com"
    )
    r2 = Reporter.objects.create(
        first_name="Paul", last_name="Jones", email="paul@example.com"
    )
    r3 = Reporter.objects.create(
        first_name="Park", last_name="Silva", email="silva@example.com"
    )
    reporters = [r1, r2, r3]

    # Article data (belongs to reporter)
    article_count = 30
    for i in range(article_count):
        Article.objects.create(
            id=None,
            headline=f"This is a test headline {i}",
            pub_date=date(
                random.randint(1980, 2020), random.randint(1, 12), random.randint(1, 28)
            ),
            reporter=reporters[random.randint(0, 2)],
        )
