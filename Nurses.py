import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class NursesFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(fill="both", expand=True)
        self.login_label = ttk.Label(self, text="Nurse Login", font=("Arial", 18))
        self.login_label.pack(pady=10)
        self.nurse_ssn_var = tk.StringVar()
        self.nurse_password_var = tk.StringVar()
        ttk.Label(self, text="SSN:").pack()
        ttk.Entry(self, textvariable=self.nurse_ssn_var).pack()
        ttk.Label(self, text="Password:").pack()
        ttk.Entry(self, textvariable=self.nurse_password_var, show="*").pack()
        ttk.Button(self, text="Login", command=self.nurse_login).pack(pady=10)
        self.functional_frame = tk.Frame(self)
    
    def nurse_login(self):
        ssn = self.nurse_ssn_var.get()
        password = self.nurse_password_var.get()
        if self.authenticate_nurse(ssn, password):
            messagebox.showinfo("Login Successful", "Welcome!")
            self.functional_frame.pack(fill="both", expand=True)
            self.load_nurse_functions()
        else:
            messagebox.showerror("Login Failed", "Invalid SSN or password")


    def authenticate_nurse(self, ssn, password):
        return True
    
    def display_nurses(self):
        nurse_names = ['Nurse A', 'Nurse B', 'Nurse C']  #replace
        for name in nurse_names:
            self.nurses_listbox.insert(tk.END, name)
        self.reference_combobox['values'] = nurse_names

    def give_reference(self):
        selected_nurse = self.selected_nurse.get()
        points = self.reference_point.get()
        print(f"Reference given to {selected_nurse} with {points} points.")
        