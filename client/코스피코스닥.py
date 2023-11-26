'''
상장되어 있는 종목들을 가져온다.
그리고 인덱스, 코덱스, 인버스 같은 상품들도 같이 불러오기 때문에
가져온 종목들 중에서 그러한 종목들을 제외되도록 직접 필터링을 직접 해줘야한다.
'''

from requests import post
from icecream import ic
import datetime
import json
import csv
import os


# class 메인:
#     def __init__(self):
        
#         accessToken = self.로그인()
#         ic("접근키 확인", accessToken)

#         종목들 = TR요청들().코스피코스닥(accessCode=accessToken)
#         ic(종목들)

#     def 로그인(self) -> str:
#         url = "https://openapi.ebestsec.co.kr:8080/oauth2/token"
#         headers = {"Content-type": "application/x-www-form-urlencoded"}
#         body = {
#             "grant_type": "client_credentials",
#             "appkey": " PSZmG6ZONgejhZUpa8FGkb9hBPi107y1FMZg",
#             "appsecretkey": "2L3NKwyRDFi1DmOkCgp6jaMeShlDtO3z",
#             "scope": "oob",
#         }

#         response = post(url, headers=headers, data=body)

#         return response.json()["access_token"]


class PriceRequestHandler:
    def stock_code_request(self, accessCode):
        url = "https://openapi.ebestsec.co.kr:8080/stock/market-data"
        headers = {
            "Content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {accessCode}",
            "tr_cont": "N",
            "tr_cd": "t9945",
            "tr_cont_key": "",
        }
        # gubun: 1(코스피) / 2(코스닥)
        # Fetch data for both gubun: 1 and gubun: 2 and combine them
        combined_results = []
        for gubun in ['1','2']:
            body = {"t9945InBlock": {"gubun": gubun}} 
            response = post(url, headers=headers, data=json.dumps(body))
            results = response.json()["t9945OutBlock"]
            if results:
                for result in results:
                    result['gubun'] = gubun  # Add 'gubun' key to each entry
                combined_results.extend(results)

            #combined_results.extend(results or [])
        
        self.save_to_csv(combined_results, 'stock_code.csv')
        #RESPONSE BODY상세내역

        # hname: 종목명
        # shcode: 단축코드
        # expcode: 확장코드
        # etfchk: ETF구분
        # filler: filler
        return combined_results
        
    def save_to_csv(self, data, filename):
        # data폴더 존재여부 확인
        if not os.path.exists('..\\data'):
            os.makedirs('..\\data')

        #save the CSV file in the data folder
        filepath = os.path.join('..\\data', filename)
        keys = data[0].keys() if data else []
        with open(filepath, 'w', newline='', encoding='cp949') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)


def time_format():
    return f"{datetime.datetime.now()}|> "


#ic.configureOutput(prefix=time_format)

#메인()
