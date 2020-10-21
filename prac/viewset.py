from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from prac.models import Reporter, Article
from prac.serializer import ReporterSerializer, ArticleSerializer


class ReporterViewSet(viewsets.ViewSet):
    """
    A basic ViewSet for Reporter
    - If reserved function doesn't exist api returns 405 (Method not implemented)
    - need to implement each action(=function) manually

    https://www.django-rest-framework.org/api-guide/viewsets/
    """

    def list(self, request):
        # GET /prac/reporters/
        queryset = Reporter.objects.all()
        serializer = ReporterSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # GET /prac/reporters/1/
        queryset = Reporter.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ReporterSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        # POST /prac/reporters/
        return Response("create")

    def update(self, request, pk=None):
        # POST /prac/reporters/1/
        return Response("update")

    def partial_update(self, request, pk=None):
        # PATCH /prac/reporters/1/
        return Response("partial_update")

    def destroy(self, request, pk=None):
        # DELETE /prac/reporters/1/
        return Response("destroy")


class ArticleModelViewSet(viewsets.ModelViewSet):
    """
    Model ViewSet example

    - inherits from GenericAPIView
    - includes implementations for various basic actions (fundamental CRUD)
    - minimum required attributes: queryset, serializer_class (to support get_object(), get_queryset() )
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
