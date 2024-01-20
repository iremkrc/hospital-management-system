import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector
import datetime



class DoctorsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.patient_tree = None 
        self.current_date = datetime.date(2023, 10, 10)
        #self.doctor_id = 10847 #hardcoded
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
        self.selected_patient_var = tk.StringVar()
        self.showing_upcoming = False 
        self.setup_login_ui()

    def setup_login_ui(self):
        self.login_label = ttk.Label(self, text="Doctor Login", font=("Arial", 18))
        self.login_label.pack(pady=10)
        self.doctor_id_var = tk.StringVar()
        self.doctor_password_var = tk.StringVar()
        ttk.Label(self, text="Doctor ID:").pack()
        ttk.Entry(self, textvariable=self.doctor_id_var).pack()
        ttk.Label(self, text="Password:").pack()
        ttk.Entry(self, textvariable=self.doctor_password_var, show="*").pack()
        ttk.Button(self, text="Login", command=self.doctor_login).pack(pady=10)

    def doctor_login(self):
        doctor_id = self.doctor_id_var.get()
        password = self.doctor_password_var.get()

        if not doctor_id or not password:
            messagebox.showerror("Login Failed", "Doctor ID and Password cannot be empty.")
            return

        if self.authenticate_doctor(doctor_id, password):
            messagebox.showinfo("Login Successful", "Welcome!")
            self.clear_login_ui()
            self.setup_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid Doctor ID or password")

    def authenticate_doctor(self, doctor_id, password):
        query = "SELECT * FROM doctor WHERE doctor.employeeId = %s;"
        self.db_cursor.execute(query, (doctor_id,))
        doctor = self.db_cursor.fetchone()

        if doctor and password == "1234":
            self.doctor_id = doctor_id
            return True
        else:
            return False
    
    def load_doctor_functions(self):
        self.patient_list_label = ttk.Label(self.functional_frame, text="Patients", font=("Arial", 16))
        self.patient_list_label.pack(pady=10)
        self.patient_filter_var = tk.StringVar()
        self.patient_filter_entry = ttk.Entry(self.functional_frame, textvariable=self.patient_filter_var)
        self.patient_filter_entry.pack()
        self.patient_listbox = tk.Listbox(self.functional_frame)
        self.patient_listbox.pack(pady=10)
        self.display_patients()
        self.prescription_label = ttk.Label(self.functional_frame, text="Write Prescription", font=("Arial", 16))
        self.prescription_label.pack(pady=10)
        ttk.Label(self.functional_frame, text="Select Patient:").pack()
        self.selected_patient_var = tk.StringVar()
        self.selected_patient_combobox = ttk.Combobox(self.functional_frame, textvariable=self.selected_patient_var, state="readonly")
        self.selected_patient_combobox.pack()
        ttk.Label(self.functional_frame, text="Prescription:").pack()
        self.prescription_text = scrolledtext.ScrolledText(self.functional_frame, wrap=tk.WORD, height=5)
        self.prescription_text.pack(pady=10)
        ttk.Button(self.functional_frame, text="Issue Prescription", command=self.issue_prescription).pack()
        self.appointment_list_label = ttk.Label(self.functional_frame, text="Appointments", font=("Arial", 16))
        self.appointment_list_label.pack(pady=10)
        self.appointment_listbox = tk.Listbox(self.functional_frame)
        self.appointment_listbox.pack(pady=10)

    def clear_login_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

    def setup_main_menu(self):
        self.clear_ui()
        ttk.Button(self, text="Show My Patients", command=self.show_patients_ui).pack(pady=10)
        ttk.Button(self, text="Show My Appointments", command=self.show_appointments_ui).pack(pady=10)
        ttk.Button(self, text="Issue Prescription", command=self.show_prescription_ui).pack(pady=10)

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

    def clear_appointment_tree(self, appointment_tree):
        for item in appointment_tree.get_children():
            appointment_tree.delete(item)
            
    def toggle_appointments_view(self, appointment_tree, button):
        self.clear_appointment_tree(appointment_tree) 

        if self.showing_upcoming:
            self.display_appointments(appointment_tree)
            button.config(text="Show Upcoming Appointments")
        else:
            self.display_upcoming_appointments(appointment_tree)
            button.config(text="Show All Appointments")
        self.showing_upcoming = not self.showing_upcoming
        
    def show_appointments_ui(self):
        self.clear_ui()
        current_date_label = ttk.Label(self, text=f"Date: {self.current_date.strftime('%d.%m.%Y')}", font=("Arial", 12))
        current_date_label.pack(side="top", anchor="ne", padx=10, pady=10)
        ttk.Label(self, text="My Appointments", font=("Arial", 16)).pack(pady=10)
        columns = ("AppointmentID", "Duration", "Date", "Floor", "RoomNumber", "PatientSSN", "Name")
        appointment_tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            appointment_tree.heading(col, text=col)
            appointment_tree.column(col, width=95)
        self.display_appointments(appointment_tree)
        toggle_button = ttk.Button(self, text="Show Upcoming Appointments", 
                                   command=lambda: self.toggle_appointments_view(appointment_tree, toggle_button))
        toggle_button.pack(pady=5)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def display_upcoming_appointments(self, appointment_tree):
        query = """
        SELECT a.AppointmentId, a.Duration, a.Date, a.Floor, a.RoomNumber, p.PatientSSN, p.Name
        FROM appointment a 
        JOIN participates pa ON a.AppointmentId = pa.AppointmentId 
        JOIN doctor d ON pa.EmployeeId = d.EmployeeId 
        JOIN patient p ON pa.PatientSSN = p.PatientSSN 
        WHERE d.EmployeeId = %s AND a.Date >= %s;
        """
        self.db_cursor.execute(query, (self.doctor_id, self.current_date))
        appointments = self.db_cursor.fetchall()
        for i in appointment_tree.get_children():
            appointment_tree.delete(i)
        for appointment in appointments:
            appointment_tree.insert("", 'end', values=(appointment[0], appointment[1], appointment[2], appointment[3], appointment[4], appointment[5], appointment[6]))

            
    def show_prescription_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Select Patient for Prescription", font=("Arial", 16)).pack(pady=10)
        columns = ("PatientSSN", "PhoneNumber", "Name", "BirthDate", "BloodType", "City", "Street", "State", "Sex")
        self.patient_tree = ttk.Treeview(self, columns=columns, show='headings')

        for col in columns:
            self.patient_tree.heading(col, text=col)
            self.patient_tree.column(col, width=95)
        self.display_patients(self.patient_tree)
        self.patient_tree.pack(pady=10)
        self.patient_tree.bind('<<TreeviewSelect>>', self.on_patient_selected)

        ttk.Label(self, text="Prescription:").pack()
        self.prescription_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=10)
        self.prescription_text.pack(pady=10)

        ttk.Button(self, text="Issue Prescription", command=self.issue_prescription).pack(pady=10)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)
    
    def on_patient_selected(self, event):
        selected = event.widget.selection()
        if selected:
            index = selected[0]
            selected_patient = event.widget.item(index)['values']
            self.selected_patient_var.set(selected_patient)

    def issue_prescription(self):
        selected_items = self.patient_tree.selection()
        if selected_items:
            selected_patient = self.patient_tree.item(selected_items[0])['values']
            prescription = self.prescription_text.get("1.0", tk.END).strip()
            if prescription:
                patient_name = selected_patient[2]
                messagebox.showinfo("Prescription Issued", f"Prescription {prescription} issued to Patient {patient_name}.")
                self.prescription_text.delete("1.0", tk.END)
            else:
                messagebox.showerror("Error", "Please write a prescription.")
        else:
            messagebox.showerror("Error", "Please select a patient.")

    def clear_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

    def display_patients(self, patient_tree):
        query = """
        SELECT * 
        FROM patient p 
        JOIN participates par ON p.PatientSSN = par.PatientSSN 
        JOIN doctor d ON par.EmployeeId = d.EmployeeId 
        WHERE d.EmployeeId = %s;"""
        self.db_cursor.execute(query, (self.doctor_id,))
        patients = self.db_cursor.fetchall()
        for patient in patients:
            patient_tree.insert("", 'end', values=(patient[0], patient[1], patient[2], patient[3], patient[4], patient[5], patient[6], patient[7], patient[8]))
        
        patient_tree.pack(pady=10)
    

    def display_appointments(self, appointment_tree):
        query = """
        SELECT a.AppointmentId, a.Duration, a.Date, a.Floor, a.RoomNumber, p.PatientSSN, p.Name
        FROM appointment a
        JOIN participates pa ON a.AppointmentId = pa.AppointmentId
        JOIN doctor d ON pa.EmployeeId = d.EmployeeId
        JOIN patient p ON pa.PatientSSN = p.PatientSSN
        WHERE d.EmployeeId = %s;
        """
        self.db_cursor.execute(query, (self.doctor_id,))
        appointments = self.db_cursor.fetchall()
        for appointment in appointments:
            appointment_tree.insert("", 'end', values=(appointment[0], appointment[1], appointment[2], appointment[3], appointment[4], appointment[5], appointment[6]))

        appointment_tree.pack(pady=10)