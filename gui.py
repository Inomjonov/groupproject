import tkinter
from tkinter import *
from tkinter import messagebox
import database

def add():
    if len(addtask.get()) == 0:
        messagebox.showerror("Error", "You have entered empty data")
    else:
        database.insertdata(addtask.get())
        addtask.delete(0, END)
        populate()

def populate():
    listbox.delete(0, END)
    for rows in database.show():
        listbox.insert(END, rows[1])

def deletetask():
    selected_task = listbox.get(ANCHOR)
    if selected_task:
        database.deletebytask(selected_task)
        populate()

main = tkinter.Tk()
main.title("Task Manager")
main.geometry("600x800")
main.resizable(True, True)
main.configure(background="#1d1d1d")

tkinter.Label(main, text="Task Manager", background="#1d1d1d", foreground="#eeeeee", font=("Verdana", 20)).pack(pady=10)

addframe = tkinter.Frame(main, bg="#1d1d1d")
addframe.pack()
addtask = tkinter.Entry(addframe, font=("Verdana"), background="#eeeeee")
addtask.pack(ipadx=20, ipady=5, side="left")

addbtn = tkinter.Button(addframe, text="ADD TASK", command=add, background="#000000", foreground="#eeeeee", relief="flat", font=("Arial"), highlightcolor="#000000", activebackground="#1d1d1d", border=0, activeforeground="#eeeeee")
addbtn.pack(padx=20, ipadx=20, ipady=5)

delbtn = tkinter.Button(main, text="DELETE TASK", command=deletetask, background="#ff0000", foreground="#ffffff", relief="flat", font=("Arial"), highlightcolor="#ff0000", activebackground="#cc0000", border=0, activeforeground="#ffffff")
delbtn.pack(pady=10)

tkinter.Label(main, text="Your Tasks", background="#1d1d1d", foreground="#eeeeee", font=("Calibri", 18)).pack(pady=10)

taskframe = tkinter.Frame(main, bg="#1d1d1d")
taskframe.pack(fill=BOTH, expand=300)
scrollbar = Scrollbar(taskframe)
scrollbar.pack(side=RIGHT, fill=Y)
listbox = Listbox(taskframe, font=("Verdana 18 bold"), bg="#1d1d1d", fg="#eeeeee", selectbackground="#eeeeee", selectforeground="#1d1d1d")
listbox.pack(fill=BOTH, expand=300)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

main.mainloop()
