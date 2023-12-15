import tkinter as tk
from tkinter import ttk
import requests

def create_task():
    task = {
        "name": task_name_entry.get(),
        "urgency": urgency_var.get(),
        "assigned_to": int(assignee_entry.get())
    }
    response = requests.post("http://localhost:8000/tasks/", json=task)
    # handle response

root = tk.Tk()
root.title("Task Management App")

task_name_entry = ttk.Entry(root)
task_name_entry.pack()

urgency_var = tk.StringVar()
urgent_rb = ttk.Radiobutton(root, text='Urgent', variable=urgency_var, value='Urgent')
medium_rb = ttk.Radiobutton(root, text='Medium', variable=urgency_var, value='Medium')
low_rb = ttk.Radiobutton(root, text='Low', variable=urgency_var, value='Low')
urgent_rb.pack()
medium_rb.pack()
low_rb.pack()

assignee_entry = ttk.Entry(root)
assignee_entry.pack()

create_task_button = ttk.Button(root, text="Create Task", command=create_task)
create_task_button.pack()

root.mainloop()
