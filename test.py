'''import tkinter 
win = tkinter.Tk()
win.mainloop()
'''

# tkinter library install
from tkinter import*
import time as t

dc=Tk()
dc.title("Digital Clock")
dc.geometry("800x100")

# time and date module 
def time():
    d = t.strftime("%d-%m-%y , %H:%M:%S %p "  )
    l.config(text=d)
    l.after(1000,time)

#print Current Date
print("Todays Time:", t.strftime("%d-%m-%y , %H:%M:%S %p "))

l=Label(dc,font=('Arial',55), bg="black", fg="yellow", text="d")

l.pack(anchor='center')

time()
dc.mainloop()















'''
from datetime import datetime,date,time
c_datetime = datetime.now()
print("current date and time:",c_datetime)

today_date = date.today()
print("today date:",today_date)

c_time=datetime.now().time()
print("c_time:",c_time)

formatted_datetime = c_datetime.strftime("%Y-%M-%D  %H:%M:%S:")
print("foramatted date and time :",formatted_datetime)
'''