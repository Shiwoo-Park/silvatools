import difflib

import requests
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView

from utils import string_util


class JsonDiffHomeView(TemplateView):
    template_name = 'jsondiff/index.html'

    def _get_unified_diff(self, response1, response2):
        f1 = "/home/silva/PycharmProjects/silvatools/resources/sample_json1.json"
        f2 = "/home/silva/PycharmProjects/silvatools/resources/sample_json2.json"
        file1 = open(f1)
        file2 = open(f2)
        diff_text = difflib.unified_diff(file1.readlines(), file2.readlines(), fromfile="aaa", tofile="bbb")
        diff_text = string_util.html_unescape("".join(list(diff_text)))
        file1.close()
        file2.close()
        print(diff_text)
        return diff_text

    def _get_unified_diff_by_responses(self, res1: requests.Response, res2: requests.Response):
        # json dic 으로 받은다음에 Pretty print 해서 line 단위로 쪼개봐
        diff_text = difflib.unified_diff(res1.text.split(), res2.text.split(), fromfile="aaa", tofile="bbb")
        diff_text = string_util.html_unescape("".join(list(diff_text)))
        return diff_text

    def _get_responses(self):
        url1 = "http://127.0.0.1:8000/jsondiff/sample1"
        url2 = "http://127.0.0.1:8000/jsondiff/sample2"

        r1 = requests.get(url1)
        r2 = requests.get(url2)

        return r1, r2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["unified_diff"] = self._get_unified_diff(1, 2)
        context["unified_diff"] = self._get_unified_diff_by_responses(*self._get_responses())
        return context


def sample_json1(request):
    path = f"{settings.BASE_DIR}/resources/sample_json1.json"
    file = open(path)
    json_text = file.read()
    file.close()
    return HttpResponse(json_text)


def sample_json2(request):
    path = f"{settings.BASE_DIR}/resources/sample_json2.json"
    file = open(path)
    json_text = file.read()
    file.close()
    return HttpResponse(json_text)
