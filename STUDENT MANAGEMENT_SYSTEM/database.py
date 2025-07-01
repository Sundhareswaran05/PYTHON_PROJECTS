from tkinter import *
import time
import ttkthemes
from tkinter import ttk, messagebox,filedialog
import pymysql
import pandas as pd

# functions
def exit():
    result = messagebox.askyesno('Confirm','Do you want to exit')
    if result:
        root.destroy()
    else:
        pass


def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = student_table.get_children()
    newlist = []
    for index in indexing:
        content = student_table.item(index)
        datalist = content['values']
        newlist.append(datalist)

    table = pd.DataFrame(newlist,columns=['Id','Name','Mobile','Email','Address','Gender','DOB','Added Date','Added Time'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data exported Successfully')
def field_data(title,button_text,command):
    global id_entry,name_entry,email_entry,phone_entry,address_entry,gender_entry,dob_entry,dataentry
    dataentry = Toplevel()
    dataentry.title(title)
    dataentry.resizable(0, 0)
    dataentry.grab_set()

    id_label = Label(dataentry, text='ID', font=('times new roman', 20, 'bold'))
    id_label.grid(row=0, column=0, padx=25, pady=15, sticky=W)
    id_entry = Entry(dataentry, font=('roman', 15, 'bold'))
    id_entry.grid(row=0, column=1, padx=10, pady=15)

    name_label = Label(dataentry, text='NAME', font=('times new roman', 20, 'bold'))
    name_label.grid(row=1, column=0, padx=25, pady=15, sticky=W)
    name_entry = Entry(dataentry, font=('roman', 15, 'bold'))
    name_entry.grid(row=1, column=1, padx=10, pady=15)

    phone_label = Label(dataentry, text='PHONE NO.', font=('times new roman', 20, 'bold'))
    phone_label.grid(row=2, column=0, padx=25, pady=15, sticky=W)
    phone_entry = Entry(dataentry, font=('roman', 15, 'bold'))
    phone_entry.grid(row=2, column=1, padx=10, pady=15)

    email_label = Label(dataentry, text='EMAIL', font=('times new roman', 20, 'bold'))
    email_label.grid(row=3, column=0, padx=25, pady=15, sticky=W)
    email_entry = Entry(dataentry, font=('roman', 15, 'bold'))
    email_entry.grid(row=3, column=1, padx=10, pady=15)

    address_label = Label(dataentry, text='ADDRESS', font=('times new roman', 20, 'bold'))
    address_label.grid(row=4, column=0, padx=25, pady=15, sticky=W)
    address_entry = Entry(dataentry, font=('roman', 15, 'bold'))
    address_entry.grid(row=4, column=1, padx=10, pady=15)

    gender_label = Label(dataentry, text='GENDER', font=('times new roman', 20, 'bold'))
    gender_label.grid(row=5, column=0, padx=25, pady=15, sticky=W)
    gender_entry = Entry(dataentry, font=('roman', 15, 'bold'))
    gender_entry.grid(row=5, column=1, padx=10, pady=15)

    dob_label = Label(dataentry, text='D.O.B', font=('times new roman', 20, 'bold'))
    dob_label.grid(row=6, column=0, padx=25, pady=15, sticky=W)
    dob_entry = Entry(dataentry, font=('roman', 15, 'bold'))
    dob_entry.grid(row=6, column=1, padx=10, pady=15)

    student_button = ttk.Button(dataentry, text=button_text, command=command)
    student_button.grid(row=7, columnspan=2, pady=10)

    if title=='Update Student':

        indexing = student_table.focus()
        print(indexing)
        content = student_table.item(indexing)
        listdata = content['values']

        id_entry.insert(0, listdata[0])
        name_entry.insert(0, listdata[1])
        phone_entry.insert(0, listdata[2])
        email_entry.insert(0, listdata[3])
        address_entry.insert(0, listdata[4])
        gender_entry.insert(0, listdata[5])
        dob_entry.insert(0, listdata[6])


def update_data():
    query='update student set name=%s, email=%s, mobile=%s, address=%s, gender=%s, dob=%s, date=%s, time=%s where id=%s'
    mycursor.execute(query,(name_entry.get(),email_entry.get(),phone_entry.get(),address_entry.get(),
                            gender_entry.get(),dob_entry.get(),date,currenttime,id_entry.get()))
    con.commit()
    messagebox.showinfo('Updation..!',f'Id {id_entry.get()} is successfully updated',parent=dataentry)
    dataentry.destroy()
    show_student()



def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    student_table.delete(*student_table.get_children())
    for data in fetched_data:
        student_table.insert('', END, values=data)


def delete_student():
    indexing=student_table.focus()
    print(indexing)
    content=student_table.item(indexing)
    content_id=content['values'][0]
    query = 'delete from student where id=%s'
    mycursor.execute(query,content_id)
    con.commit()
    messagebox.showinfo('Deleted',f'Id {content_id} is deleted successfully')
    query='select * from student'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    student_table.delete(*student_table.get_children())
    for data in fetched_data:
        student_table.insert('',END,values=data)


def search_data():
    query='select * from student where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s'
    mycursor.execute(query,(id_entry.get(),name_entry.get(),email_entry.get(),phone_entry.get(),address_entry.get(),gender_entry.get(),dob_entry.get()))
    student_table.delete(*student_table.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        student_table.insert('',END,values=data)



def add_data():
    if id_entry.get()=='' or name_entry.get()=='' or phone_entry.get()=='' or email_entry=='' or address_entry.get()=='' or gender_entry.get()=='' or dob_entry.get()=='':
        messagebox.showerror('Error','All fields are required', parent=dataentry)

    else:
        try:
            query='insert into student value(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(id_entry.get(),name_entry.get(),phone_entry.get(),email_entry.get(),address_entry.get(),
                                    gender_entry.get(),dob_entry.get(),date,currenttime))
            con.commit()
            result=messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clear the form?',parent = dataentry)

            if result:
                id_entry.delete(0,END)
                name_entry.delete(0, END)
                phone_entry.delete(0, END)
                email_entry.delete(0, END)
                address_entry.delete(0, END)
                gender_entry.delete(0, END)
                dob_entry.delete(0, END)
            else:
                pass
        except:
            messagebox.showerror('Error','Id should be unique..!',parent=dataentry)
            return

        query = 'select * from student'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        student_table.delete(*student_table.get_children())
        for data in fetched_data:
            student_table.insert('',END,values=data)






def connect_database():
    def connect():
        global mycursor,con
        try:
            con = pymysql.connect(host='', user='', password='')
            mycursor = con.cursor()

        except:
            messagebox.showerror('Error','Invalid Details',parent=connectWindow)
            return

        try:
            query = 'create database studentmanagementsystem'
            mycursor.execute(query)
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
            query =  'create table student(id int not null primary key, name varchar(30), mobile varchar(10),email varchar(30), address varchar(100), gender varchar(10), dob varchar(10), date varchar(20), time varchar(20))'
            mycursor.execute(query)

        except:
            query='use studentmanagementsystem'
            mycursor.execute(query)
        messagebox.showinfo('Success', 'Database Connection is Successful', parent=connectWindow)

        connectWindow.destroy()
        add_student_button.config(state=NORMAL)
        search_student_button.config(state=NORMAL)
        delete_student_button.config(state=NORMAL)
        update_student_button.config(state=NORMAL)
        show_student_button.config(state=NORMAL)
        export_student_button.config(state=NORMAL)


    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0, 0)

    hostnamelabel = Label(connectWindow, text='Host Name', font=('arial', 20, 'bold'))
    hostnamelabel.grid(row=0, column=0, padx=20)


    hostentry = Entry(connectWindow, font=('roman', 15,'bold'), bd=2)
    hostentry.grid(row=0, column=1, padx=40, pady=20)

    usernamelabel = Label(connectWindow, text='User Name', font=('arial',20, 'bold'))
    usernamelabel.grid(row=1, column=0, padx=20)

    userentry = Entry(connectWindow,font=('roman', 15,'bold'), bd=2)
    userentry.grid(row=1, column=1, padx=40, pady=20)

    passwordnamelabel = Label(connectWindow, text='Password', font=('arial',20,'bold'))
    passwordnamelabel.grid(row=2, column=0, padx=20)

    passwordentry = Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    passwordentry.grid(row=2, column=1, padx=40, pady=20)

    connect_buttton = ttk.Button(connectWindow, text="CONNECT", command=connect)
    connect_buttton.grid(row=3, columnspan=2)



