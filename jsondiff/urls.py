from django.urls import path

from .views import JsonDiffHomeView

urlpatterns = [
    path('', JsonDiffHomeView.as_view(), name='index'),
]