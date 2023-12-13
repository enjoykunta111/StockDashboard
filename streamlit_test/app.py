import streamlit as st
from requests import post
from apps import login,data,home


def get_access_token():
    BASE_URL = "https://openapi.ebestsec.co.kr:8080"
    PATH = 'oauth2/token'
    url = f"{BASE_URL}/{PATH}"
    #url = "https://openapi.ebestsec.co.kr:8080/oauth2/token"
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    body = {    
        "grant_type": "client_credentials",
        "appkey": "PSZmG6ZONgejhZUpa8FGkb9hBPi107y1FMZg",
        "appsecretkey": "2L3NKwyRDFi1DmOkCgp6jaMeShlDtO3z",
        "scope": "oob",
    }
    response = post(url, headers=headers, data=body)

    if response.status_code == 200:
        access_token = response.json()["access_token"]
        return access_token
    else:
        return None


st.set_page_config(
    page_title = "Main Page"
)
st.write('# Welcome to Streamlit')

#사이드바 메뉴 설정
login_btn = st.sidebar.button("로그인")
menu = st.sidebar.radio(
    "메뉴를 선택하세요",
    ("Home","Data Collect","Backtest")
)



if login_btn:
    token = get_access_token()
    
    if token:
        st.session_state['accesstoken'] = token
        st.info('로그인 성공')
        st.info(token)
        login.show_balance()
    else:
        st.info('로그인 실패')

if menu == "Data Collect":
    data.display_page_datacollect()
if menu == "Home":
    home.display_page_home()