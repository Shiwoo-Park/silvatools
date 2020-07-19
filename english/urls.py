from django.urls import path

from english.views import (
    EnglishHomeView,
    EnglishWordListView,
    EnglishTestGeneratorView,
    EnglishWordTestListView,
)

app_name = "english"

urlpatterns = [
    path("", EnglishHomeView.as_view(), name="index"),
    path("word-list", EnglishWordListView.as_view(), name="word_list"),
    path("generator", EnglishTestGeneratorView.as_view(), name="generator"),
    path("word-test-list", EnglishWordTestListView.as_view(), name="word_test_list"),
]
