import tkinter as tk

class GuiApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.bg_colour = "#c3c3c3"

        self.initialize_ui()

    def initialize_ui(self):
        self.title('Stock Market Application')
        self.geometry('500x400')
        self.load_frame1()

    def indicate(self):
        

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
                command=lambda:self.login()
                )
        login_button.place(x=10,y=50)

        login_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
        login_indicate.place(x=3,y=50,width=5,height=40)
        ##################################################

        data_collect_button = tk.Button(options_frame,
                text="데이터수집",
                font=("Bold",13),
                bg="#c3c3c3",   
                fg="#158aff",
                bd=0,
                #cursor="hand2",
                activebackground="#badee2",
                activeforeground="black",
                command=lambda:self.login()
                )
        data_collect_button.place(x=10,y=100)

        data_collect_indicate = tk.Label(options_frame, text='', bg='#c3c3c3')
        data_collect_indicate.place(x=3,y=100,width=5,height=40)
           


        main_frame = tk.Frame(self, highlightbackground='black'
                              ,highlightthickness=2)
        main_frame.pack(side=tk.LEFT)
        main_frame.pack_propagate(False)
        main_frame.configure(height=400, width=500)
        

    def on_closing(self):
        #창이 닫힐 때 서버 종료
        if self.client_socket:
            self.client_socket.close()
        self.destroy()


app = GuiApplication()
#app.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()