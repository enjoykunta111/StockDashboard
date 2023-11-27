'''
일봉들 요청에서는 재귀함수를 사용한다.
재귀함수는 구조만 알면 아주아주 간단한 용어이다.

같은 내용을 조건에 따라 반복하게 만드는 것이라고 보면된다.
일봉 요청은 한번에 500일치를 가져올 수 있다. 그 이상 가져오려면 또 요청해야 하는데, 이때 재귀함수를 사용하면 된다.
'''

import asyncio
from requests import post
from icecream import ic
import datetime
import json

def time_format():
    return f"{datetime.datetime.now()}|> "
ic.configureOutput(prefix=time_format)

class 메인:
    def __init__(self):
        
        accessToken = self.로그인()
        ic("접근키 확인", accessToken)

        asyncio.run(
            TR요청들().일봉들요청(
                accessCode=accessToken, tr_cont="N", tr_cont_key="", cts_date=""
            )
        )

    def 로그인(self) -> str:
        url = "https://openapi.ebestsec.co.kr:8080/oauth2/token"
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": "client_credentials",
            "appkey": "PSZmG6ZONgejhZUpa8FGkb9hBPi107y1FMZg",
            "appsecretkey": "2L3NKwyRDFi1DmOkCgp6jaMeShlDtO3z",
            "scope": "oob",
        }

        response = post(url, headers=headers, data=body)

        return response.json()["access_token"]


class TR요청들:
    async def 일봉들요청(self, accessCode, tr_cont, tr_cont_key, cts_date):
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
                "shcode": "000250",
                "gubun": "2",
                "qrycnt": 500,
                "sdate": "20231101",
                "edate": cts_date or "20231110",
                # cts_date로만 조회가 먹히질 않음. 그러므로 edate를 바꿔가며 조회가 필요함, 결국 연속조회에서 cts_date를 넣지 않아도 됨.
                # 또한 해당 날짜일 포함하여 검색된다.
                "cts_date": "",
                "comp_yn": "N",
                "sujung": "Y",
            }
        }

        response = post(url, headers=headers, data=json.dumps(body))

        headers = response.headers
        rTrContKey = headers["tr_cont_key"]
        rTrCont = headers["tr_cont"]
        ic(headers)

        ctsResult = response.json()["t8410OutBlock"]
        rCtsDate = ctsResult["cts_date"]
        ic(rCtsDate)
        

        response.json()["t8410OutBlock1"]

        if rTrCont == "Y":
            await asyncio.sleep(2)
            await self.일봉들요청(
                accessCode=accessCode,
                tr_cont=tr_cont,
                tr_cont_key=rTrContKey,
                cts_date=rCtsDate,
            )

        print(response.json()["t8410OutBlock1"])

메인()
