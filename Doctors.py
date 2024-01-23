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
        passwd="Keremiis123!",
        auth_plugin='mysql_native_password'
        )
        self.db_cursor = self.db_connection.cursor(buffered=True)
        self.db_cursor.execute("USE comp306project")
        self.pack(fill="both", expand=True)
        self.selected_patient_var = tk.StringVar()
        self.prescription_id_var = tk.StringVar()
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
        doctor_name = self.get_doctor_name(doctor_id) 
        if self.authenticate_doctor(doctor_id, password):
            messagebox.showinfo("Login Successful", f"Welcome, Dr. {doctor_name}!") 
            self.clear_login_ui()
            self.setup_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid Doctor ID or password")

    def get_doctor_name(self, doctor_id):
        query = "SELECT e.Name FROM doctor d JOIN employee e ON d.EmployeeId = e.EmployeeId WHERE d.EmployeeId = %s;"
        self.db_cursor.execute(query, (doctor_id,))
        result = self.db_cursor.fetchone()
        if result:
            return result[0]
        else:
            return "Unknown"
    
    def authenticate_doctor(self, doctor_id, password):
        query = "SELECT * FROM doctor WHERE doctor.employeeId = %s;"
        self.db_cursor.execute(query, (doctor_id,))
        doctor = self.db_cursor.fetchone()

        if doctor and password == "1234":
            self.doctor_id = doctor_id
            return True
        else:
            return False

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
        
        columns = ("PatientSSN", "PhoneNumber", "Name", "BirthDate", "BloodType", "Sex")
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

        columns = ("PatientSSN", "PhoneNumber", "Name", "BirthDate", "BloodType", "Sex")
        self.patient_tree = ttk.Treeview(self, columns=columns, show='headings')

        for col in columns:
            self.patient_tree.heading(col, text=col)
            self.patient_tree.column(col, width=95)
        self.display_patients(self.patient_tree)
        self.patient_tree.pack(pady=10)
        self.patient_tree.bind('<<TreeviewSelect>>', self.on_patient_selected)
        ttk.Label(self, text="Diagnosis:").pack()
        self.diagnosis_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.diagnosis_var).pack()
        ttk.Label(self, text="Medicines (one per line):").pack()
        self.medicines_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=5)
        self.medicines_text.pack(pady=10)
        ttk.Button(self, text="Issue Prescription", command=self.issue_prescription).pack(pady=10)
        ttk.Button(self, text="Show Prescriptions", command=self.show_prescriptions).pack(pady=10)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)
    
    def show_prescriptions(self):
        self.clear_ui()
        ttk.Label(self, text="Patients and Prescriptions", font=("Arial", 16)).pack(pady=10)
        columns = ("PatientSSN", "PhoneNumber", "Name", "BirthDate", "BloodType", "Sex", "PrescriptionId", "Diagnosis", "Medicine", "WritingDate")
        combined_tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            combined_tree.heading(col, text=col)
            combined_tree.column(col, width=95) 
        query_combined = "SELECT p.PatientSSN, p.PhoneNumber, p.Name, p.BirthDate, p.BloodType, p.Sex, " \
                    "pr.PrescriptionId, pr.Diagnosis, pm.Medicine, w.WritingDate " \
                    "FROM patient p " \
                    "LEFT JOIN writes w ON p.PatientSSN = w.PatientSSN " \
                    "LEFT JOIN prescription pr ON w.PrescriptionId = pr.PrescriptionId " \
                    "LEFT JOIN prescription_medicine pm ON pr.PrescriptionId = pm.PrescriptionId " \
                    "WHERE w.DoctorId = %s;" 
        self.db_cursor.execute(query_combined, (self.doctor_id,)) 
        combined_data = self.db_cursor.fetchall()
        for data in combined_data:
            combined_tree.insert("", 'end', values=data)

        combined_tree.pack(pady=10)
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
            diagnosis = self.diagnosis_var.get().strip()
            medicines = self.medicines_text.get("1.0", tk.END).strip().splitlines() 
            if diagnosis and medicines:
                query = "INSERT INTO prescription (Diagnosis) VALUES (%s);"
                self.db_cursor.execute(query, (diagnosis,))
                self.db_connection.commit()
                prescription_id = self.db_cursor.lastrowid
                for medicine in medicines:
                    query = "INSERT INTO prescription_medicine (PrescriptionId, Medicine) VALUES (%s, %s);"
                    self.db_cursor.execute(query, (prescription_id, medicine.strip()))
                    self.db_connection.commit()
                writing_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                query = "INSERT INTO writes (PatientSSN, PrescriptionId, DoctorId, WritingDate) VALUES (%s, %s, %s, %s);"
                self.db_cursor.execute(query, (selected_patient[0], prescription_id, self.doctor_id, writing_date))
                self.db_connection.commit()
                patient_name = selected_patient[2]
                self.prescription_id_var.set(prescription_id)
                messagebox.showinfo("Prescription Issued", f"Prescription for the disease '{diagnosis}' with medicines issued to Patient {patient_name}.")
                self.diagnosis_var.set("")  
                self.medicines_text.delete("1.0", tk.END)
            else:
                messagebox.showerror("Error", "Please provide both a diagnosis and at least one medicine.")
        else:
            messagebox.showerror("Error", "Please select a patient.")

    def clear_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

    def display_patients(self, patient_tree):
        query = """
        SELECT p.PatientSSN, p.PhoneNumber, p.Name, p.BirthDate, p.BloodType, p.Sex
        FROM patient p
        JOIN participates par ON p.PatientSSN = par.PatientSSN
        JOIN doctor d ON par.EmployeeId = d.EmployeeId
        WHERE d.EmployeeId = %s;"""
        self.db_cursor.execute(query, (self.doctor_id,))
        patients = self.db_cursor.fetchall()
        for patient in patients:
            patient_tree.insert("", 'end', values=(patient[0], patient[1], patient[2], patient[3], patient[4], patient[5]))
        
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