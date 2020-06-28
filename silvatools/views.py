from django.views.generic import TemplateView


class MainHomeView(TemplateView):
    template_name = "home.html"
