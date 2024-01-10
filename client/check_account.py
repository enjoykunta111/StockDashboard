'''
잔고내역을 반복요청하는 이유는 주문이 잘 이루어졌는지 계속 확인하기 위해서이다.
주문을 넣고나면 "주문 데이터를 실시간으로 받는 함수"가 따로 있다. 하지만 이를 제어하려면 고도화된 코딩을 해야된다.
시간이 오래 걸리는 작업인 만큼, 쉽게 할 수 있는 방법이 잔고내역의 종목의 주문수량 상태와 단일가를 확안하면서 주문처리가 잘 됐는지 확인하면 된다.
'''

import asyncio
from requests import post
import json
import socket

    
class CheckAccountHandler:
    def __init__(self, conn,callback):
        self.callback=callback
        self.conn = conn
        self.보유종목들: list = []

    async def start_check(self, accessToken, conn):
        #accessToken = self.로그인()
        #ic("접근키 확인", accessToken)

        await TR요청들().주식잔고반복요청(accessCode=accessToken, callbackListener=self.잔고반복요청수신)

    def 잔고반복요청수신(self, results):
        #ic(results)
        if self.callback:
            self.callback(results, self.conn) #결과를 main.py에 전송


class TR요청들:
    

    async def 주식잔고(self, accessCode):
        url = "https://openapi.ebestsec.co.kr:8080/stock/accno"
        headers = {
            "Content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {accessCode}",
            "tr_cont": "N",
            "tr_cd": "t0424",
            "tr_cont_key": "",
        }
        body = {
            "t0424InBlock": {
                "prcgb": "",
                "chegb": "",
                "dangb": "",
                "charge": "",
                "cts_expcode": "",
            }
        }

        response = post(url, headers=headers, data=json.dumps(body))
        results: list = response.json()["t0424OutBlock1"]
        return results or []

    async def 주식잔고반복요청(self, accessCode, callbackListener):
        while True:
            await asyncio.sleep(2)
            results = await self.주식잔고(accessCode)
            callbackListener(results)


# python 3.6 이하에서 사용
# loop = asyncio.get_event_loop()
# loop.run_until_complete(메인().시작())
# loop.close()

# python 3.7 이후 사용, 최신 형태를 추천
#asyncio.run(메인().시작())

# 또 다른 비동기 표현방식
# async def main_async():
#     task = asyncio.create_task(메인().시작())  # 비동기 태스크를 생성
#     await asyncio.sleep(0.1)  # 비동기 태스크가 시작될 수 있도록 잠시 대기

#     # 태스크가 종료될 때까지 대기하는 것을 원한다면 아래 코드를 사용
#     await task

# asyncio.run(main_async())
