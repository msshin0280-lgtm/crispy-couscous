def to_number(value):
    """DART의 숫자 문자열을 숫자로 변환"""
    if value is None:
        return 0.0

    try:
        return float(str(value).replace(",", "").strip())
    except (ValueError, TypeError):
        return 0.0


def find_account(data, names):
    """
    DART 재무제표에서 계정과목을 찾습니다.
    정확히 일치하는 계정을 우선 검색합니다.
    """

    # 1. 정확히 일치
    for item in data:
        account_name = item.get("account_nm", "").strip()

        if account_name in names:
            return to_number(item.get("thstrm_amount"))

    # 2. 부분 일치
    for item in data:
        account_name = item.get("account_nm", "").strip()

        for name in names:
            if name in account_name:
                return to_number(item.get("thstrm_amount"))

    return 0.0


def calculate_ratio(numerator, denominator):
    if denominator == 0:
        return None

    return numerator / denominator * 100


def analyze(data):
    """DART 재무데이터에서 주요 재무수치와 재무비율을 계산"""

    revenue = find_account(
        data,
        [
            "매출액",
            "수익(매출액)"
        ]
    )

    operating_profit = find_account(
        data,
        [
            "영업이익",
            "영업이익(손실)"
        ]
    )

    net_income = find_account(
        data,
        [
            "당기순이익",
            "당기순이익(손실)"
        ]
    )

    total_assets = find_account(
        data,
        [
            "자산총계"
        ]
    )

    total_liabilities = find_account(
        data,
        [
            "부채총계"
        ]
    )

    total_equity = find_account(
        data,
        [
            "자본총계"
        ]
    )

    current_assets = find_account(
        data,
        [
            "유동자산"
        ]
    )

    current_liabilities = find_account(
        data,
        [
            "유동부채"
        ]
    )

    return {
        "revenue": revenue,
        "operating_profit": operating_profit,
        "net_income": net_income,

        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "total_equity": total_equity,

        "current_assets": current_assets,
        "current_liabilities": current_liabilities,

        "ratios": {
            "operating_margin": calculate_ratio(
                operating_profit,
                revenue
            ),

            "net_margin": calculate_ratio(
                net_income,
                revenue
            ),

            "roa": calculate_ratio(
                net_income,
                total_assets
            ),

            "roe": calculate_ratio(
                net_income,
                total_equity
            ),

            "debt_ratio": calculate_ratio(
                total_liabilities,
                total_equity
            ),

            "current_ratio": calculate_ratio(
                current_assets,
                current_liabilities
            )
        }
    }
