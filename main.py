import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
import bcrypt
import tkcalendar
from tkinter import PhotoImage

def setup_database():
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        urgency TEXT,
        due_date TEXT,
        assigned_to INTEGER,
        status TEXT DEFAULT 'Not Started',
        created_by INTEGER,
        FOREIGN KEY (assigned_to) REFERENCES users(id),
        FOREIGN KEY (created_by) REFERENCES users(id)
    )
    ''')

    conn.commit()
    conn.close()

setup_database()



# User Authentication Functions
# ... (user authentication functions) ...

# User Authentication Functions
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def register_user(username, password, role):
    hashed_password = hash_password(password)
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                       (username, hashed_password, role))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def login_user(username, password):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password(password, user[1]):
        return user[0]  # Return user ID
    return None

def get_user_role(user_id):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute('SELECT role, username FROM users WHERE id = ?', (user_id,))
    role, username = cursor.fetchone()
    conn.close()
    return role, username

def get_manager_tasks(manager_id):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title FROM tasks WHERE created_by = ?', (manager_id,))
    tasks = [{'id': row[0], 'title': row[1]} for row in cursor.fetchall()]
    conn.close()
    return tasks

def get_developer_tasks(developer_id):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title FROM tasks WHERE assigned_to = ?', (developer_id,))
    tasks = [{'id': row[0], 'title': row[1]} for row in cursor.fetchall()]
    conn.close()
    return tasks

# Task Manager App Class
# ... (TaskManagerApp class) ...

class TaskManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager")
        self.geometry("600x400")
        self.configure(bg='lightblue')

        self.current_user_id = None
        self.current_username = None
        self.current_role = None

        self.initialize_gui()

    def initialize_gui(self):
        self.login_frame = tk.Frame(self, bg='lightblue')
        self.registration_frame = tk.Frame(self, bg='lightblue')

        self.init_login_frame()
        self.init_registration_frame()

        self.show_frame(self.login_frame)

    def init_login_frame(self):
        tk.Label(self.login_frame, text="Username", font=("Arial", 12), bg='lightblue').pack()
        self.login_username = tk.Entry(self.login_frame)
        self.login_username.pack()

        tk.Label(self.login_frame, text="Password", font=("Arial", 12), bg='lightblue').pack()
        self.login_password = tk.Entry(self.login_frame, show="*")
        self.login_password.pack()

        tk.Button(self.login_frame, text="Login", command=self.login, bg='lightgreen').pack(pady=10)
        tk.Button(self.login_frame, text="Register", command=lambda: self.show_frame(self.registration_frame), bg='lightcoral').pack()

    def init_registration_frame(self):
        label_font = ("Arial", 14, "bold")  # Change font style as needed
        background_color = "lightblue"  # Change background color as needed
        tk.Label(self.registration_frame, text="Username", font=label_font, bg=background_color).pack()
        self.reg_username = tk.Entry(self.registration_frame)
        self.reg_username.pack()

        tk.Label(self.registration_frame, text="Password", font=label_font, bg=background_color).pack()
        self.reg_password = tk.Entry(self.registration_frame, show="*")
        self.reg_password.pack()

        tk.Label(self.registration_frame, text="Role (manager/developer)", font=label_font, bg=background_color).pack()
        self.reg_role = tk.Entry(self.registration_frame)
        self.reg_role.pack()

        tk.Button(self.registration_frame, text="Register", command=self.register, bg='lightgreen').pack(pady=10)
        tk.Button(self.registration_frame, text="Back to Login", command=lambda: self.show_frame(self.login_frame), bg='lightcoral').pack()

    def show_frame(self, frame):
        frame.pack(fill="both", expand=True)

    def hide_frame(self, frame):
        frame.pack_forget()

    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()

        user_id = login_user(username, password)
        if user_id:
            self.current_user_id = user_id
            role, user_name = get_user_role(user_id)
            self.current_role = role
            self.current_username = user_name

            if role == 'manager':
                ManagerWindow(self, user_id, user_name)
            elif role == 'developer':
                DeveloperWindow(self, user_id, user_name)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

    def register(self):
        username = self.reg_username.get()
        password = self.reg_password.get()
        role = self.reg_role.get().lower()

        if role not in ['manager', 'developer']:
            messagebox.showerror("Registration Failed", "Role must be either 'manager' or 'developer'")
            return

        if register_user(username, password, role):
            messagebox.showinfo("Registration Success", "You have successfully registered!")
            self.show_frame(self.login_frame)
        else:
            messagebox.showerror("Registration Failed", "Username already exists")
class ManagerWindow(tk.Toplevel):
    # def __init__(self, master, user_id, username):
    #     super().__init__(master)
    #     self.title("Manager Dashboard")
    #     self.geometry("600x400")
    #     self.configure(bg='lightblue')
    #     label_font = ("Arial", 14, "bold")  # Change font style as needed
    #     background_color = "lightblue"  # Change background color as needed

    #     tk.Label(self, text=f"Hello, {username}", font=label_font, bg=background_color).pack()

    #     tk.Button(self, text="Create Task", command=lambda: CreateTaskWindow(self, user_id), bg="lightcoral").pack()

    #     self.account_frame = self.init_account_frame(username)
    #     tk.Button(self, text="Account", command=lambda: self.toggle_frame(self.account_frame), bg="lightcoral").pack()
    def __init__(self, master, user_id, username):
        super().__init__(master)
        self.title("Manager Dashboard")
        self.geometry("1200x400")
        self.configure(bg='lightblue')
        self.user_id = user_id
        label_font = ("Arial", 14, "bold")  # Change font style as needed
        background_color = "lightblue"  # Change background color as needed


        tk.Label(self, text=f"Hello, {username}", font=label_font, bg=background_color).pack()

        # Set up the Treeview widget
        self.tasks_tree = ttk.Treeview(self, columns=('ID', 'Title', 'Urgency', 'Due Date', 'Assigned To', 'Status'), show='headings')
        self.tasks_tree.heading('ID', text='ID')
        self.tasks_tree.heading('Title', text='Title')
        self.tasks_tree.heading('Urgency', text='Urgency')
        self.tasks_tree.heading('Due Date', text='Due Date')
        self.tasks_tree.heading('Assigned To', text='Assigned To')
        self.tasks_tree.heading('Status', text='Status')
        self.tasks_tree.pack(expand=True, fill='both')

        # Load the tasks assigned by this manager
        self.load_tasks()

        # Button to create a new task
        tk.Button(self, text="Create Task", command=lambda: CreateTaskWindow(self, user_id), bg='lightgreen').pack()

        # Account frame (you will need to implement this if not already done)
        self.account_frame = self.init_account_frame(username)
        tk.Button(self, text="Account", command=lambda: self.toggle_frame(self.account_frame), bg='lightcoral').pack()

    def load_tasks(self):
        tasks = self.get_manager_tasks(self.user_id)
        for task in tasks:
            # Fetch the username of the user this task is assigned to
            assigned_to_username = self.get_username_by_id(task['assigned_to']) if task['assigned_to'] else "Unassigned"
            self.tasks_tree.insert('', 'end', values=(task['id'], task['title'], task['urgency'], task['due_date'], assigned_to_username, task['status']))

    def get_manager_tasks(self, manager_id):
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, urgency, due_date, assigned_to, status FROM tasks 
            WHERE created_by = ?
        ''', (manager_id,))
        tasks = [{'id': row[0], 'title': row[1], 'urgency': row[2], 'due_date': row[3], 'assigned_to': row[4], 'status': row[5]} for row in cursor.fetchall()]
        conn.close()
        return tasks

    def get_username_by_id(self, user_id):
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
        username = cursor.fetchone()
        conn.close()
        return username[0] if username else "Unassigned"

    # Add additional methods as needed for the ManagerWindow

    def init_account_frame(self, username,):
        frame = tk.Frame(self, bg="white", width=200,height=400)

        tk.Label(frame, text=f"Username: {username}", font=("Arial", 14, 'bold'), bg="white").pack(pady=10)
        tk.Button(frame, text="Logout", command=self.logout, bg="lightcoral").pack(pady=10)

        return frame

    def toggle_frame(self, frame):
        if frame.winfo_ismapped():
            frame.pack_forget()
        else:
            frame.pack(side="bottom", fill="y")

    def logout(self):
        self.destroy()


    def create_task(self):
        CreateTaskWindow(self, self.master.current_user_id)

