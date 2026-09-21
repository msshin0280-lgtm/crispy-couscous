def find_account(data, keywords):
    for item in data:
        name = item.get("account_nm", "")

        if any(keyword in name for keyword in keywords):
            try:
                return float(item.get("thstrm_amount", 0).replace(",", ""))
            except (ValueError, AttributeError):
                return 0

    return 0


def analyze(data):
    revenue = find_account(data, ["매출액", "수익(매출액)"])
    operating_profit = find_account(data, ["영업이익"])
    net_income = find_account(data, ["당기순이익"])

    assets = find_account(data, ["자산총계"])
    liabilities = find_account(data, ["부채총계"])
    equity = find_account(data, ["자본총계"])

    current_assets = find_account(data, ["유동자산"])
    current_liabilities = find_account(data, ["유동부채"])

    result = {
        "revenue": revenue,
        "operating_profit": operating_profit,
        "net_income": net_income,
        "total_assets": assets,
        "total_liabilities": liabilities,
        "total_equity": equity,
        "current_assets": current_assets,
        "current_liabilities": current_liabilities,
        "ratios": {
            "operating_margin": (
                operating_profit / revenue * 100
                if revenue else 0
            ),
            "net_margin": (
                net_income / revenue * 100
                if revenue else 0
            ),
            "roa": (
                net_income / assets * 100
                if assets else 0
            ),
            "roe": (
                net_income / equity * 100
                if equity else 0
            ),
            "debt_ratio": (
                liabilities / equity * 100
                if equity else 0
            ),
            "current_ratio": (
                current_assets / current_liabilities * 100
                if current_liabilities else 0
            )
        }
    }

    return result
