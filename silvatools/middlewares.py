import logging
import traceback
from datetime import datetime
from time import time
from typing import Dict
from urllib.parse import urlencode

from django.conf import settings
from django.http import QueryDict
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

from utils import file_util, http_util

logger = logging.getLogger()
req_logger = logging.getLogger("request")


class RequestLoggerMiddleware(MiddlewareMixin):
    """
    request 정보를 로그로 남기위한 미들웨어

    req_logger 는 requests.log 라는 별도의 파일에
    정확히 요청 & 응답 기록만을 남기기위해 따로 로깅을 하도록 한다.
    """

    ATTR_REQ_LOG_UID = "myapp_reqlog_uid"
    ATTR_REQ_START_TIME = "myapp_reqlog_start_time"
    ATTR_REQ_ENTER_LOG = "myapp_reqlog_enter_log"

    def __get_req_log_data(self, req) -> Dict:
        req_id = getattr(req, self.ATTR_REQ_LOG_UID)
        request_info = {"path": req.path, "data": dict(), "file": dict()}

        # 주의: 아래 코드 지우지 말것 !!!
        trick_code = req.body

        # 입력 param 또는 data 수집
        if req.method == "GET":
            if len(req.GET) > 0:
                request_info["path"] = req.path + "?" + urlencode(dict(req.GET))
        elif req.method == "POST":
            request_info["data"] = dict(req.POST)
        elif req.method in ["PUT", "DELETE"]:
            if len(req.GET) > 0:
                request_info["path"] = req.path + "?" + urlencode(dict(req.GET))
            request_info["data"] = dict(QueryDict(req.body))

        # 업로드 파일 데이터 수집
        if hasattr(req, "FILES") and len(req.FILES):
            for input_name in req.FILES:
                file_info = file_util.get_file_info(req.FILES[input_name])
                request_info["file"][input_name] = "[%s] %s (%s)" % (
                    file_info["content_type"],
                    file_info["name"],
                    file_info["size"],
                )
        client_ip = http_util.get_client_ip(req)

        # 로깅 텍스트 완성
        final_log_text = f"[#{req_id}] Request by IP: {client_ip} - {req.method} {request_info['path']}"

        # 입력 정보 개행하여 추가
        if len(request_info["file"]) > 0:
            final_log_text += "\n    INPUT FILE: %s" % request_info["file"]

        if len(request_info["data"]) > 0:
            final_log_text += "\n    INPUT DATA: %s" % request_info["data"]

        return {
            "log_text": final_log_text,
        }

    def __set_req_attrs(self, req):
        req_id = str(int(time() * 1000000))
        setattr(req, self.ATTR_REQ_LOG_UID, req_id)
        setattr(req, self.ATTR_REQ_START_TIME, datetime.now())

    def process_request(self, request):
        self.__set_req_attrs(request)
        request_log_data = self.__get_req_log_data(request)
        logger.info("request ----- {}".format(request_log_data["log_text"]))

        setattr(request, self.ATTR_REQ_ENTER_LOG, request_log_data["log_text"])

    def process_exception(self, request, exception: Exception):
        logger.error("Exception handling request for {}".format(request.path))
        req_logger.error(traceback.format_exc())

    def process_response(self, request, response):
        if hasattr(request, self.ATTR_REQ_START_TIME):
            time_delta = datetime.now() - getattr(request, self.ATTR_REQ_START_TIME)
            time_delta = int(time_delta.total_seconds() * 1000)

            response_log = "[#{}] Response Code - {} ({} ms)".format(
                getattr(request, self.ATTR_REQ_LOG_UID),
                str(response.status_code),
                time_delta,
            )
            logger.info("response ----- {}\n".format(response_log))

            # 진입시 와 응답시 로그를 합쳐서 한꺼번에 남긴다
            # (logstash 에서 단일 리퀘스트로 인식할때 용이하도록 하기 위하여)
            full_request_log = "{}\n  {}".format(
                getattr(request, self.ATTR_REQ_ENTER_LOG), response_log
            )
            req_logger.info(full_request_log)

        return response