import tkinter as tk
from tkinter import ttk, messagebox
import tkcalendar
import sqlite3

class CreateTaskWindow(tk.Toplevel):
    def __init__(self, master, creator_id):
        super().__init__(master)
        self.title("Create New Task")
        self.geometry("600x400")
        self.creator_id = creator_id

        # Set background color for the entire window
        self.configure(bg='lightblue')

        # Task Name
        tk.Label(self, text="Task Name", font=("Arial", 12, "bold"), bg='lightblue').grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.task_name_entry = tk.Entry(self)
        self.task_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Urgency Level
        tk.Label(self, text="Urgency Level", font=("Arial", 12, "bold"), bg='lightblue').grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.urgency_level = tk.StringVar(self)
        self.urgency_level.set("Low")  # default value
        tk.OptionMenu(self, self.urgency_level, "Low", "Medium", "High").grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Due Date
        tk.Label(self, text="Due Date", font=("Arial", 12, "bold"), bg='lightblue').grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.due_date_entry = tkcalendar.DateEntry(self)
        self.due_date_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Assign to (Username) - Dropdown menu for developers
        tk.Label(self, text="Assign to (Developer)", font=("Arial", 12, "bold"), bg='lightblue').grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.assign_to_var = tk.StringVar(self)
        developers = self.get_developers()
        self.assign_to_menu = ttk.Combobox(self, textvariable=self.assign_to_var, values=developers, state="readonly")
        self.assign_to_menu.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Create Task Button
        tk.Button(self, text="Create Task", command=self.add_task_to_db, bg='lightgreen').grid(row=4, column=0, columnspan=2, pady=10)

    def get_developers(self):
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE role = ?', ('developer',))
        developers = [row[0] for row in cursor.fetchall()]
        conn.close()
        return developers

    def get_user_role_by_id(self, user_id):
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT role FROM users WHERE id = ?', (user_id,))
        role = cursor.fetchone()
        conn.close()
        return role[0] if role else None
    
    def add_task_to_db(self):
        task_name = self.task_name_entry.get()
        urgency = self.urgency_level.get()
        due_date = self.due_date_entry.get()
        assign_to_username = self.assign_to_var.get()

        if not assign_to_username:
            messagebox.showerror("Error", "Please select a developer to assign the task.")
            return

        assign_to_id = self.get_user_id_by_username(assign_to_username)
        if assign_to_id is None:
            messagebox.showerror("Error", "Developer username not found.")
            return

        # Check if the assignee is not a manager
        assignee_role = self.get_user_role_by_id(assign_to_id)
        if assignee_role == 'manager':
            messagebox.showerror("Error", "Managers cannot be assigned tasks.")
            return

        # Add task to the database
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, description, urgency, due_date, assigned_to, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (task_name, f"Urgency: {urgency}, Due: {due_date}", urgency, due_date, assign_to_id, self.creator_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Task created successfully.")
        self.destroy()


    def get_user_id_by_username(self, username):
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = cursor.fetchone()
        conn.close()
        return user_id[0] if user_id else None


# class CreateTaskWindow(tk.Toplevel):
#     def __init__(self, master, creator_id):
#         super().__init__(master)
#         self.title("Create New Task")
#         self.geometry("600x400")
#         self.creator_id = creator_id

#         # Set background color for the entire window
#         self.configure(bg='lightblue')

#         # Task Name
#         tk.Label(self, text="Task Name", font=("Arial", 12, "bold"), bg='lightblue').grid(row=0, column=0, padx=10, pady=5, sticky="w")
#         self.task_name_entry = tk.Entry(self)
#         self.task_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

#         # Urgency Level
#         tk.Label(self, text="Urgency Level", font=("Arial", 12, "bold"), bg='lightblue').grid(row=1, column=0, padx=10, pady=5, sticky="w")
#         self.urgency_level = tk.StringVar(self)
#         self.urgency_level.set("Low")  # default value
#         tk.OptionMenu(self, self.urgency_level, "Low", "Medium", "High").grid(row=1, column=1, padx=10, pady=5, sticky="w")

#         # Due Date
#         tk.Label(self, text="Due Date", font=("Arial", 12, "bold"), bg='lightblue').grid(row=2, column=0, padx=10, pady=5, sticky="w")
#         self.due_date_entry = tkcalendar.DateEntry(self)
#         self.due_date_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

#         # Assign to (Username)
#         tk.Label(self, text="Assign to (Username)", font=("Arial", 12, "bold"), bg='lightblue').grid(row=3, column=0, padx=10, pady=5, sticky="w")
#         self.assign_to_entry = tk.Entry(self)
#         self.assign_to_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

#         # Create Task Button
#         tk.Button(self, text="Create Task", command=self.add_task_to_db, bg='lightgreen').grid(row=4, column=0, columnspan=2, pady=10)

#     def get_user_role_by_id(self, user_id):
#         conn = sqlite3.connect('task_manager.db')
#         cursor = conn.cursor()
#         cursor.execute('SELECT role FROM users WHERE id = ?', (user_id,))
#         role = cursor.fetchone()
#         conn.close()
#         return role[0] if role else None
    
#     def add_task_to_db(self):
#         task_name = self.task_name_entry.get()
#         urgency = self.urgency_level.get()
#         due_date = self.due_date_entry.get()
#         assign_to_username = self.assign_to_entry.get()

#         assign_to_id = self.get_user_id_by_username(assign_to_username)
#         if assign_to_id is None:
#             messagebox.showerror("Error", "Developer username not found.")
#             return

#         # Add task to the database
#         conn = sqlite3.connect('task_manager.db')
#         cursor = conn.cursor()
#         cursor.execute('''
#             INSERT INTO tasks (title, description, urgency, due_date, assigned_to, created_by)
#             VALUES (?, ?, ?, ?, ?, ?)
#         ''', (task_name, f"Urgency: {urgency}, Due: {due_date}", urgency, due_date, assign_to_id, self.creator_id))
#         conn.commit()
#         conn.close()

#         messagebox.showinfo("Success", "Task created successfully.")
#         self.destroy()


#     def get_user_id_by_username(self, username):
#         conn = sqlite3.connect('task_manager.db')
#         cursor = conn.cursor()
#         cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
#         user_id = cursor.fetchone()
#         conn.close()
#         return user_id[0] if user_id else None


class DeveloperWindow(tk.Toplevel):
    def __init__(self, master, user_id, username):
        super().__init__(master)
        self.title("Developer Dashboard")
        self.geometry("1200x400")
        self.user_id = user_id
        self.configure(bg='lightblue')
        label_font = ("Arial", 14, "bold")  # Change font style as needed
        background_color = "lightblue"  # Change background color as needed





        # Treeview setup
        self.tasks_tree = ttk.Treeview(self, columns=('ID', 'Title', 'Urgency', 'Due Date', 'Assigned By', 'Phase'), show='headings')
        # self.tasks_tree.column('ID', width=30)
        # self.tasks_tree.column('Title', width=120)
        # self.tasks_tree.column('Urgency', width=80)
        # self.tasks_tree.column('Due Date', width=80)
        # self.tasks_tree.column('Assigned By', width=100)
        # self.tasks_tree.column('Phase', width=100)
        self.tasks_tree.heading('ID', text='ID')
        self.tasks_tree.heading('Title', text='Title')
        self.tasks_tree.heading('Urgency', text='Urgency')
        self.tasks_tree.heading('Due Date', text='Due Date')
        self.tasks_tree.heading('Assigned By', text='Assigned By')
        self.tasks_tree.heading('Phase', text='Phase')
        self.tasks_tree.pack(expand=True, fill='both')

        self.load_tasks()

        # Update Task Phase Button
        tk.Button(self, text="Update Task Phase", command=self.update_task_phase, bg='lightcoral').pack()

        self.account_frame = self.init_account_frame(username)
        tk.Button(self, text="Account", command=lambda: self.toggle_frame(self.account_frame), bg='lightgreen').pack()

    def load_tasks(self):
        tasks = get_developer_tasks(self.user_id)
        for task in tasks:
            assigned_by_username = self.get_username_by_id(task['created_by'])
            self.tasks_tree.insert('', 'end', values=(task['id'], task['title'], task['urgency'], task['due_date'], assigned_by_username, task['status']))

    def get_username_by_id(self, user_id):
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
        username = cursor.fetchone()
        conn.close()
        return username[0] if username else 'Unknown'

    def update_task_phase(self):
        selected_item = self.tasks_tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "No task selected")
            return

        task_id = self.tasks_tree.item(selected_item)['values'][0]
        new_phase = simpledialog.askstring("Input", "Enter new phase (Not Started, In Progress, Finished)", parent=self)

        if new_phase not in ["Not Started", "In Progress", "Finished"]:
            messagebox.showerror("Error", "Invalid phase entered")
            return

        # Update task phase in the database
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_phase, task_id))
        conn.commit()
        conn.close()

        # Refresh the task list
        self.tasks_tree.delete(*self.tasks_tree.get_children())
        self.load_tasks()

    # ... (rest of the DeveloperWindow class) ...
    def init_account_frame(self, username):
        frame = tk.Frame(self, bg="lightblue")

        tk.Label(frame, text=f"Account: {username}", bg="lightgreen").pack(pady=10)
        tk.Button(frame, text="Logout", command=self.logout, bg='lightcoral').pack(pady=10)

        return frame

    def toggle_frame(self, frame):
        if frame.winfo_ismapped():
            frame.pack_forget()
        else:
            frame.pack(side="bottom", fill="y")

    def logout(self):
        self.destroy()


def get_developer_tasks(developer_id):
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, title, urgency, due_date, created_by, status FROM tasks 
        WHERE assigned_to = ?
    ''', (developer_id,))
    tasks = [{'id': row[0], 'title': row[1], 'urgency': row[2], 'due_date': row[3], 'created_by': row[4], 'status': row[5]} for row in cursor.fetchall()]
    conn.close()
    return tasks

if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()
