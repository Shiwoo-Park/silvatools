import logging
import os
import random
import time
from datetime import datetime

from django.conf import settings
from django.core.files.images import get_image_dimensions
from django.http import HttpResponse
from requests import Response

logger = logging.getLogger(__name__)


def write_tempfile(file):
    rd = random.randint(1, 1000)
    st = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
    filename = "%s_%.4d_%s" % (st, rd, file._name)

    print("write_tempfile: %s" % filename)
    tempfile = "%s/%s/%s" % (settings.BASE_DIR, "tmp_files", filename)
    fp = open(tempfile, "wb")
    for chunk in file.chunks():
        fp.write(chunk)
    fp.close()

    return tempfile


def delete_tempfile(filepath):
    print("delete_tempfile: %s" % filepath)
    os.remove(filepath)


def get_file_type(file):
    """ 자동으로 content_type 을 찾아준다 (광고 content 테이블에 쓰임) """

    ret = file.content_type
    if file.content_type.startswith("video/"):
        if file.content_type == "video/mp4":
            ret = "VIDEO_MP4"
        else:
            ret = "VIDEO"
    elif file.content_type.startswith("image/"):
        try:
            w, h = get_image_dimensions(file)
            ret = "IMAGE_%sx%s" % (w, h)
        except Exception as e:
            ret = "IMAGE"
    # print("get_file_type: file.content_type=", file.content_type, ' / RETURN = ', ret)
    return ret


def get_file_info(file):
    ret = dict()
    ret["extension"] = file.name.split(".")[-1]
    ret["name"] = file.name
    ret["size"] = file.size
    ret["content_type"] = file.content_type
    if file.content_type.startswith("image/"):
        w, h = get_image_dimensions(file)
        ret["width"] = w
        ret["height"] = h
    # print("get_file_info: ", ret)
    return ret


def is_image(file):
    if not file:
        raise Exception("파일 없습니다.")
    if not file.content_type:
        raise Exception("파일의 content_type 이 없습니다.")
    if file.content_type in settings.IMG_FILE_VALID_CONTENT_TYPE:
        return True
    return False


def save_file_from_response(response: Response, file_name: str) -> str:
    """
    :param response: 다운로드 할 csv 파일의 저장소 URL 을 requests 라이브러리를 사용하여 stream=True 로 받은 응답 객체
    :param file_name: 다운로드하여 저장할 파일명 (확장자 포함)
    :return: 다운로드 한 파일 path
    """

    file_path = f"{settings.TEMP_FILE_PATH}/{file_name}"

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, "wb") as f:
        # write by 1mb chunk
        for chunk in response.iter_content(1048576):
            f.write(chunk)

    logger.info(f"File download success: path={file_path}")
    return file_path


def make_file_download_response(
    file_path: str, content_type="text/plain"
) -> HttpResponse:
    """
    :param file_path: 서버로 다운로드 받은 파일 path
    :param content_type: http 응답의 content_type 헤더값
    :return: HttpResponse
    """
    if os.path.exists(file_path):
        with open(file_path, "rb") as fh:
            response = HttpResponse(fh.read(), content_type="text/csv")
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                file_path
            )
            return response

    raise FileNotFoundError
