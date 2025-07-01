from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

def login():
    if username_entry.get().lower()=='sundar' and password_entry.get()=='1234':
        messagebox.showinfo("Success",'Welcome')
        window.destroy()
        import database
    elif username_entry.get()=='' or password_entry.get()=='':
        messagebox.showerror("Error", "Fields cannot be empty")

    else:
        messagebox.showerror("Error","Please enter the correct credentials")

window = Tk()

window.geometry("1525x775+0+0")
window.title("Student Management System - Login page")
window.resizable(False,False)

bg = ImageTk.PhotoImage(file = 'smsb.jpg')
bg_label = Label(window,image = bg)
bg_label.place(x= 0, y = 0)

login_frame = Frame(window, bg = "white")
login_frame.place(x = 500, y = 250)

logo_image = PhotoImage(file = 'logo.png')
logo_label = Label(login_frame, image = logo_image)
logo_label.grid(row = 0, column = 0, columnspan = 2)


username_image = PhotoImage(file = "profile.png")
username_label = Label(login_frame, image = username_image,text = 'Username', compound=LEFT,
                       font=("times new roman",20,'bold'), bg = "white")
username_label.grid(row = 1,column = 0, pady = 10, padx = 20)
username_entry = Entry(login_frame, font=("times new roman",20,'bold'),bd = 5)
username_entry.grid(row = 1, column = 1, pady = 10, padx = 20)


password_image = PhotoImage(file = "profile.png")
password_label = Label(login_frame, image = password_image,text = 'Password', compound=LEFT,
                       font=("times new roman",20,'bold'), bg = "white")
password_label.grid(row = 2,column = 0, pady = 10, padx = 20)
password_entry = Entry(login_frame, font=("times new roman",20,'bold'),bd = 5)
password_entry.grid(row = 2, column = 1, pady = 10, padx = 20)


login_button = Button(login_frame, text="Login", font=("times new roman",15,'bold'), width = 12,
                  fg = 'white', bg = "green", activebackground="green",activeforeground="white",
                      cursor="hand2", command= login)
login_button.grid(row = 3, column = 1, pady = 10)


window.mainloop()



