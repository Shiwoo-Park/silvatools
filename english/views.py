import logging
import random
import traceback

from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest
from django.views.generic import TemplateView

from services.english_test_generator import EngTestGenerator, WORD_LIST_GOOGLE_SHEET_URL

logger = logging.getLogger(__name__)


class EnglishHomeView(TemplateView):
    template_name = "english/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["base_google_sheet_url"] = WORD_LIST_GOOGLE_SHEET_URL
        return context


class AllWordSingleColListView(TemplateView):
    template_name = "english/word_list_1col.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["words"] = EngTestGenerator.generate_by_google_sheet_url().items()
        return context


class AllWord2ColsListView(TemplateView):
    template_name = "english/word_list_2cols.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["words"] = EngTestGenerator.get_2col_word_list()
        return context


class EnglishTestGeneratorView(TemplateView):
    template_name = "english/generator.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["url"] = WORD_LIST_GOOGLE_SHEET_URL
        return context


class EnglishWordTestListView(TemplateView):
    template_name = "english/word_test_list_2cols.html"

    def post(self, request: WSGIRequest, *args, **kwargs):
        try:

            value_list = EngTestGenerator.get_2col_word_list(
                request.POST["url"],
                int(request.POST["startIdx"]),
                int(request.POST["endIdx"]),
            )
            random.shuffle(value_list)
            question_count = int(request.POST["questionCount"])
            context = self.get_context_data(**kwargs)

            line_cut = int(question_count / 2)
            context["words"] = value_list[:line_cut]
            context["startIdx"] = request.POST["startIdx"]
            context["endIdx"] = request.POST["endIdx"]
            context["question_count"] = question_count

            return self.render_to_response(context)

        except Exception as e:
            logger.error(traceback.format_exc())
            messages.error(request, f"시험지 생성 실패: {e}")
            return HttpResponseBadRequest()
