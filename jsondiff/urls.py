from django.urls import path

from .views import JsonDiffHomeView, sample_json1, sample_json2

urlpatterns = [
    path('', JsonDiffHomeView.as_view(), name='index'),
    path('sample1', sample_json1, name='index'),
    path('sample2', sample_json2, name='index'),
]
