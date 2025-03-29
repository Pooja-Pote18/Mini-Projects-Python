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

#label
l=Label(dc,font=('Arial',55), bg="black", fg="yellow", text="d")

l.pack(anchor='center')

time()
dc.mainloop()

