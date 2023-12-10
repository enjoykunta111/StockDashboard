import streamlit as st
from requests import post
import json

#st.set_page_config(page_title='로그인 메인')
st.markdown('로그인 메인페이지')

#주식 잔고조회(t0424)
def show_balance():
    
    if 'accesstoken' in st.session_state:
        accesstoken = st.session_state['accesstoken']
    else:
        st.error('로그인이 필요합니다.')
        return

    BASE_URL = "https://openapi.ebestsec.co.kr:8080"
    PATH = 'stock/accno'
    url = f"{BASE_URL}/{PATH}"
    headers = {
        "Content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {accesstoken}",
        "tr_cd":"t0424", 
        "tr_cont":"N",
        "tr_cont_key":"",

    }
    body = {
        "t0424InBlock" : 
        {    
            "prcgb" : "",    
            "chegb" : "",    
            "dangb" : "",    
            "charge" : "",    
            "cts_expcode" : ""  
        }  
    }
    requset = post(url, headers=headers, data=json.dumps(body))
    
    st.write(requset.json())
