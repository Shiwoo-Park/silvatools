import sys, logging
import traceback
from typing import Dict

import requests
from django.conf import settings

from common.exceptions import DownloadError

logger = logging.getLogger(__name__)

WORD_FILE_PATH = f"{settings.BASE_DIR}/resources/english/toeic_frequent_words"
WORD_LIST_GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1eU9HsDJfd6U6W_pqP5nG9qfCf2nN-2-M9eFZM_8PGfE/edit?usp=sharing"
NAVER_DICT_SEARCH_URL_PREFIX = "https://en.dict.naver.com/#/search?query="


class EngTestGenerator:
    @staticmethod
    def generate_by_file(path=WORD_FILE_PATH, start=0, end=sys.maxsize) -> Dict:
        ret = {}
        f = open(path)

        while True:
            try:
                line = f.readline()
                if not line:
                    break
                idx, word, meaning = line.strip().split("\t")
                naver_dic_url = (
                    f"{NAVER_DICT_SEARCH_URL_PREFIX}{'%20'.join(word.split())}"
                )
                if start <= int(idx) <= end:
                    ret[word] = {
                        "idx": idx,
                        "word": word,
                        "meaning": meaning,
                        "naver_dic_url": naver_dic_url,
                    }
            except Exception as e:
                logger.error(f"단어 파싱 실패: line = {line}\n{traceback.format_exc()}")

        f.close()
        return ret

    @staticmethod
    def generate_by_url(
        google_sheet_url=WORD_LIST_GOOGLE_SHEET_URL, start=0, end=sys.maxsize
    ) -> Dict:
        """
        URL 포맷을 바꿔주어야 함
        before: https://docs.google.com/spreadsheets/d/1eU9HsDJfd6U6W_pqP5nG9qfCf2nN-2-M9eFZM_8PGfE/edit?usp=sharing
        after: https://docs.google.com/spreadsheets/d/1eU9HsDJfd6U6W_pqP5nG9qfCf2nN-2-M9eFZM_8PGfE/export?format=csv

        :param google_sheet_url: A열에 ID, B열에 영단어, C열에 뜻 이 적힌 Google Sheet URL
        :param start, end: 추출 하고자 하는 ID 구간
        :return: { 영단어: {idx: ID, meaning: 뜻}, ... }
        """
        google_sheet_url = google_sheet_url.split("/")
        google_sheet_url = f"{'/'.join(google_sheet_url[:-1])}/export?format=csv"

        ret = {}
        res = requests.get(google_sheet_url)

        if res.status_code != 200:
            msg = "Google Spread Sheet 에서 데이터 불러오기 실패"
            logger.error(msg)
            raise DownloadError(msg)

        lines = res.content.decode("utf-8").split("\n")
        for line in lines:
            tarr = line.strip().split(",")
            if len(tarr) < 3:
                continue

            idx, word, meaning = tarr[0], tarr[1], ",".join(tarr[2:])
            if "" in [idx, word, meaning]:
                continue

            word = word.lower()
            meaning = meaning[1:-1] if meaning[0] == '"' else meaning
            naver_dic_url = f"{NAVER_DICT_SEARCH_URL_PREFIX}{'%20'.join(word.split())}"
            if start <= int(idx) <= end:
                ret[word] = {
                    "idx": idx,
                    "word": word,
                    "meaning": meaning,
                    "naver_dic_url": naver_dic_url,
                }

        return ret
