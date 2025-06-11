#importin GUI
import tkinter as tk
from tkinter import messagebox, simpledialog

#importing json
import json
import os


DATA_FILE = "todolist.json"
'''json file to save the data'''

#adding classes for the overview

class Task:
    '''Representing the various functions like completion, reminding, and marking the task as important'''
    def __init__(self, description):
        '''adding descriptions to each task'''
        self.description = description
        self.completed = False
        self.important = False
        self.reminder = None

    def mark_completed(self):
        '''task completed'''
        self.completed = True

    def set_reminder(self, day):
        '''setting the reminder'''
        self.reminder = day

    def mark_important(self):
        '''making sure to add an important mark to distinguish between all the tasks'''
        self.important = True

    def __str__(self):
        status = '[x]' if self.completed else '[ ]'
        important = '(!)' if self.important else ''
        reminder = f" - Reminder: {self.reminder}" if self.reminder else ''
        return f"{status} {self.description} {important}{reminder}"

class User:
    '''Showing the user with the chosen username, password, and the list of tasks they added'''
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tasks = []

    def add_task(self, description):
        '''adding task'''
        task = Task(description)
        self.tasks.append(task)

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def list_tasks(self):
        return [str(task) for task in self.tasks]

class ToDoApp(tk.Tk):
    '''Main application class/ includes the GUI as well as the user interactions'''
    def __init__(self):
        '''Initialize the to-do list app GUI and loads the login screen'''
        super().__init__()
        self.title("To-Do List App")
        self.geometry('400x500')
        self.configure(bg='#f0f8ff')
        self.users = {}
        self.load_data()  # Load data from json file
        self.current_user = None
        self.login_screen()

    def save_data(self):
        """Save all user data to a JSON file."""
        data = {}
        for username, user in self.users.items():
            data[username] = {
                'password': user.password,
                'tasks': [{
                    'description': t.description,
                    'completed': t.completed,
                    'important': t.important,
                    'reminder': t.reminder
                } for t in user.tasks]
            }
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        """Load user data from a JSON file."""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                raw_data = json.load(f)
                for username, udata in raw_data.items():
                    user = User(username, udata['password'])
                    for tdata in udata['tasks']:
                        task = Task(tdata['description'])
                        task.completed = tdata['completed']
                        task.important = tdata['important']
                        task.reminder = tdata['reminder']
                        user.tasks.append(task)
                    self.users[username] = user

    # GUI Screens
    def login_screen(self):
        '''Login and registration screen'''
        self.clear_window()
        tk.Label(self, text='To-Do List App', font=('Helvetica', 18, 'bold'), bg='#f0f8ff', fg='#4682b4').pack(pady=20)
        tk.Label(self, text='Login or Register', font=('Arial', 14), bg='#f0f8ff', fg='#5f9ea0').pack(pady=10)
        tk.Button(self, text='Login', command=self.login, bg='#5f9ea0', fg='white', width=15).pack(pady=10)
        tk.Button(self, text='Register', command=self.register, bg='#4682b4', fg='white', width=15).pack(pady=10)

    def task_screen(self):
        '''Displaying the functions on the screen for the user'''
        #Using colors that are aesthetically pleasing for the user 
        self.clear_window()
        tk.Label(self, text=f"Welcome {self.current_user.username}", font=('Helvetica', 16, 'bold'), bg='#f0f8ff', fg='#4682b4').pack(pady=10)
        self.task_listbox = tk.Listbox(self, width=50, height=15, bg='#ffffff', fg='#000000', selectbackground='#4682b4', selectforeground='white')
        self.task_listbox.pack(pady=10)
        self.refresh_task_list()

        tk.Button(self, text='Add Task', command=self.add_task, bg='#4682b4', fg='white', width=20).pack(pady=5)
        tk.Button(self, text='Mark as Done', command=self.mark_done, bg='#5f9ea0', fg='white', width=20).pack(pady=5)
        tk.Button(self, text='Delete Task', command=self.delete_task, bg='#4682b4', fg='white', width=20).pack(pady=5)
        tk.Button(self, text='Add Reminder', command=self.add_reminder, bg='#5f9ea0', fg='white', width=20).pack(pady=5)
        tk.Button(self, text='Mark as Important', command=self.mark_important, bg='#4682b4', fg='white', width=20).pack(pady=5)
        tk.Button(self, text='Logout', command=self.logout, bg='#5f9ea0', fg='white', width=20).pack(pady=10)

    # GUI Actions
    def register(self):
        '''Register a new user where they can choose their username and password'''
        username = simpledialog.askstring('Register', 'Username:')
        if username in self.users:
            messagebox.showerror('Error', 'Username already exists.')
            return
        password = simpledialog.askstring('Register', 'Password:', show='*')
        self.users[username] = User(username, password)
        self.save_data()  # Save data to JSON after registration
        messagebox.showinfo('Success', 'Registration complete.')

    def login(self):
        '''Login with the username and password they chose'''
        username = simpledialog.askstring('Login', 'Username:')
        password = simpledialog.askstring('Login', 'Password:', show='*')
        user = self.users.get(username)
        if user and user.password == password:
            self.current_user = user
            self.task_screen()
        else:
            messagebox.showerror('Error', 'Invalid credentials.')

    def logout(self):
        '''Log out the current user and return them to the login screen'''
        self.current_user = None
        self.login_screen()

    def add_task(self):
        '''Add task to the current user's list'''
        desc = simpledialog.askstring('New Task', 'Enter task description:')
        if desc:
            self.current_user.add_task(desc)
            self.save_data()  # Save data after adding a task
            self.refresh_task_list()

    def mark_done(self):
        '''Mark selected task as done'''
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            self.current_user.tasks[index].mark_completed()
            self.save_data()  # Save data after marking a task done
            self.refresh_task_list()
        else:
            messagebox.showwarning('Warning', 'No task selected.')

    def delete_task(self):
        '''Delete selected task from the list'''
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            self.current_user.delete_task(index)
            self.save_data()  # Save data after deleting a task
            self.refresh_task_list()
        else:
            messagebox.showwarning('Warning', 'No task selected.')

    def add_reminder(self):
        '''Add reminder to selected task/ reminder dont have the limit for weekdays and user can choose freely what the reminder can be'''
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            reminder = simpledialog.askstring('Add Reminder', 'Enter reminder (e.g., Monday):')
            if reminder:
                self.current_user.tasks[index].set_reminder(reminder)
                self.save_data()  # Save data after adding reminder
                self.refresh_task_list()
        else:
            messagebox.showwarning('Warning', 'No task selected.')

    def mark_important(self):
        '''Mark selected task as important'''
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            self.current_user.tasks[index].mark_important()
            self.save_data()  # Save data after marking a task important
            self.refresh_task_list()
        else:
            messagebox.showwarning('Warning', 'No task selected.')

    def refresh_task_list(self):
        '''Refresh and update the task listbox'''
        self.task_listbox.delete(0, tk.END)
        for task in self.current_user.tasks:
            self.task_listbox.insert(tk.END, str(task))

    def clear_window(self):
        '''Clear all widgets from the current window'''
        for widget in self.winfo_children():
            widget.destroy()

# Start the application
if __name__ == '__main__':
    app = ToDoApp()
    app.mainloop()
