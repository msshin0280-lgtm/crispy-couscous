import json
import os
from datetime import datetime

from dart_api import get_financial_statements
from financial_analysis import analyze


DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "financial_data.json")


def load_existing_data():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    current_year = datetime.now().year

    # 최근 사업연도부터 조회
    for year in range(current_year, current_year - 3, -1):

        try:
            raw = get_financial_statements(
                year,
                report_code="11011"
            )

            if not raw:
                continue

            analysis = analyze(raw)

            existing = load_existing_data()

            existing[str(year)] = {
                "company": "삼성전자",
                "year": year,
                "updated_at": datetime.now().isoformat(),
                "financials": analysis
            }

            save_data(existing)

            print(f"{year}년 데이터 업데이트 완료")

        except Exception as e:
            print(f"{year}년 처리 실패: {e}")


if __name__ == "__main__":
    main()
