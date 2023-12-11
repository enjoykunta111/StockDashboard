import socket
import threading
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from client.로그인 import LoginHandler
from client.코스피코스닥 import PriceRequestHandler
import asyncio
import pandas as pd

#Server code
class MainServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket()
        self.server_socket.bind((self.host, self.port))
        self.login_handler = LoginHandler()
        self.stock_code_handler = PriceRequestHandler()

        self.access_token = None

    def start_server(self):
        self.server_socket.listen()    #client가 접속가능한 갯수 제한?
        print(f"Server listening on (self.host):(self.port)")
        while True:
            conn, address = self.server_socket.accept()
            print(f'Connected by {address}')
            threading.Thread(target=self.client_handler, args=(conn,)).start()

    def client_handler(self, conn):
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            # Split the received message by spaces
            received_message = data.split(' ')
            # Check the command part of the message
            command = received_message[0]

            #받은 데이터가 'login_request' 일 경우
            if command == "login_request":
                # 로그인.py - Login 클래스의 login() 호출 후 response 저장
                response = self.login_handler.login()
                self.access_token = response
                #연결되어있는 소켓에 보냄
                conn.sendall(str(response).encode())

            elif command == "stock_price_request":
                
                response = self.stock_code_handler.stock_code_request(self.access_token)
                
                conn.sendall(str(response).encode())
                
            elif command == "fetch_daily_prices":
                #csv에서 종목들 불러오기
                stock_code_df = pd.read_csv('../data/stock_code.csv', encoding='cp949')

                # Extract start and end dates from the message
                shcode = received_message[1] 
                sdate = received_message[2]
                edate = received_message[3]


                # Find the matching gubun value for the given shcode
                gubun = int(stock_code_df.loc[stock_code_df['shcode'] == shcode, 'gubun'].iloc[0])
                

                #response = self.stock_code_handler.stock_price_request(self.access_token,sdate,edate)
                asyncio.run(self.stock_code_handler.stock_price_request(self.access_token,gubun,shcode, sdate, edate))

            # Process incoming data and send responses
            # Example: self.login.process(data), self.data_request.process(data)
            response = 'Response from server'
            conn.send(response.encode())
        conn.close()

    
        

if __name__ == "__main__":
    server = MainServer('localhost',5000)
    server.start_server()
