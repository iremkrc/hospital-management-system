import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from Appointments import AppointmentsFrame, get_appointments

class PatientsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.appointments_list = []
        #self.appointments_controller = AppointmentsFrame()
        self.current_date = datetime.date(2023, 10, 10)
        self.db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="pwd",
        auth_plugin='mysql_native_password'
        )
        self.db_cursor = self.db_connection.cursor(buffered=True)
        self.db_cursor.execute("USE comp306project")
        self.pack(fill="both", expand=True)
        self.showing_upcoming = False 
        self.setup_login_ui()


    def setup_login_ui(self):
        self.login_label = ttk.Label(self, text="Patient Login", font=("Arial", 18))
        self.login_label.pack(pady=10)
        self.patient_ssn_var = tk.StringVar()
        self.patient_password_var = tk.StringVar()
        ttk.Label(self, text="SSN:").pack()
        ttk.Entry(self, textvariable=self.patient_ssn_var).pack()
        ttk.Label(self, text="Password:").pack()
        ttk.Entry(self, textvariable=self.patient_password_var, show="*").pack()
        ttk.Button(self, text="Login", command=self.patient_login).pack(pady=10)


    def patient_login(self):
        patient_ssn = self.patient_ssn_var.get()
        password = self.patient_password_var.get()

        if not patient_ssn or not password:
            messagebox.showerror("Login Failed", "Patient SSN or Password cannot be empty.")
            return

        if self.authenticate_patient(patient_ssn, password):
            messagebox.showinfo("Login Successful", "Welcome!")
            self.clear_login_ui()
            self.setup_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid Patient SSN or password")


    def authenticate_patient(self, ssn, password):
        query = "SELECT * FROM patient WHERE patient.PatientSSN = %s;"
        self.db_cursor.execute(query, (ssn,))
        patient = self.db_cursor.fetchone()

        if patient and password == "1234":
            self.ssn = ssn
            return True
        else:
            return False


    def clear_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

    def clear_login_ui(self):
        for widget in self.winfo_children():
            widget.destroy()


    def load_patient_functions(self):
        self.doctor_list_label = ttk.Label(self.functional_frame, text="Doctors", font=("Arial", 16))
        self.doctor_list_label.pack(pady=10)
        self.doctor_listbox = tk.Listbox(self.functional_frame)
        self.doctor_listbox.pack(pady=10)
        self.display_doctors(self.doctor_listbox)
        self.appointment_list_label = ttk.Label(self.functional_frame, text="Appointments", font=("Arial", 16))
        self.appointment_list_label.pack(pady=10)
        self.appointment_listbox = tk.Listbox(self.functional_frame)
        self.appointment_listbox.pack(pady=10)
        self.update_patient_combobox()

######################################################################################## 

    def get_patient_info(self, ssn):
        query = "SELECT * FROM patient WHERE patient.PatientSSN = %s;"
        self.db_cursor.execute(query, (ssn,))
        patient = self.db_cursor.fetchone()

        if patient:
            patient_info = f"Patient Information:\n"
            patient_info += f"Name: {patient.get('Name', 'N/A')}\n"
            patient_info += f"Age: {self.calculate_age(patient.get('BirthDate', None))}\n"
            patient_info += f"Gender: {patient.get('Sex', 'N/A')}\n"
            patient_info += f"Blood Type: {patient.get('BloodType', 'N/A')}\n"
            patient_info += f"Phone Number: {patient.get('PhoneNumber', 'N/A')}\n"
            patient_info += f"Address: {patient.get('Street', 'N/A')}, {patient.get('City', 'N/A')}, {patient.get('State', 'N/A')}\n"
            return patient_info
        else:
            return "Patient not found."
    

    def display_patient_info(self):
            patient_info = self.get_patient_info()  
            self.patient_info_listbox.delete(0, tk.END)
            for patient in patient_info:
                self.patient_info_listbox.insert(tk.END, patient)

    def show_patient_info_ui(self, ssn):
        self.clear_ui()
        ttk.Label(self, text="Your Informations", font=("Arial", 16)).pack(pady=10)
        patient_info_listbox = tk.Listbox(self)
        patient_info_listbox.pack(pady=10)
        self.display_companion(patient_info_listbox)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

