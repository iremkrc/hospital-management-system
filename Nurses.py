import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ScrollableFrameUtil import ScrollableFrame
import mysql.connector


class NursesFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.nurse_id = 11270 #hardcoded
        self.db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password",
        auth_plugin='mysql_native_password'
        )
        print(self.db_connection)
        self.db_cursor = self.db_connection.cursor(buffered=True)
        self.db_cursor.execute("USE comp306project")
        self.pack(fill="both", expand=True)
        self.setup_login_ui()


    def setup_login_ui(self):
        self.login_label = ttk.Label(self, text="Nurse Login", font=("Arial", 18))
        self.login_label.pack(pady=10)
        self.nurse_id_var = tk.StringVar()
        self.nurse_password_var = tk.StringVar()
        ttk.Label(self, text="Nurse ID:").pack()
        ttk.Entry(self, textvariable=self.nurse_id_var).pack()
        ttk.Label(self, text="Password:").pack()
        ttk.Entry(self, textvariable=self.nurse_password_var, show="*").pack()
        ttk.Button(self, text="Login", command=self.nurse_login).pack(pady=10)

    def nurse_login(self):
        nurse_id = self.nurse_id_var.get()
        password = self.nurse_password_var.get()

        if not nurse_id or not password:
            messagebox.showerror("Login Failed", "Nurse ID and Password cannot be empty.")
            return

        if self.authenticate_nurse(nurse_id, password):
            messagebox.showinfo("Login Successful", "Welcome!")
            self.clear_login_ui()
            self.setup_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid Nurse ID or password")

    def load_nurse_functions(self):
        self.patient_list_label = ttk.Label(self.functional_frame, text="Patients", font=("Arial", 16))
        self.patient_list_label.pack(pady=10)
        self.patient_listbox = tk.Listbox(self.functional_frame)
        self.patient_listbox.pack(pady=10)
        self.display_patients()
        self.appointment_list_label = ttk.Label(self.functional_frame, text="Appointments", font=("Arial", 16))
        self.appointment_list_label.pack(pady=10)
        self.appointment_listbox = tk.Listbox(self.functional_frame)
        self.appointment_listbox.pack(pady=10)

    def authenticate_nurse(self, ssn, password):
        return True
            
    def display_patients(self, patient_tree):
        query = "SELECT * FROM patient p JOIN participates par ON p.PatientSSN = par.PatientSSN JOIN nurse n ON par.EmployeeId = n.EmployeeId WHERE n.EmployeeId = %s;"
        self.db_cursor.execute(query, (self.nurse_id,))
        patients = self.db_cursor.fetchall()
        for patient in patients:
            patient_tree.insert("", 'end', values=(patient[0], patient[1], patient[2], patient[3], patient[4], patient[5], patient[6], patient[7], patient[8]))
        
        patient_tree.pack(pady=10)

    def display_appointments(self, appointment_tree):
        query = "SELECT a.AppointmentId, a.Duration, a.Date, a.Floor, a.RoomNumber FROM appointment a JOIN participates p ON a.AppointmentId = p.AppointmentId JOIN nurse n ON p.EmployeeId = n.EmployeeId WHERE n.EmployeeId = %s;"
        self.db_cursor.execute(query, (self.nurse_id,))
        appointments = self.db_cursor.fetchall()
        for appointment in appointments:
            appointment_tree.insert("", 'end', values=(appointment[0], appointment[1], appointment[2], appointment[3], appointment[4]))
        appointment_tree.pack(pady=10)

    def clear_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

    def clear_login_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

    def setup_main_menu(self):
        self.clear_ui()
        ttk.Button(self, text="Show My Patients", command=self.show_patients_ui).pack(pady=10)
        ttk.Button(self, text="Show My Appointments", command=self.show_appointments_ui).pack(pady=10)
        ttk.Button(self, text="Refer Nurses", command=self.show_refer_nurses_ui).pack(pady=10)

    def show_patients_ui(self):
        self.clear_ui()
        ttk.Label(self, text="My Patients", font=("Arial", 16)).pack(pady=10)

        columns = ("PatientSSN", "PhoneNumber", "Name", "BirthDate", "BloodType", "City", "Street", "State", "Sex")
        patient_tree = ttk.Treeview(self, columns=columns, show='headings')

        for col in columns:
            patient_tree.heading(col, text=col)
            patient_tree.column(col, width=95)
        self.display_patients(patient_tree)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def show_appointments_ui(self):
        self.clear_ui()
        ttk.Label(self, text="My Appointments", font=("Arial", 16)).pack(pady=10)
        columns = ("AppointmentID", "Duration", "Date", "Floor", "RoomNumber")
        appointment_tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            appointment_tree.heading(col, text=col)
            appointment_tree.column(col, width=95)
        self.display_appointments(appointment_tree)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def show_refer_nurses_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Refer a Nurse", font=("Arial", 16)).pack(pady=10)
        columns = ("EmployeeId", "EmployeeSSN", "Name", "Sex", "BirthDate", "Salary", "HireDate", "City", "Street", "State")
        self.nurses_tree = ttk.Treeview(self, columns=columns, show='headings')

        for col in columns:
            self.nurses_tree.heading(col, text=col)
            self.nurses_tree.column(col, width=95)
        self.display_nurses(self.nurses_tree)

        ttk.Label(self, text="Reference Points:").pack()
        self.reference_point = tk.StringVar()
        ttk.Entry(self, textvariable=self.reference_point).pack()
        ttk.Button(self, text="Give Reference", command=self.give_reference).pack(pady=10)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)


    def display_nurses(self, nurse_tree):
        query = "select * from employee, nurse where nurse.employeeId = employee.employeeId;"
        self.db_cursor.execute(query)
        nurses = self.db_cursor.fetchall()
        for nurse in nurses:
            nurse_tree.insert("", 'end', values=(nurse[0], nurse[1], nurse[2], nurse[3], nurse[4], nurse[5], nurse[6], nurse[7], nurse[8], nurse[9]))
        nurse_tree.pack(pady=10)


    def give_reference(self):
        selected_items = self.nurses_tree.selection()
        points = self.reference_point.get()
        if selected_items and points.isdigit():
            selected_nurse = self.nurses_tree.item(selected_items[0])['values']
            nurse_name = selected_nurse[2]
            messagebox.showinfo("Reference Given", f"Reference given to {nurse_name} with {points} points.")
        else:
            messagebox.showerror("Error", "Please select a nurse and enter valid reference points.")
