import tkinter as tk
import socket
import threading
import time

class GuiApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.bg_colour = "#c3c3c3"

        self.initialize_ui()
        self.client_socket = None
        self.server_address = ('localhost', 5000)

    def initialize_ui(self):
        self.title('Stock Market Application')
        self.geometry('500x400')
        self.load_frame1()

    def hide_indicator(self):
        self.login_indicate.config(bg='#c3c3c3')
        self.data_collect_indicate.config(bg='#c3c3c3')
    def delete_pages(self):
        for frame in self.main_frame.winfo_children():
            frame.destroy()

    def indicator(self,lb,page):
        self.hide_indicator()
        lb.config(bg='#158aff')
        self.delete_pages()
        page()

    def load_frame1(self):
        
        # self.frame1.pack_propagate(False)
        # self.frame1.configure(width=100, height=400)
        options_frame = tk.Frame(self, bg=self.bg_colour)
        options_frame.pack(side=tk.LEFT)
        options_frame.pack_propagate(False)
        options_frame.configure(width=100,height=400) 

        ##############################################
        login_button = tk.Button(options_frame,
                text="로그인",
                font=("Bold",13),
                bg="#c3c3c3",   
                fg="#158aff",
                bd=0,
                #cursor="hand2",
                activebackground="#badee2",
                activeforeground="black",
                command=lambda:[self.indicator(self.login_indicate,self.login_page)]
                )
        login_button.place(x=10,y=50)

        self.login_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
        self.login_indicate.place(x=3,y=50,width=5,height=40)
        ##################################################

        self.data_collect_button = tk.Button(options_frame,
                text="데이터수집",
                font=("Bold",13),
                bg="#c3c3c3",   
                fg="#158aff",
                bd=0,
                #cursor="hand2",
                activebackground="#badee2",
                activeforeground="black",
                command=lambda:[self.indicator(self.data_collect_indicate,self.data_collect_page)]
                )
        self.data_collect_button.place(x=10,y=100)

        self.data_collect_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
        self.data_collect_indicate.place(x=3,y=100,width=5,height=40)
           


        self.main_frame = tk.Frame(self, highlightbackground='black'
                              ,highlightthickness=2)
        self.main_frame.pack(side=tk.LEFT)
        self.main_frame.pack_propagate(False)
        self.main_frame.configure(height=400, width=500)
        
    def login_page(self):
        self.login_frame = tk.Frame(self.main_frame)
        self.lb = tk.Label(self.login_frame, text='Login Page\n\nPage: 1', font=('Bold',30))
        self.lb.pack()
        self.login_frame.pack(pady=20)

        if self.client_socket is None:
            # 소켓 생성 후 서버 연결
            self.client_socket = socket.socket()
            try:
                self.client_socket.connect(self.server_address)
            except Exception as e:
                print('Error connecting to server:',e)
                return

        #로그인 요청을 별도의 스레드에서 처리
        threading.Thread(target=self.send_login_request).start()

    def send_login_request(self):
        # 로그인 요청 메시지 전송
        try:
            # 로그인 요청 메시지 전송
            self.client_socket.sendall("login_request".encode())
            # 서버로부터 응답받기
            response = self.client_socket.recv(1024).decode()
            print("Response from server:", response)

            # 연결 종료
            #self.client_socket.close()

        except Exception as e:
            print("Error connecting to server:",e)


    def data_collect_page(self):
        self.data_collect_frame = tk.Frame(self.main_frame)
        self.lb = tk.Label(self.data_collect_frame, text='Data Collect Page\n\nPage: 1', font=('Bold',30))
        self.lb.pack()
        self.data_collect_frame.pack(pady=20)
        # Create Date Entry Widgets
        tk.Label(self.data_collect_frame, text="종목코드:").pack()
        self.stockcode_entry = tk.Entry(self.data_collect_frame)
        self.stockcode_entry.pack(pady=5)

        tk.Label(self.data_collect_frame, text="시작날짜:").pack()
        self.start_date_entry = tk.Entry(self.data_collect_frame)
        self.start_date_entry.pack(pady=5)

        tk.Label(self.data_collect_frame, text="종료날짜:").pack()
        self.end_date_entry = tk.Entry(self.data_collect_frame)
        self.end_date_entry.pack(pady=5)

        send_button = tk.Button(self.data_collect_frame, text="전송"
                                ,command=lambda:[self.stock_price_request()] )
        send_button.pack()

    def stock_price_request(self):
        stock_code = self.stockcode_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        #print(stock_code,start_date,end_date)
        threading.Thread(target=self.send_stock_price_request(stock_code,start_date,end_date)).start()

    def send_stock_price_request(self,stock_code,sdate,edate):
        # First, request stock code export
        self.client_socket.sendall("stock_price_request".encode())

        # Then, request fetching daily prices
        # You might want to add a delay or a confirmation step here
        time.sleep(1)
        self.client_socket.sendall(f"fetch_daily_prices {stock_code} {sdate} {edate}".encode())


        response = self.client_socket.recv(1024).decode()
        print("Response from server:", response)

    def on_closing(self):
        #창이 닫힐 때 서버 종료
        if self.client_socket:
            self.client_socket.close()
        self.destroy()


app = GuiApplication()
#app.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()