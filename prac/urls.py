from django.urls import path
from rest_framework.routers import DefaultRouter

from prac.viewset import ReporterViewSet, ArticleModelViewSet

app_name = "prac"

router = DefaultRouter()
router.register(r"reporters", ReporterViewSet, basename="reporter")
router.register(r"articles", ArticleModelViewSet, basename="article")
urlpatterns = [] + router.urls
