import tkinter as tk
import tkinter.messagebox as msgbox
from PIL import ImageTk
import socket
import threading

class GuiApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.bg_colour = "#3d6466"

        #self.master = master
        #initialize_ui 메서드는 master 인자를 필요로하기 때문에
        #self.master부터 정의해줘야함
        #self.initialize_ui(self.master)
        self.initialize_ui()
        

        
        self.client_socket = None
        self.server_address = ('localhost', 5000)


    def initialize_ui(self):
        # GUI 요소 초기화 및 배치
        # 예: 프레임, 버튼 등
        # 기본 창 설정
        #self.master = master    #여기서 self.master는 메인윈도우(root)를 참조한다.
        #예를 들어, 버튼을 생성하고 이 메인윈도우에 추가할 수 있음
        #self.button = tk.Button(self.master, text= "Click Me")
        #self.button.pack()

        self.title('Stock Market Application')
        x = self.winfo_screenwidth() //2
        y = int(self.winfo_screenheight()*0.1)
        self.geometry('500x600+' + str(x) + '+' + str(y))

        # 프레임 초기화 및 배치
        self.frame1 = tk.Frame(self, width=500, height=600, bg=self.bg_colour)
        self.frame2 = tk.Frame(self, bg = self.bg_colour)
        for frame in (self.frame1, self.frame2):
            frame.grid(row=0, column=0)

        # 프레임 1에 위젯 추가
        self.load_frame1()
    
    def load_frame1(self):
        self.frame1.pack_propagate(False)

        #logo widget
        logo_img = ImageTk.PhotoImage(file='..\\assets\\RRecipe_logo.png')
        logo_widget = tk.Label(self.frame1, image = logo_img, bg= self.bg_colour)
        logo_widget.image = logo_img
        logo_widget.pack()

        tk.Label(self.frame1,
            text="주가데이터 뽑기",
            bg = self.bg_colour,
            fg = "white",
            font=("TkMenuFont",14)
            ).pack()
        
        # button widget (로그인)
        tk.Button(self.frame1,
                text="로그인",
                font=("TkHeadingFont",20),
                bg="#28393a",
                fg="white",
                cursor="hand2",
                activebackground="#badee2",
                activeforeground="black",
                command=lambda:self.login()
                ).pack(pady=20)
        
        # button widget (종목코드 출력)
        tk.Button(self.frame1,
                text="종목코드출력",
                font=("TkHeadingFont",20),
                bg="#28393a",
                fg="white",
                cursor="hand2",
                activebackground="#badee2",
                activeforeground="black",
                command=lambda:self.stock_price_request()
                ).pack(pady=20)
        
    def login(self):
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

    def stock_price_request(self):
        threading.Thread(target=self.send_stock_price_request).start()

    def send_stock_price_request(self):
        self.client_socket.sendall("stock_price_request".encode())
        response = self.client_socket.recv(1024).decode()
        print("Response from server:", response)

    
    def on_closing(self):
        #창이 닫힐 때 서버 종료
        if self.client_socket:
            self.client_socket.close()
        self.destroy()
        


#메인 윈도우 생성
#root = tk.Tk()

# GUI 인스턴스 생성, 여기서 root가 GUI 클래스의 'master'가 된다.
app = GuiApplication()
app.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()
# 이벤트 루프 시작
#왜 여기서 app.mainloop() 이 아니라 root.mainloop()이지?
#root.mainloop()