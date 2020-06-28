from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.request import Request


def get_client_ip(request: WSGIRequest = None, drf_request: Request = None):
    if drf_request:
        request = drf_request._request

    if not request:
        raise ValidationError("접속 ip 확인 실패: request 객체가 없습니다")

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