########################################################################################  

    def display_prescriptions(self):
            prescriptions = self.get_prescriptions()  
            self.prescriptions_listbox.delete(0, tk.END)
            for prescription in prescriptions:
                self.prescriptions_listbox.insert(tk.END, prescription)


    def show_prescriptions_ui(self, ssn):
        self.clear_ui()
        ttk.Label(self, text="Prescriptions", font=("Arial", 16)).pack(pady=10)
        prescription_listbox = tk.Listbox(self)
        prescription_listbox.pack(pady=10)
        self.display_companion(prescription_listbox)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)


    def get_prescriptions(self, ssn):
        query = """
        SELECT p.PrescriptionId, p.Diagnosis, pm.Medicine, pm.Dosage
        FROM prescription p
        JOIN prescription_medicine pm ON p.PrescriptionId = pm.PrescriptionId
        WHERE p.PatientSSN = %s;
        """
        self.db_cursor.execute(query, (ssn,))
        prescription_data = self.db_cursor.fetchall()

        if prescription_data:
            prescriptions_info = "Prescriptions:\n"
            for prescription in prescription_data:
                prescriptions_info += f"Prescription ID: {prescription.get('PrescriptionId', 'N/A')}\n"
                prescriptions_info += f"Diagnosis: {prescription.get('Diagnosis', 'N/A')}\n"
                prescriptions_info += f"Medicine: {prescription.get('Medicine', 'N/A')}\n"
                prescriptions_info += f"Dosage: {prescription.get('Dosage', 'N/A')}\n"
                prescriptions_info += "-----------------\n"
            return prescriptions_info
        else:
            return "No prescriptions found for the patient."

######################################################################################## 

    def setup_main_menu(self):
        self.clear_ui()
        ttk.Button(self, text="Make Appointment", command=self.show_make_appointment_ui).pack(pady=10)
        ttk.Button(self, text="See Your Appointments", command=self.show_appointments_ui).pack(pady=10)
        ttk.Button(self, text="See Your Companions", command=self.show_companion_ui).pack(pady=10)
        ttk.Button(self, text="See Your Prescriptions", command=self.show_prescription_ui).pack(pady=10)
        ttk.Button(self, text="See Your Information", command=self.show_patient_info_ui).pack(pady=10)
        


    '''def make_appointment(self):
        selection = self.doctor_combobox.curselection()
        if selection:
            selected_doctor = self.doctor_combobox.get(selection[0])
            appointment = self.appointment_text.get("1.0", tk.END).strip()
            if appointment:
                messagebox.showinfo("Appointment made", f"Appoinment made with  {selected_doctor}.")
                self.appointment_text.delete("1.0", tk.END)
            else:
                messagebox.showerror("Error", "Please make an appointment.")
        else:
            messagebox.showerror("Error", "Please select a doctor.")'''

    """def make_appointment(self):
        selected_doctor = self.selected_doctor_var.get()
        appointment = self.appointment_text.get("1.0", tk.END).strip()

        if selected_doctor:
            messagebox.showinfo("Appointment made", f"Appointment made with {selected_doctor}.")
            self.appointment_text.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Please select a doctor.")"""



    def show_make_appointment_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Make Appointment", font=("Arial", 16)).pack(pady=10)

        self.selected_doctor_var = tk.StringVar()
        ttk.Label(self, text="Select Doctor:").pack()
        self.doctor_combobox = ttk.Combobox(self, textvariable=self.selected_doctor_var, state="readonly")
        self.update_doctor_combobox()
        self.doctor_combobox.pack()
        self.display_doctors(self.doctor_combobox)

        '''self.doctors_listbox = tk.Listbox(self)
        self.doctors_listbox.pack(pady=10)
        self.display_doctors(self.doctors_listbox)'''

        self.appointment_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=40, height=10)

        self.selected_day_var = tk.StringVar()
        ttk.Label(self, text="Select Day:").pack()
        self.day_combobox = ttk.Combobox(self, textvariable=self.selected_day_var, state="readonly")
        self.update_day_combobox()
        self.day_combobox.pack()
        self.display_days(self.day_combobox)

        self.selected_time_var = tk.StringVar()
        ttk.Label(self, text="Select Time:").pack()
        self.time_combobox = ttk.Combobox(self, textvariable=self.selected_time_var, state="readonly")
        self.update_time_combobox()
        self.time_combobox.pack()
        self.display_times(self.time_combobox)
        ttk.Button(self, text="Make Appointment", command=self.make_appointment).pack(pady=10)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)


    def update_doctor_combobox(self):
        query = "SELECT Expertise FROM doctor;"
        self.db_cursor.execute(query)
        doctor_expertise = [row['Expertise'] for row in self.db_cursor.fetchall() if row['Expertise']]
        self.doctor_combobox['values'] = doctor_expertise

    def update_day_combobox(self):
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thusday', 'Friday']
        self.day_combobox['values'] = day_names

    def update_time_combobox(self):
        time_names = ['12:00', '13:00', '15:00',  '16:00']
        self.time_combobox['values'] = time_names


    def display_doctors(self, listbox):
        query = "SELECT Expertise FROM doctor;"
        self.db_cursor.execute(query)
        doctors = [row['Expertise'] for row in self.db_cursor.fetchall() if row['Expertise']]
        listbox.delete(0, tk.END)
        for doctor in doctors:
            listbox.insert(tk.END, doctor)

    def display_days(self, listbox):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thusday', 'Friday']
        listbox.delete(0, tk.END)
        for day in days:
            listbox.insert(tk.END, day)


    def display_times(self, listbox):
        times = ['12:00', '13:00', '15:00', '16:00']
        listbox.delete(0, tk.END)
        for time in times:
            listbox.insert(tk.END, time)

