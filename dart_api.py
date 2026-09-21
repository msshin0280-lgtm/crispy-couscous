import os
import requests

API_KEY = os.environ["DART_API_KEY"]
BASE_URL = "https://opendart.fss.or.kr/api"

SAMSUNG_CORP_CODE = "00126380"


def get_financial_statements(year, report_code="11011"):
    """
    report_code
    11011 = 사업보고서
    11012 = 반기보고서
    11013 = 1분기보고서
    11014 = 3분기보고서
    """

    url = f"{BASE_URL}/fnlttSinglAcntAll.json"

    params = {
        "crtfc_key": API_KEY,
        "corp_code": SAMSUNG_CORP_CODE,
        "bsns_year": str(year),
        "reprt_code": report_code,
        "fs_div": "CFS"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    if data.get("status") != "000":
        raise RuntimeError(
            f"DART API 오류: {data.get('status')} - {data.get('message')}"
        )

    return data.get("list", [])
