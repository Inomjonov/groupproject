# import tkinter
# from tkinter import *
# from tkinter import messagebox
# import database


# def add():
#     if(len(addtask.get()) == 0):
#         messagebox.showerror(
#             "You have entered empty data")
#     else:
#         database.insertdata(addtask.get())
#         addtask.delete(0, END)
#         populate()


# def populate():
#     listbox.delete(0, END)
#     for rows in database.show():
#         listbox.insert(END, rows[1])


# def deletetask(event):
#     database.deletebytask(listbox.get(ANCHOR))
#     populate()


# main = tkinter.Tk()
# main.title("Task manager")
# main.geometry("600x800")
# main.resizable(True, True)
# main.configure(
#     background="#1d1d1d",
# )

# tkinter.Label(
#     main,
#     text="Task Manager",
#     background="#1d1d1d",
#     foreground="#eeeeee",
#     font=("Verdana 20")
# ).pack(pady=10)

# addframe = tkinter.Frame(
#     main,
#     bg="#1d1d1d",
# )
# addframe.pack()
# addtask = tkinter.Entry(
#     addframe,
#     font=("Verdana"),
#     background="#eeeeee",
# )
# addtask.pack(ipadx=20, ipady=5, side="left")

# addbtn = tkinter.Button(
#     addframe,
#     text="ADD TASK",
#     command=add,
#     background="#000000",
#     foreground="#eeeeee",
#     relief="flat",
#     font=("Helvetica"),
#     highlightcolor="#000000",
#     activebackground="#1d1d1d",
#     border=0,
#     activeforeground="#eeeeee",
# )
# addbtn.pack(padx=20, ipadx=20, ipady=5)

# tkinter.Label(
#     main,
#     text="Your Tasks",
#     background="#1d1d1d",
#     foreground="#eeeeee",
#     font=("Calibri", 18),
# ).pack(pady=10)

# taskframe = tkinter.Frame(
#     main,
#     bg="#1d1d1d",
# )
# taskframe.pack(fill=BOTH, expand=300)
# scrollbar = Scrollbar(taskframe)
# scrollbar.pack(side=RIGHT, fill=Y)
# listbox = Listbox(
#     taskframe,
#     font=("Verdana 18 bold"),
#     bg="#1d1d1d",
#     fg="#eeeeee",
#     selectbackground="#eeeeee",
#     selectforeground="#1d1d1d",
# )
# listbox.pack(fill=BOTH, expand=300)
# listbox.config(yscrollcommand=scrollbar.set)
# scrollbar.config(command=listbox.yview)

# listbox.bind("<Double-Button-1>", deletetask)
# listbox.bind("<Delete>", deletetask)

# populate()

# tkinter.Label(
#     main,
#     text="TIP : Double Click On A Task to Delete",
#     background="#1d1d1d",
#     foreground="#FFEB3B",
#     font=("Calibri 18"),
# ).pack(side=BOTTOM, pady=10)

# main.mainloop()


# import tkinter
# from tkinter import *
# from tkinter import messagebox
# import database
# from tkinter import simpledialog

# def add():
#     task = addtask.get()
#     if not task:
#         messagebox.showerror("Error", "You have entered empty data")
#     else:
#         database.insertdata(task)
#         addtask.delete(0, END)
#         populate()

# def update():
#     selected_task = listbox.get(ANCHOR)
#     if selected_task:
#         new_task = simpledialog.askstring("Update Task", "Enter new task:", initialvalue=selected_task[1])
#         if new_task:
#             database.updatedata(selected_task[0], new_task)
#             populate()

# def populate():
#     listbox.delete(0, END)
#     for rows in database.show():
#         listbox.insert(END, rows[1])

# def deletetask(event):
#     selected_task = listbox.get(ANCHOR)
#     if selected_task:
#         database.deletebytask(selected_task[0])
#         populate()

# main = tkinter.Tk()
# main.title("Task manager")
# main.geometry("600x800")
# main.resizable(True, True)
# main.configure(background="#f0f0f0")  # Lighter background color

# tkinter.Label(main, text="Task Manager", background="#f0f0f0", foreground="#000000", font=("Arial", 24)).pack(pady=10)

# addframe = tkinter.Frame(main, bg="#f0f0f0")
# addframe.pack()
# addtask = tkinter.Entry(addframe, font=("Arial", 16), background="#ffffff")
# addtask.pack(ipadx=20, ipady=5, side="left")

# addbtn = tkinter.Button(addframe, text="ADD TASK", command=add, background="#007bff", foreground="#ffffff", relief="flat", font=("Arial", 12), activebackground="#0056b3", activeforeground="#ffffff")
# addbtn.pack(padx=20, ipadx=20, ipady=5)

# updatebtn = tkinter.Button(main, text="UPDATE SELECTED TASK", command=update, background="#28a745", foreground="#ffffff", relief="flat", font=("Arial", 12), activebackground="#1e7e34", activeforeground="#ffffff")
# updatebtn.pack(pady=10)

# taskframe = tkinter.Frame(main, bg="#f0f0f0")
# taskframe.pack(fill=BOTH, expand=300)
# scrollbar = Scrollbar(taskframe)
# scrollbar.pack(side=RIGHT, fill=Y)
# listbox = Listbox(taskframe, font=("Arial", 16), bg="#ffffff", fg="#000000", selectbackground="#007bff", selectforeground="#ffffff")
# listbox.pack(fill=BOTH, expand=300)
# listbox.config(yscrollcommand=scrollbar.set)
# scrollbar.config(command=listbox.yview)

# listbox.bind("<Double-Button-1>", deletetask)
# listbox.bind("<Delete>", deletetask)

# populate()

# tkinter.Label(main, text="TIP: Double Click On A Task to Delete, Select and Click 'UPDATE SELECTED TASK' to Edit", background="#f0f0f0", foreground="#FFEB3B", font=("Arial", 14)).pack(side=BOTTOM, pady=10)

# main.mainloop()
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
