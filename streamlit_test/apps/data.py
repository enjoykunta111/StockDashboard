import streamlit as st
from datetime import datetime
from requests import post
import json


class StockDataHandler:
    def __init__(self):
        self.accesstoken = st.session_state.get('accesstoken',None)
    def stock_code_request(self):
        if not self.accesstoken:
            st.error("로그인이 필요합니다.")
            return
        st.write('#코스피 코스닥 처리 페이지')

        url = "https://openapi.ebestsec.co.kr:8080/stock/market-data"
        headers = {
            "Content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self.accesstoken}",
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
    
# Streamlit 페이지 함수
def display_page_datacollect():
    st.title("Data Collect 페이지")
    st.info(st.session_state['accesstoken'])
    #날짜입력
    start_date = st.date_input("시작날짜",key="start_date")
    end_date = st.date_input("종료날짜",key="end_date")

    #날짜데이터 처리
    if st.button("데이터내려받기"):
        st.write(f"시작 날짜: {start_date.strftime('%Y%m%d')}")
        st.write(f"종료 날짜: {end_date.strftime('%Y%m%d')}")
    
    handler = StockDataHandler()
    handler.