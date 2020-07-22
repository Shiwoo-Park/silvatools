from django.urls import path, include

from english.views import (
    EnglishHomeView,
    EnglishWordListView,
    EnglishTestGeneratorView,
    EnglishWordTestListView,
)
from english.views_api import DownloadPDFTestAPIView, EnglishTestPDFGeneratorAPIView

app_name = "english"

api_urlpatterns = [
    path("pdf-down", DownloadPDFTestAPIView.as_view(), name="pdf_download")
]

urlpatterns = [
    path("", EnglishHomeView.as_view(), name="index"),
    path("api/", include(api_urlpatterns)),
    path("word-list/", EnglishWordListView.as_view(), name="word_list"),
    path("generator/", EnglishTestGeneratorView.as_view(), name="generator"),
    path(
        "pdf-generator/", EnglishTestPDFGeneratorAPIView.as_view(), name="pdf_generator"
    ),
    path("word-test-list/", EnglishWordTestListView.as_view(), name="word_test_list"),
]