count=0
text = ''
def slider():
    global text,count
    if count==len(s):
        count=0
        text=''
    text = text+s[count]
    sliderlabel.config(text=text)
    count+=1
    sliderlabel.after(500, slider)

def clock():
    global date,currenttime
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime("%H:%M:%S")
    datetimeLabel.config(text = f"Date: {date}\nTime: {currenttime} ")
    datetimeLabel.after(1000, clock)

root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')


root.geometry("1525x775+0+0")
root.title("Student Management System - DataBase")
root.resizable(False,False)


datetimeLabel = Label(root, text="dddd", font=('times new roman', 18, 'bold'))
datetimeLabel.place(x = 5, y = 5)
clock()

s = "Student Management System"
sliderlabel = Label(root, text = s, font=('arial', 30, 'italic bold'))
sliderlabel.place(x=500,y=0)
slider()

connect_buttton = ttk.Button(root, text='Connect database', command=connect_database)
connect_buttton.place(x=1350, y=0)

left_frame = Frame(root)
left_frame.place(x=50, y=80, width = 282, height = 650)

logo_image = PhotoImage(file='students.png')
logo_label = Label(left_frame, image=logo_image)
logo_label.grid(row = 0, column = 1, pady = 20)

add_student_button = ttk.Button(left_frame,text='Add Student',width=25,state=DISABLED, command=lambda :field_data('Add Student','ADD',add_data))
add_student_button.grid(row=1, column=1, pady=20)

