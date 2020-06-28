from django.urls import path

from .views import JsonDiffHomeView, sample_json1, sample_json2

app_name = "jsondiff"

urlpatterns = [
    path('', JsonDiffHomeView.as_view(), name='index'),
    path('sample1', sample_json1, name='sample1'),
    path('sample2', sample_json2, name='sample2'),
]
