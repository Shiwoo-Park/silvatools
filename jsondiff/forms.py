from django import forms


class TwoUrlsForm(forms.Form):
    url1 = forms.URLField(
        label="URL1", initial="http://127.0.0.1:8000/jsondiff/sample1"
    )
    url2 = forms.URLField(
        label="URL2", initial="http://127.0.0.1:8000/jsondiff/sample2"
    )

    # url1 = forms.URLField(
    #     label="URL1",
    #     initial="http://alpha-api2-page.kakao.com/api/v9/store/section_container/list",
    # )
    # url2 = forms.URLField(
    #     label="URL2",
    #     initial="http://dev-api2-page.kakao.com/api/v9/store/section_container/list",
    # )
