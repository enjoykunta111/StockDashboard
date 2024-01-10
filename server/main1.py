import socket
import threading
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
#from client.로그인 import LoginHandler
#from client.check_account import CheckAccountHandler
#from client.modified_check_account import CheckAccountHandler
#from client.코스피코스닥 import PriceRequestHandler
import asyncio
import pandas as pd
import json


#Server code
class MainServer:
    def __init__(self, host, port, server_info ):
        self.host = host
        self.port = port
        self.server_info = server_info
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))

        self.access_token = None

    def start_server(self):
        self.server_socket.listen()    #client가 접속가능한 갯수 제한?
        print(f"Server listening on (self.host):(self.port)")
        while True:
            conn, address = self.server_socket.accept()
            print(f'Connected by {address}')
            threading.Thread(target=self.client_handler, args=(conn,)).start()

    def determine_target_server(self, data):
        # 서버 C,D,E 선택 로직구현
        # 예: "로그인" -> "C", "잔고조회" -> "D" 등
        if data == '/ebest/login':
            server_id = 5001
            return server_id
        
    async def send_to_server(self, data, server_idx):
        # GUI에서 버튼을 클릭하여 넘어온 키워드(data)를 
        # determine_target_server에서 해당 클라이언트의 포트번호 지정(server_idx)
        # 
        # data = /ebest/login
        # wss://openapi.ebestsec.co.kr:9443
        # ws://localhost:6789
        server_url = 'ws://localhost:' + self.server_info.get(server_idx)
        print(server_url)

    async def client_handler(self, conn):
        #asyncio.set_event_loop(asyncio.new_event_loop()) # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        #self.check_account_handler = CheckAccountHandler(self.callback_check_account, conn)
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print("received_message: ", data) # type : string
            
            # 판단 로직
            server_id = self.determine_target_server(data)
            response = await self.send_to_server(data, server_id)
            # data = /ebest/login
            # server_id = 5001
            # response
            
            response = 'Response from server'
            conn.send(response.encode())
        conn.close()

if __name__ == "__main__":
    server_info = {
        "C":('localhost',5001),
        "D":('localhost',5002),
    }
    server = MainServer('localhost',5000,server_info)
    server.start_server()
