from django.urls import path
from rest_framework.routers import DefaultRouter

from prac.viewset import ReporterViewSet

app_name = "prac"

router = DefaultRouter()
router.register(r"reporters", ReporterViewSet, basename="reporter")
urlpatterns = [] + router.urls
