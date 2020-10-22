from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from rest_framework import viewsets
from rest_framework.decorators import action
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
        # urlname: "prac:reporters-list"
        queryset = Reporter.objects.all()
        serializer = ReporterSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # GET /prac/reporters/1/
        # urlname: "prac:reporters-detail"
        queryset = Reporter.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ReporterSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        # POST /prac/reporters/
        # urlname: "prac:reporter-list"
        return Response("create")

    def update(self, request, pk=None):
        # PUT /prac/reporters/1/
        # urlname: "prac:reporter-detail"
        return Response("update")

    def partial_update(self, request, pk=None):
        # PATCH /prac/reporters/1/
        # urlname: "prac:reporter-detail"
        return Response("partial_update")

    def destroy(self, request, pk=None):
        # DELETE /prac/reporters/1/
        # urlname: "prac:reporter-detail"
        return Response("destroy")

    @action(detail=False)
    def hello(self, request):
        # GET /prac/reporters/hello/
        # urlname: "prac:reporter-hello"
        return Response("hello")

    @action(detail=True, methods=["post"])
    def byebye(self, request, pk=None):
        # GET /prac/reporters/1/byebye/
        # urlname: "prac:reporter-byebye"
        return Response(f"byebye: {pk}")

    @action(detail=False)
    def show_all_urlname(self, request):
        # GET /prac/reporters/show-all-urlname/
        # urlname: "prac:reporter-show_all_urlname"
        return Response(
            data={
                "prac:reporter-list": reverse_lazy("prac:reporter-list"),
                "prac:reporter-detail": reverse_lazy("prac:reporter-detail", args=[1]),
                "prac:reporter-hello": reverse_lazy("prac:reporter-hello"),
                "prac:reporter-byebye": reverse_lazy("prac:reporter-byebye", args=[1]),
                "prac:reporter-show-all-urlname": reverse_lazy(
                    "prac:reporter-show-all-urlname"
                ),
            }
        )


class ArticleModelViewSet(viewsets.ModelViewSet):
    """
    Model ViewSet example

    - inherits from GenericAPIView
    - includes implementations for various basic actions (fundamental CRUD)
    - minimum required attributes: queryset, serializer_class (to support get_object(), get_queryset() )
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
