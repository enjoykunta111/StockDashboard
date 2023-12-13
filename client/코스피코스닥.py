'''
상장되어 있는 종목들을 가져온다.
그리고 인덱스, 코덱스, 인버스 같은 상품들도 같이 불러오기 때문에
가져온 종목들 중에서 그러한 종목들을 제외되도록 직접 필터링을 직접 해줘야한다.
'''

'''
일봉들 요청에서는 재귀함수를 사용한다.
재귀함수는 구조만 알면 아주아주 간단한 용어이다.

같은 내용을 조건에 따라 반복하게 만드는 것이라고 보면된다.
일봉 요청은 한번에 500일치를 가져올 수 있다. 그 이상 가져오려면 또 요청해야 하는데, 이때 재귀함수를 사용하면 된다.
'''

from requests import post
import asyncio
from icecream import ic
import datetime
import json
import csv
import os

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
        
    # 종목코드 csv로 export
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


    # csv속 종목코드들의 일자별 Price data db에 저장하기 (csv로 뽑기부터 해보기)
    #아래 메소드는 어디서 불러오는게 맞을까??
    async def stock_price_request(self, accessCode,gubun,shcode,sdate, edate, tr_cont, tr_cont_key, cts_date):
        url = "https://openapi.ebestsec.co.kr:8080/stock/chart"
        headers = {
            "Content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {accessCode}",
            "tr_cd": "t8410",
            "tr_cont": tr_cont,
            "tr_cont_key": tr_cont_key,
        }                    
                                                                                                                                       
        body = {
            "t8410InBlock": {
                "shcode": shcode,
                "gubun": "2",
                "qrycnt": 500,
                "sdate": sdate,
                "edate": cts_date or edate,
                # cts_date로만 조회가 먹히질 않음. 그러므로 edate를 바꿔가며 조회가 필요함, 결국 연속조회에서 cts_date를 넣지 않아도 됨.
                # 또한 해당 날짜일 포함하여 검색된다.
                "cts_date": "",
                "comp_yn": "N",
                "sujung": "Y",
            }
        }
      
        print(url+'\n')
        ic(headers)

        response = post(url, headers=headers, data=json.dumps(body))
        headers = response.headers
        rTrContKey = headers["tr_cont_key"]
        rTrCont = headers["tr_cont"]
        
        ic(body)
        
        
        
        
        print('rTr후')
        #ic(response)
        ctsResult = response.json()["t8410OutBlock"]
        rCtsDate = ctsResult["cts_date"]
        ic(rTrContKey)
        ic(rTrCont)
        ic(rCtsDate)
        response.json()["t8410OutBlock1"]

        # if rTrCont == "Y":
        #     await asyncio.sleep(2)
        #     await self.일봉들요청(
        #         accessCode=accessCode,
        #         tr_cont=tr_cont,
        #         tr_cont_key=rTrContKey,
        #         cts_date=rCtsDate,
        #     )

        #print(response.json()["t8410OutBlock1"])


def time_format():
    return f"{datetime.datetime.now()}|> "


#ic.configureOutput(prefix=time_format)

#메인()
