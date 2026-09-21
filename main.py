import json
import os
from datetime import datetime

from dart_api import get_financial_statements
from financial_analysis import analyze


DATA_FILE = "data.json"

# 삼성전자
COMPANY_NAME = "삼성전자"
CORP_CODE = "00126380"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "company": COMPANY_NAME,
            "corp_code": CORP_CODE,
            "updated_at": None,
            "financials": {}
        }

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


def collect_year(year):
    print(f"{year}년 삼성전자 사업보고서 조회 중...")

    raw_data = get_financial_statements(
        year=year,
        report_code="11011"
    )

    if not raw_data:
        print(f"{year}년 데이터가 없습니다.")
        return None

    result = analyze(raw_data)

    return {
        "year": year,
        "report_type": "사업보고서",
        "collected_at": datetime.now().isoformat(),
        "financials": result
    }


def main():

    data = load_data()

    # 최근 3개 사업연도 조회
    current_year = datetime.now().year

    years = [
        current_year - 1,
        current_year - 2,
        current_year - 3
    ]

    for year in years:

        try:

            result = collect_year(year)

            if result is not None:

                data["financials"][str(year)] = result

                print(
                    f"{year}년 데이터 저장 완료"
                )

        except Exception as e:

            print(
                f"{year}년 처리 중 오류: {e}"
            )

    data["updated_at"] = datetime.now().isoformat()

    save_data(data)

    print("================================")
    print("삼성전자 재무 데이터 업데이트 완료")
    print("================================")


if __name__ == "__main__":
    main()
