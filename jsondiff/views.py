import difflib
import json

import requests
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from jsondiff.forms import TwoUrlsForm


class JsonDiffHomeView(FormView):
    form_class = TwoUrlsForm
    template_name = "jsondiff/index.html"
    context_add = {}

    def dispatch(self, request, *args, **kwargs):
        self.context_add = {"error_msg": "", "success_msg": ""}
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("jsondiff:index")

    def _get_unified_diff_by_responses(self, json_data1, json_data2):
        try:
            json_list1 = json.dumps(json_data1, indent=4).split("\n")
            json_list2 = json.dumps(json_data2, indent=4).split("\n")
            json_list1 = [f"{line}\n" for line in json_list1]
            json_list2 = [f"{line}\n" for line in json_list2]
            diff_text = difflib.unified_diff(
                json_list1, json_list2, fromfile="URL 1", tofile="URL 2"
            )
            diff_text = "".join(list(diff_text))
            return diff_text

        except Exception as e:
            raise Exception(
                "Making diff string failed... (json parsing or response error)"
            )

    def form_valid(self, form):
        context = self.get_context_data()

        try:
            r1 = requests.get(form.cleaned_data["url1"], timeout=3)
            r2 = requests.get(form.cleaned_data["url2"], timeout=3)
            data1 = r1.json()
            data2 = r2.json()
            context["unified_diff"] = self._get_unified_diff_by_responses(data1, data2)
            self.context_add["success_msg"] = "Success !!!"
        except Exception as e:
            self.context_add["error_msg"] = f"Http Request Failed: {e}"

        for k, v in self.context_add.items():
            context[k] = v

        return self.render_to_response(context)


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
