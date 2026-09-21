import os
import json
import requests

DART_API_KEY = os.environ.get("DART_API_KEY")
CORP_CODE = "00126380"  # 삼성전자 고유번호

def get_financial_data(year, reprt_code="11011"):
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
        print(f"[{year}] DART API응답 오류: {data.get('message')}")
        return []
        
    return data.get("list", [])

def parse_financials(years):
    records = []
    
    for year in years:
        items = get_financial_data(year)
        data_dict = {
            "year": str(year),
            "revenue": 0.0,
            "operating_income": 0.0,
            "net_income": 0.0,
            "total_assets": 0.0,
            "total_liabilities": 0.0,
            "total_equity": 0.0
        }
        
        for item in items:
            # CFS(연결재무제표) 또는 OFS(재무제표) 모두 대응
            account_nm = item.get("account_nm", "").strip()
            amount_str = item.get("thstrm_amount", "0").replace(",", "").strip()
            
            try:
                amount = float(amount_str)
            except ValueError:
                amount = 0.0
                
            if any(k in account_nm for k in ["매출액", "수익(매출액)", "매출"]):
                if data_dict["revenue"] == 0:
                    data_dict["revenue"] = amount
            elif "영업이익" in account_nm:
                if data_dict["operating_income"] == 0:
                    data_dict["operating_income"] = amount
            elif "당기순이익" in account_nm:
                if data_dict["net_income"] == 0:
                    data_dict["net_income"] = amount
            elif account_nm == "자산총계":
                data_dict["total_assets"] = amount
            elif account_nm == "부채총계":
                data_dict["total_liabilities"] = amount
            elif account_nm == "자본총계":
                data_dict["total_equity"] = amount
                
        revenue = data_dict["revenue"]
        op_inc = data_dict["operating_income"]
        net_inc = data_dict["net_income"]
        liab = data_dict["total_liabilities"]
        equity = data_dict["total_equity"]
        
        data_dict["op_margin"] = round((op_inc / revenue * 100), 2) if revenue else 0
        data_dict["net_margin"] = round((net_inc / revenue * 100), 2) if revenue else 0
        data_dict["debt_ratio"] = round((liab / equity * 100), 2) if equity else 0
        data_dict["roe"] = round((net_inc / equity * 100), 2) if equity else 0
        
        records.append(data_dict)
        
    return records

if __name__ == "__main__":
    # 최근 5개년 수치 수집
    target_years = [2020, 2021, 2022, 2023, 2024]
    result_data = parse_financials(target_years)
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
        
    print("DART 재무데이터 업데이트 완료")
