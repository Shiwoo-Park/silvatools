import ast
import html
import hashlib
import json
import logging
import random
import re
import string
import traceback
import uuid
from datetime import datetime
from typing import Dict

from rest_framework.request import Request

logger = logging.getLogger(__name__)


def get_date_str(dateobj=None, dformat=None):
    if dateobj is None:
        dateobj = datetime.now()
    if dformat is None:
        dformat = "%Y-%m-%d %H%M%S"
    return dateobj.strftime(dformat)


def get_date_args(date: datetime) -> dict:
    date_str = date.strftime("%Y-%m-%d")
    year, month, day = date_str.split("-")
    return {"year": year, "month": month, "day": day}


def make_html_element_attr_str(dic):
    """Dictionary 를 넣으면 HTML element의 속성 스트링으로 변환
    input EX: {attr1:val1, attr2:val2}
    output EX: " attr1=val1 attr2=val2 "
    """
    if not dic:
        return ""
    ret_list = []
    for k, v in dic.items():
        ret_list.append('%s="%s"' % (k, v))
    return " %s " % " ".join(ret_list)


def get_uuid_32():
    return "".join(str(uuid.uuid4()).split("-"))


def get_hash_sha256(source: str):
    """SHA-256 Hash 의 hex 값을 리턴한다. 길이=64"""
    try:
        return hashlib.sha256(source.encode()).hexdigest()
    except:
        logger.error("get_hash_sha256: Failed to make SHA-256 hash [%s]" % source)


def get_hash_md5(source: str):
    """ MD5 Hash 의 hex 값을 리턴한다. 길이=32"""
    try:
        return hashlib.md5(source.encode()).hexdigest()
    except:
        logger.error("get_hash_md5: Failed to make MD5 hash [%s]" % source)


def get_list_from_string(data: str) -> list:
    """ 스트링을 리스트로 convert """
    the_list = data.split("__|__")
    # 빈 문자열을 제거
    the_list = list(filter(None, the_list))
    return the_list


def is_email(s: str) -> bool:
    regex = re.compile("\w+@\w+\.[\.\w]+")
    m = regex.match(s)
    return m is not None


def convert_to_dict(str):
    return ast.literal_eval(str)


def json_parse(json_string):
    try:
        # return json.loads(json_string)
        return json.JSONDecoder().decode(json_string)
    except:
        print("[ERROR] JSON 파싱 실패 : ", json_string)
        traceback.print_exc()
        return dict()


def parse_list(str_list):
    try:
        return ast.literal_eval(str_list)  # parse ['1', '2', '3'] into list
    except:
        print("[ERROR] JSON 생성 실패 : ", str_list)
        return ""


def json_stringify(dic: Dict) -> str:
    try:
        return json.JSONEncoder().encode(dic)
    except:
        print("[ERROR] JSON 생성 실패 : ", dic)
        return ""


def replace_url_by_protocol(request: Request, url: str) -> str:
    if request.is_secure():
        return url.replace("http:", "https:", 1)
    else:
        return url


def is_url(s, allowed_schemes=()):
    additional_scheme = (
        "|{}".format("|".join(allowed_schemes)) if allowed_schemes else ""
    )
    regex = re.compile(
        rf"^(?:http|ftp{additional_scheme})s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    m = re.match(regex, s)
    if m:
        return True
    return False


def is_number(src):
    try:
        int(src)
        return True
    except:
        return False


def is_hex_color(s):
    if not s:
        return False
    regex = re.compile("^#([A-Fa-f0-9]{8}|[A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
    if regex.match(s):
        return True
    return False


def html_escape(text, include_quote=True):
    return html.escape(text, quote=include_quote)


def html_unescape(text):
    return html.unescape(text)


def to_camelcase(underscored):
    words = underscored.split("_")

    for i in range(1, len(words)):
        words[i] = words[i].capitalize()

    return "".join(words)


def camel_to_snakecase(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def replace_texts_by_match(regex, text, replace_text="***"):
    """
    입력한 regex 안의 괄호로 지정한 영역을
    replace_text 로 치환하는 함수

    :param regex: regex 문자열 or compiled regex
    :param text:  입력 문자열
    :param replace_text: 치환할 문자열
    :return: 치환이 완료된 문자열
    """

    def repl_func(m):
        text = m.group(0)
        groups = m.groups()

        for i in range(len(groups)):
            if groups[i] is not None:
                text = text.replace(groups[i], replace_text)

        return text

    return re.sub(regex, repl_func, text)


def get_random_str(length, letter: bool = True, number: bool = True):
    candidates = ""
    if letter:
        candidates += string.ascii_letters
    if number:
        candidates += "0123456789"

    if len(candidates) == 0:
        raise Exception("랜덤 문자열 생성 오류: 최소 1개 이상의 문자열 후보가 있어야 합니다.")

    return "".join(random.sample(candidates, length))


def to_camel_case(snake_str):
    """
    :param snake_str: snake_case_str
    :return: camelCase 문자열 snakeCaseStr
    """
    components = snake_str.split("_")
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + "".join(x.title() for x in components[1:])


def to_pascal_case(snake_str):
    """
    :param snake_str: snake_case_str
    :return: PascalCase 문자열 SnakeCaseStr
    """
    components = snake_str.split("_")
    return "".join(x.title() for x in components)


def get_random_str_for_redeem(length: int = 0, is_alpha_num: bool = True):
    """
    리딤코드 랜덤 문자열 생성
    :param length 문자열 길이:
    :param is_alpha_num 리딤코드 생성 문자열 선태 플래그:
    :return:
    """
    prevent_confuse_l_a = "A,B,C,D,E,F,G,H,J,K,L,M,N,P,Q,R,S,T,U,V,W,X,Y,Z,2,3,4,5,6,7,8,9".split(
        ","
    )
    prevent_confuse_l = "A,B,C,D,E,F,G,H,J,K,L,M,N,P,Q,R,S,T,U,V,W,X,Y,Z".split(",")

    if is_alpha_num:
        return "".join(random.sample(prevent_confuse_l_a, length))
    else:
        return "".join(random.sample(prevent_confuse_l, length))
