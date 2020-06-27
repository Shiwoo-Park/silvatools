from django.http import HttpResponse
from django.views.generic import TemplateView


class JsonDiffHomeView(TemplateView):
    template_name = 'jsondiff/index.html'
