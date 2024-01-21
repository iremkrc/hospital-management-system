import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ScrollableFrameUtil import ScrollableFrame
import mysql.connector
import datetime


class NursesFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        #self.nurse_id = 12365 #hardcoded
        self.current_date = datetime.date(2023, 10, 10)
        self.db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="24632463",
        auth_plugin='mysql_native_password'
        )
        self.db_cursor = self.db_connection.cursor(buffered=True)
        self.db_cursor.execute("USE comp306project")
        self.pack(fill="both", expand=True)
        self.showing_upcoming = False 
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
        nurse_name = self.get_nurse_name(nurse_id)
        if self.authenticate_nurse(nurse_id, password):
            messagebox.showinfo("Login Successful", f"Welcome, Nurse {nurse_name}!")
            self.clear_login_ui()
            self.setup_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid Nurse ID or password")

    def get_nurse_name(self, nurse_id):
        query = "SELECT e.Name FROM nurse n JOIN employee e ON n.EmployeeId = e.EmployeeId WHERE n.EmployeeId = %s;"
        self.db_cursor.execute(query, (nurse_id,))
        result = self.db_cursor.fetchone()
        if result:
            return result[0]
        else:
            return "Unknown"
    
    def authenticate_nurse(self, nurse_id, password):
        query = "SELECT * FROM nurse WHERE nurse.employeeId = %s;"
        self.db_cursor.execute(query, (nurse_id,))
        nurse = self.db_cursor.fetchone()

        if nurse and password == "1234":
            self.nurse_id = nurse_id
            return True
        else:
            return False
    
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
        ttk.Button(self, text="Add a Certificate", command=self.add_certificate_ui).pack(pady=10)
        ttk.Button(self, text="Refer Nurses", command=self.show_refer_nurses_ui).pack(pady=10)

    def add_certificate_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Add a Certificate", font=("Arial", 16)).pack(pady=10)
        self.certificate_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.certificate_var).pack()
        ttk.Button(self, text="Add", command=lambda: self.add_certificate(self.certificate_var.get())).pack(pady=10)
        ttk.Button(self, text="Show My Certificates", command=self.show_my_certificates).pack(pady=5)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)
    
    def add_certificate(self, certificate):
        if certificate:
            query = "SELECT Certificate FROM nurse_certificates WHERE EmployeeId = %s AND Certificate = %s;"
            self.db_cursor.execute(query, (self.nurse_id, certificate))
            existing_certificate = self.db_cursor.fetchone()
            if existing_certificate:
                messagebox.showinfo("Certificate Already Exists", f"Certificate '{certificate}' already exists.")
            else:
                query = "INSERT INTO nurse_certificates (EmployeeId, Certificate) VALUES (%s, %s);"
                values = (self.nurse_id, certificate)
                self.db_cursor.execute(query, values)
                self.db_connection.commit()
                messagebox.showinfo("Certificate Added", f"Certificate '{certificate}' added successfully.")
        else:
            messagebox.showerror("Error", "Certificate cannot be empty.")
    
    def show_my_certificates(self):
        self.clear_ui()
        ttk.Label(self, text="My Certificates", font=("Arial", 16)).pack(pady=10)  
        columns = ("Certificate",)
        certificates_tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            certificates_tree.heading(col, text=col)
            certificates_tree.column(col, width=200)
        self.display_certificates(certificates_tree)    
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=5)
    
    def display_certificates(self, certificates_tree):
        query = "SELECT Certificate FROM nurse_certificates WHERE EmployeeId = %s;"
        self.db_cursor.execute(query, (self.nurse_id,))
        certificates = self.db_cursor.fetchall()
        for certificate in certificates:
            certificates_tree.insert("", 'end', values=(certificate[0],))
        certificates_tree.pack(pady=10)
    
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
        columns = ("AppointmentID", "Duration", "Date", "Floor", "RoomNumber")
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
            SELECT a.AppointmentId, a.Duration, a.Date, a.Floor, a.RoomNumber 
            FROM appointment a 
            JOIN participates p ON a.AppointmentId = p.AppointmentId 
            JOIN nurse n ON p.EmployeeId = n.EmployeeId 
            WHERE n.EmployeeId = %s AND a.Date >= %s;
        """
        self.db_cursor.execute(query, (self.nurse_id, self.current_date))
        appointments = self.db_cursor.fetchall()
        for i in appointment_tree.get_children():
            appointment_tree.delete(i)
        for appointment in appointments:
            appointment_tree.insert("", 'end', values=(appointment[0], appointment[1], appointment[2], appointment[3], appointment[4]))
            
    def show_refer_nurses_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Refer a Nurse", font=("Arial", 16)).pack(pady=10)
        columns = ("EmployeeId", "Name")
        self.nurses_tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.nurses_tree.heading(col, text=col)
            self.nurses_tree.column(col, width=95)
        self.display_nurses(self.nurses_tree)
        ttk.Label(self, text="Reference Points:").pack()
        self.reference_point = tk.StringVar()
        ttk.Entry(self, textvariable=self.reference_point).pack()
        ttk.Button(self, text="Give Reference", command=self.give_reference).pack(pady=10)
        ttk.Button(self, text="Show References Given By Me", command=self.show_references_given).pack(pady=10)
        ttk.Button(self, text="Show References Given To Me", command=self.show_references_given_to_me).pack(pady=10)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def show_references_given_to_me(self):
        self.clear_ui()
        ttk.Label(self, text="References Given To Me", font=("Arial", 16)).pack(pady=10)
        columns = ("Referer Nurse Name", "Referer Nurse ID", "Rating")
        references_tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            references_tree.heading(col, text=col)
            references_tree.column(col, width=95)
        query = """
        SELECT e.Name AS RefererNurseName, nr.RefererNurseId, nr.Rating 
        FROM nurse_references nr
        JOIN employee e ON nr.RefererNurseId = e.EmployeeId
        WHERE nr.RefereeNurseId = %s;
        """
        self.db_cursor.execute(query, (self.nurse_id,))
        references = self.db_cursor.fetchall()
        for reference in references:
            references_tree.insert("", 'end', values=reference)
        references_tree.pack(pady=10)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def show_references_given(self):
        self.clear_ui()
        ttk.Label(self, text="References Given By Me", font=("Arial", 16)).pack(pady=10)
        columns = ("Referee Nurse Name", "Referee Nurse ID", "Rating")
        references_tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            references_tree.heading(col, text=col)
            references_tree.column(col, width=95)
        query = """
        SELECT e.Name AS RefereeNurseName, nr.RefereeNurseId, nr.Rating 
        FROM nurse_references nr
        JOIN employee e ON nr.RefereeNurseId = e.EmployeeId
        WHERE nr.RefererNurseId = %s;
        """
        self.db_cursor.execute(query, (self.nurse_id,))
        references = self.db_cursor.fetchall()
        for reference in references:
            references_tree.insert("", 'end', values=reference)
        references_tree.pack(pady=10)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def display_nurses(self, nurse_tree):
        query = "SELECT employee.employeeId, employee.Name FROM employee JOIN nurse ON nurse.employeeId = employee.employeeId;"
        self.db_cursor.execute(query)
        nurses = self.db_cursor.fetchall()
        for nurse in nurses:
            nurse_tree.insert("", 'end', values=nurse)
        nurse_tree.pack(pady=10)


    def give_reference(self):
        selected_items = self.nurses_tree.selection()
        points = self.reference_point.get()
        
        if selected_items and points.isdigit():
            selected_nurse = self.nurses_tree.item(selected_items[0])['values']
            referee_nurse_id = selected_nurse[0]
            referrer_nurse_id = self.nurse_id_var.get()
            query_check = "SELECT * FROM nurse_references WHERE RefereeNurseId = %s AND RefererNurseId = %s;"
            self.db_cursor.execute(query_check, (referee_nurse_id, referrer_nurse_id))
            existing_reference = self.db_cursor.fetchone()
            if existing_reference:
                query_update = "UPDATE nurse_references SET Rating = %s WHERE RefereeNurseId = %s AND RefererNurseId = %s;"
                values_update = (int(points), referee_nurse_id, referrer_nurse_id)
                self.db_cursor.execute(query_update, values_update)
            else:
                query_insert = "INSERT INTO nurse_references (RefereeNurseId, RefererNurseId, Rating) VALUES (%s, %s, %s);"
                values_insert = (referee_nurse_id, referrer_nurse_id, int(points))
                self.db_cursor.execute(query_insert, values_insert)
            self.db_connection.commit()
            messagebox.showinfo("Reference Given", f"Reference given to Nurse ID {referee_nurse_id} with {points} points.")
        else:
            messagebox.showerror("Error", "Please select a nurse and enter valid reference points.")