######################################################################################## 
    def show_appointments_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Appointments", font=("Arial", 16)).pack(pady=10)
        appointment_listbox = tk.Listbox(self)
        appointment_listbox.pack(pady=10)
        self.display_appointments(appointment_listbox)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def display_appointments(self, listbox):
        appointments = get_appointments(self)
        #appointments = ["1", "2", "3"]
        listbox.delete(0, tk.END)
        for appointment in appointments:
            listbox.insert(tk.END, appointment)
######################################################################################## 

    def show_companion_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Companions", font=("Arial", 16)).pack(pady=10)
        companion_listbox = tk.Listbox(self)
        companion_listbox.pack(pady=10)
        self.display_companion(companion_listbox)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)


    def display_companions(self, patient_ssn):
        query = """
        SELECT c.Name, c.Relationship, c.PhoneNumber, c.since, c.until
        FROM companion c
        WHERE c.PatientSSN = %s;
        """
        self.db_cursor.execute(query, (patient_ssn,))
        companions = self.db_cursor.fetchall()

        if companions:
            companions_info = "Companions:\n"
            for companion in companions:
                companions_info += f"Name: {companion.get('Name', 'N/A')}\n"
                companions_info += f"Relationship: {companion.get('Relationship', 'N/A')}\n"
                companions_info += f"Phone Number: {companion.get('PhoneNumber', 'N/A')}\n"
                companions_info += f"Since: {companion.get('since', 'N/A')}\n"
                companions_info += f"Until: {companion.get('until', 'N/A')}\n"
                companions_info += "-----------------\n"
            return companions_info
        else:
            return "No companions found for the patient."

######################################################################################## 
    
    def add_appointment_gui(self, selected_doctor, selected_day, selected_time):
        appointment_details = f"Doctor: {selected_doctor}\nDay: {selected_day}\nTime: {selected_time}"
        self.appointments_controller.add_appointment(appointment_details)
        messagebox.showinfo("Appointment added", "Appointment has been successfully added!")

    """def make_appointment(self):
        selected_doctor = self.selected_doctor_var.get()
        appointment_text = self.appointment_text.get("1.0", tk.END).strip()
        selected_day = self.selected_day_var.get()
        selected_time = self.selected_time_var.get()

        if selected_doctor and appointment_text and selected_day and selected_time:
            self.add_appointment_gui(selected_doctor, selected_day, selected_time)
            self.appointment_text.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Please fill in all the appointment details.")"""
    

    def make_appointment(self):
        selected_doctor_index = self.doctor_combobox.current()
        selected_doctor = self.doctor_combobox.get() if selected_doctor_index != -1 else None
        appointment_text = self.appointment_text.get("1.0", tk.END).strip()
        selected_day = self.selected_day_var.get()
        selected_time = self.selected_time_var.get()

        if selected_doctor and appointment_text and selected_day and selected_time:
            self.add_appointment_gui(selected_doctor, selected_day, selected_time)
            self.appointment_text.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Please fill in all the appointment details.")


    def add_appointment(self, appointment):
        self.appointments_list.append(appointment)

    def get_appointments(self):
        return self.appointments_list

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
    
    
    def clear_appointment_tree(self, appointment_tree):
        for item in appointment_tree.get_children():
            appointment_tree.delete(item)