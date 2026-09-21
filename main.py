import os
import json
import requests
import pandas as pd

DART_API_KEY = os.environ.get("DART_API_KEY")
CORP_CODE = "00126380"  # 삼성전자 고유번호

def get_financial_data(year, reprt_code="11011"):
    """
    reprt_code:
    11013: 1분기, 11012: 반기, 11014: 3분기, 11011: 사업보고서(4분기)
    """
    url = "https://opendart.fss.or.kr/api/fnlttSinglAcct.json"
    params = {
        "crtfc_key": DART_API_KEY,
        "corp_code": CORP_CODE,
        "bsns_year": str(year),
        "reprt_code": reprt_code
    }
    
    res = requests.get(url, params=params)
    data = res.json()
    
    if data.get("status") != "000":
        print(f"Error fetching data for {year}: {data.get('message')}")
        return None
        
    return data.get("list", [])

def parse_financials(years):
    records = []
    
    for year in years:
        items = get_financial_data(year)
        if not items:
            continue
            
        data_dict = {"year": str(year)}
        
        for item in items:
            account_nm = item.get("account_nm")
            amount_str = item.get("thstrm_amount", "0").replace(",", "")
            
            try:
                amount = float(amount_str)
            except ValueError:
                amount = 0.0
                
            if account_nm in ["매출액", "수익(매출액)"]:
                data_dict["revenue"] = amount
            elif account_nm in ["영업이익", "영업이익(손실)"]:
                data_dict["operating_income"] = amount
            elif account_nm in ["당기순이익", "당기순이익(손실)"]:
                data_dict["net_income"] = amount
            elif account_nm == "자산총계":
                data_dict["total_assets"] = amount
            elif account_nm == "부채총계":
                data_dict["total_liabilities"] = amount
            elif account_nm == "자본총계":
                data_dict["total_equity"] = amount
                
        # 주요 재무비율 계산
        revenue = data_dict.get("revenue", 0)
        op_inc = data_dict.get("operating_income", 0)
        net_inc = data_dict.get("net_income", 0)
        assets = data_dict.get("total_assets", 0)
        liab = data_dict.get("total_liabilities", 0)
        equity = data_dict.get("total_equity", 0)
        
        data_dict["op_margin"] = round((op_inc / revenue * 100), 2) if revenue else 0
        data_dict["net_margin"] = round((net_inc / revenue * 100), 2) if revenue else 0
        data_dict["debt_ratio"] = round((liab / equity * 100), 2) if equity else 0
        data_dict["roe"] = round((net_inc / equity * 100), 2) if equity else 0
        
        records.append(data_dict)
        
    return records

if __name__ == "__main__":
    target_years = [2021, 2022, 2023, 2024, 2025]
    result_data = parse_financials(target_years)
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
        
    print("DART financial data successfully updated & saved to data.json")
