import random, logging
import traceback

from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import TemplateView

from services.english_test_generator import EngTestGenerator, WORD_LIST_GOOGLE_SHEET_URL

logger = logging.getLogger(__name__)


class EnglishHomeView(TemplateView):
    template_name = "english/index.html"


class EnglishWordListView(TemplateView):
    template_name = "english/word_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["words"] = EngTestGenerator.generate_by_url().items()
        return context


class EnglishTestGeneratorView(TemplateView):
    template_name = "english/generator.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["url"] = WORD_LIST_GOOGLE_SHEET_URL
        return context


class EnglishWordTestListView(TemplateView):
    template_name = "english/word_test_list.html"

    def post(self, request: WSGIRequest, *args, **kwargs):
        try:
            word_data = EngTestGenerator.generate_by_url(
                request.POST["url"],
                int(request.POST["startIdx"]),
                int(request.POST["endIdx"]),
            )
            value_list = list(word_data.values())
            random.shuffle(value_list)
            questionCount = int(request.POST["questionCount"])

            context = self.get_context_data(**kwargs)
            context["words"] = value_list[:questionCount]
            context["startIdx"] = request.POST["startIdx"]
            context["endIdx"] = request.POST["endIdx"]
            context["questionCount"] = questionCount
            messages.success(request, "시험지 생성 성공")

            return self.render_to_response(context)

        except Exception as e:
            logger.error(traceback.format_exc())
            messages.error(request, f"시험지 생성 실패: {e}")
            return HttpResponseBadRequest()
