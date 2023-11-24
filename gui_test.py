import tkinter as tk
import tkinter.messagebox as msgbox
from PIL import ImageTk
import sqlite3
import 로그인
#import 코스피코스닥

bg_colour = "#3d6466"

def fetch_db():
    connection = sqlite3.connect("data/recipes.db")
    cursor = connection.cursor()
    cursor

def load_frame1():

    frame1.pack_propagate(False)
    # logo widget
    logo_img = ImageTk.PhotoImage(file="D:\\spstock\\dongsan\\offline_lecture\\samplegui\\assets\\RRecipe_logo.png")
    logo_widget = tk.Label(frame1, image= logo_img, bg="#3d6466")
    logo_widget.image = logo_img
    logo_widget.pack()

    tk.Label(frame1,
            text="주가데이터 뽑기",
            bg = bg_colour,
            fg = "white",
            font=("TkMenuFont",14)
            ).pack()

    # button widget (로그인)
    tk.Button(frame1,
            text="Click",
            font=("TkHeadingFont",20),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda:load_frame2()
            ).pack(pady=20)
    
    # button widget (계좌내역 가져오기)
    tk.Button(frame1,
            text="Click",
            font=("TkHeadingFont",20),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda:load_frame2()
            ).pack(pady=20)
    
def load_frame2():
    accessToken = 로그인.메인().로그인()
    msgbox.showinfo(accessToken)

def load_frame3():
    
    msgbox.showinfo('계좌내역가져오기')

def load_frame4():
    
    msgbox.showinfo('일봉데이터 요청')




# initiallize app
root = tk.Tk()
root.title('Stock Dashboard')

#root.eval('tk::PlaceWindow . center')
x = root.winfo_screenwidth() //2
y = int(root.winfo_screenheight()*0.1)
root.geometry('500x600+' + str(x) + '+' + str(y))


# create a frame widget
frame1 = tk.Frame(root, width=500, height=600, bg="#3d6466")
frame2 = tk.Frame(root, bg = bg_colour)
frame1.grid(row=0, column=0)
frame2.grid(row=0, column=0)

for frame in (frame1, frame2):
    frame.grid(row=0, column=0)

load_frame1()

#run app
root.mainloop()