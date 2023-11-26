import tkinter as tk
import tkinter.messagebox as msgbox
from PIL import ImageTk
import sqlite3
import 로그인
import 코스피코스닥



class GuiApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.bg_colour = "#3d6466"
        self.accessToken = None
        self.initialize_ui()

    def initialize_ui(self):
        # GUI 요소 초기화 및 배치
        # 예: 프레임, 버튼 등
        # 기본 창 설정
        self.title('Stock Dashboard')
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
        # logo widget
        logo_img = ImageTk.PhotoImage(file=".\\assets\\RRecipe_logo.png")
        logo_widget = tk.Label(self.frame1, image= logo_img, bg=self.bg_colour)
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
                command=lambda:self.load_frame2()
                ).pack(pady=20)
    
        # button widget (계좌내역 가져오기)
        tk.Button(self.frame1,
                text="계좌내역가져오기",
                font=("TkHeadingFont",20),
                bg="#28393a",
                fg="white",
                cursor="hand2",
                activebackground="#badee2",
                activeforeground="black",
                command=lambda:self.load_frame3()
                ).pack(padx=50,pady=10)
    
        # button widget (일봉데이터 요청)
        tk.Button(self.frame1,
                text="전종목일봉데이터 가져오기",
                font=("TkHeadingFont",20),
                bg="#28393a",
                fg="white",
                cursor="hand2",
                activebackground="#badee2",
                activeforeground="black",
                command=lambda:self.load_frame4()
                ).pack(pady=20)

    def load_frame2(self):
        self.accessToken = 로그인.메인().로그인()
        msgbox.showinfo("확인",self.accessToken)

    def load_frame3(self):
        
        msgbox.showinfo('확인','계좌내역가져오기')

    def load_frame4(self):
        testStockCode = 코스피코스닥.TR요청들().코스피코스닥(self.accessToken)
        print(testStockCode)
        msgbox.showinfo('확인','코스피 코스닥 종목코드 가져오기')

# 애플리케이션 실행
app = GuiApplication()
app.mainloop()