import socket
import threading
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from client.로그인 import LoginHandler
from client.코스피코스닥 import PriceRequestHandler

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
            
            #받은 데이터가 'login_request' 일 경우
            if data == "login_request":
                # 로그인.py - Login 클래스의 login() 호출 후 response 저장
                response = self.login_handler.login()
                self.access_token = response
                #연결되어있는 소켓에 보냄
                conn.sendall(str(response).encode())
            elif data == "stock_price_request":
                response = self.stock_code_handler.stock_code_request(self.access_token)
                
                conn.sendall(str(response).encode())
                


            # Process incoming data and send responses
            # Example: self.login.process(data), self.data_request.process(data)
            response = 'Response from server'
            conn.send(response.encode())
        conn.close()

    
        

if __name__ == "__main__":
    server = MainServer('localhost',5000)
    server.start_server()
