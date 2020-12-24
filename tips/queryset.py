from django.contrib.auth.models import User

# show SQL (use query.as_sql())
print(User.objects.all().query.as_sql())