search_student_button = ttk.Button(left_frame,text='Search Student', width=25, state=DISABLED, command=lambda :field_data('Search Student','Search',search_data))
search_student_button.grid(row=2, column=1, pady=20)

delete_student_button = ttk.Button(left_frame,text='Delete Student', width=25,state=DISABLED,command=delete_student)
delete_student_button.grid(row=3, column=1,pady=20)

update_student_button = ttk.Button(left_frame,text='Update Student', width=25,state=DISABLED,command=lambda :field_data('Update Student','Update',update_data))
update_student_button.grid(row=4, column=1, pady=20)

show_student_button = ttk.Button(left_frame,text='Show Student', width=25,state=DISABLED,command=show_student)
show_student_button.grid(row=5, column=1, pady=20)

export_student_button = ttk.Button(left_frame,text='Export Student', width=25, state=DISABLED,command=export_data)
export_student_button.grid(row=6, column=1, pady=20)

exit_student_button = ttk.Button(left_frame,text='Exit Student', width=25,command=exit)
exit_student_button.grid(row=7, column=1, pady=20)


right_frame = Frame(root)
right_frame.place(x=337,y=80,width = 1180, height = 650)

scroll_bar_x = Scrollbar(right_frame, orient=HORIZONTAL)
scroll_bar_y = Scrollbar(right_frame, orient=VERTICAL)
scroll_bar_x.pack(side=BOTTOM, fill=X)
scroll_bar_y.pack(side=RIGHT, fill=Y)

student_table = ttk.Treeview(right_frame,columns=('Id','Name','Mobile No','Email','Address','Gender',
                                 'D.O.B','Added Date','Added Time'),xscrollcommand=scroll_bar_x.set,
                                 yscrollcommand=scroll_bar_y.set)

scroll_bar_x.config(command=student_table.xview)
scroll_bar_y.config(command=student_table.yview)

student_table.pack(fill = BOTH, expand=1)

student_table.heading('Id', text='Id')
student_table.heading('Name', text='Name')
student_table.heading('Mobile No', text='Mobile No')
student_table.heading('Email', text='Email')
student_table.heading('Address', text='Address')
student_table.heading('Gender', text='Gender')
student_table.heading('D.O.B', text='D.O.B')
student_table.heading('Added Date', text='Added Date')
student_table.heading('Added Time', text='Added Time')

student_table.column('Id',width=50,anchor=CENTER)
student_table.column('Name',width=250,anchor=CENTER)
student_table.column('Mobile No',width=150,anchor=CENTER)
student_table.column('Email',width=250,anchor=CENTER)
student_table.column('Address',width=300,anchor=CENTER)
student_table.column('Gender',width=120,anchor=CENTER)
student_table.column('D.O.B',width=170,anchor=CENTER)
student_table.column('Added Date',width=150,anchor=CENTER)
student_table.column('Added Time',width=150,anchor=CENTER)

style = ttk.Style()

style.configure('Treeview',rowheight=30,font=('arial',15),foreground='red',background='white',fieldbackground='white')
style.configure('Treeview.Heading',font=('arial',15,'bold'))




student_table.config(show='headings')




root.mainloop()