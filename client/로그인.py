'''
모든 증권 시스템의 시작은 로그인이다.
RestAPI에서는 아이디와 패스워드를 입력하지 않고 appkey와 secret key를 이용해서 증권사에 고객이라는 것을 알려준다.
그리고 반환 받은 토큰으로 데이터를 요청하면 된다.
'''

from requests import post
from icecream import ic
import datetime


def time_format():
    #f는 파이썬3.6부터 이용 가능한 괄호 안에 데이터를 넣을 수 있는 표현식을 의미할때 적는다.
    return f"{datetime.datetime.now()}|> "
ic.configureOutput(prefix=time_format)

class LoginHandler:
    # def __init__(self):
    #     global accessToken
    #     accessToken = self.로그인()

        #ic("접근키 확인", accessToken)
        

    def login(self) -> str:
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

