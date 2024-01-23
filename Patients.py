import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector

class PatientsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.appointments_list = [] 
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
        patient_name = self.get_patient_name(patient_ssn)
        if self.authenticate_patient(patient_ssn, password):
            messagebox.showinfo("Login Successful", f"Welcome, {patient_name}!")
            self.clear_login_ui()
            self.setup_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid SSN or password")


    def get_patient_name(self, ssn):
        query = "SELECT p.Name FROM patient p WHERE p.PatientSSN =  %s;"
        self.db_cursor.execute(query, (ssn,))
        result = self.db_cursor.fetchone()
        if result:
            return result[0]
        else:
            return "Unknown"


    def authenticate_patient(self, ssn, password):
        query = "SELECT * FROM patient WHERE patient.PatientSSN = %s;"
        self.db_cursor.execute(query, (ssn,))
        patient = self.db_cursor.fetchone()

        if password == "1234":
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

########################################################
    def get_patient_info(self, ssn):
        query = "SELECT * FROM patient WHERE patient.PatientSSN = %s;"
        self.db_cursor.execute(query, (ssn,))
        patient = self.db_cursor.fetchone()
        #print(patient)
        if patient:
            return {
            "Name": patient[2],    
            "Gender": patient[8],  
            "Blood Type": patient[4],  
            "Phone Number": patient[1],  
            "Address": f"{patient[6]}, {patient[5]}, {patient[7]}"  
            }
        else:
            return {"error": "Patient not found."}

    def display_patient_info(self):
        patient_info = self.get_patient_info(self.patient_ssn_var.get())
        
        if "error" in patient_info:
            self.patient_info_listbox.insert(tk.END, patient_info["error"])
        else:
            self.patient_info_listbox.delete(0, tk.END)
            for key, value in patient_info.items():
                self.patient_info_listbox.insert(tk.END, f"{key}: {value}")

    def show_patient_info_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Your Information", font=("Arial", 16)).pack(pady=10)
        self.patient_info_listbox = tk.Listbox(self)
        self.patient_info_listbox.pack(pady=20)
        self.display_patient_info()
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)


########################################################################################  

    def display_prescriptions(self):
        prescriptions = self.get_prescriptions(self.patient_ssn_var.get())  
        self.prescriptions_listbox.delete(0, tk.END)
        
        if isinstance(prescriptions, list):
            for prescription in prescriptions:
                for key, value in prescription.items():
                    self.prescriptions_listbox.insert(tk.END, f"{key}: {value}")
                self.prescriptions_listbox.insert(tk.END, "-----------------")
        else:
            self.prescriptions_listbox.insert(tk.END, prescriptions)

    def show_prescriptions_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Prescriptions", font=("Arial", 16)).pack(pady=10)
        self.prescriptions_listbox = tk.Listbox(self)
        self.prescriptions_listbox.pack(pady=10)
        self.display_prescriptions()
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def get_prescriptions(self, ssn):
        query = """
        SELECT p.PrescriptionId, p.Diagnosis, pm.Medicine
        FROM prescription p
        JOIN prescription_medicine pm ON p.PrescriptionId = pm.PrescriptionId
        JOIN writes w ON w.PrescriptionId = p.PrescriptionId
        WHERE w.PatientSSN = %s;
        """
        self.db_cursor.execute(query, (ssn,))
        prescription_data = self.db_cursor.fetchall()
        print(prescription_data)
        prescriptions_list = []
        
        if prescription_data:
            for prescription in prescription_data:
                prescription_info = {
                    "Prescription ID": prescription[0],  
                    "Diagnosis": prescription[1],  
                    "Medicine": prescription[2],  
                }
                prescriptions_list.append(prescription_info)
            return prescriptions_list
        else:
            return "No prescriptions found for the patient."


######################################################################################## 
    def setup_main_menu(self):
        self.clear_ui()
        ttk.Button(self, text="Make Appointment", command=self.show_make_appointment_ui).pack(pady=10)
        ttk.Button(self, text="See Your Appointments", command=self.show_appointments_ui).pack(pady=10)
        ttk.Button(self, text="See Your Companions", command=self.show_companion_ui).pack(pady=10)
        ttk.Button(self, text="See Your Prescriptions", command=self.show_prescriptions_ui).pack(pady=10)
        ttk.Button(self, text="See Your Information", command=self.show_patient_info_ui).pack(pady=10)
        
    """def make_appointment(self):
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
            messagebox.showerror("Error", "Please select a doctor.")"""


    def make_appointment(self):
        selection = self.doctor_combobox.curselection()
        if selection:
            selected_doctor = self.doctor_combobox.get(selection[0])
            appointment_text = self.appointment_text.get("1.0", tk.END).strip()
            selected_day = self.selected_day_var.get()
            selected_time = self.selected_time_var.get()

            if not appointment_text or not selected_day or not selected_time:
                messagebox.showerror("Error", "Please provide all the required information.")
                return

            appointment_id = self.insert_appointment(selected_doctor, appointment_text, selected_day, selected_time)

            if appointment_id:
                messagebox.showinfo("Appointment made", f"Appointment made with {selected_doctor}.")
                self.appointments_list.append({
                    "AppointmentID": appointment_id,
                    "Duration": appointment_text,
                    "Date": f"{selected_day} {selected_time}",
                    "Floor": "3",  
                    "RoomNumber": "20"  
                })

               
                self.show_appointments_ui()
            else:
                messagebox.showerror("Error", "Failed to make an appointment. Please try again.")

            self.appointment_text.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Please select a doctor.")













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
        query = "SELECT DISTINCT Expertise FROM doctor;"
        self.db_cursor.execute(query)
        doctor_expertise = [row[0] for row in self.db_cursor.fetchall() if row[0]]
        print(doctor_expertise)
        self.doctor_combobox['values'] = doctor_expertise


    def update_day_combobox(self):
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thusday', 'Friday']
        self.day_combobox['values'] = day_names


    def update_time_combobox(self):
        time_names = ['12:00', '13:00', '15:00',  '16:00']
        self.time_combobox['values'] = time_names


    def display_doctors(self, listbox):
        query = "SELECT DISTINCT Expertise FROM doctor;"
        self.db_cursor.execute(query)
        doctors = [row[0] for row in self.db_cursor.fetchall() if row[0]]
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
        self.display_appointments(self.patient_ssn_var.get())
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)


    def display_appointments(self, ssn):
        appointments = self.get_patient_appointments(ssn)
        self.appointment_listbox.delete(0, tk.END)
        if appointments:
            for key, value in appointments:
                self.appointment_listbox.insert(tk.END, f"{key}: {value}")
            self.companion_listbox.insert(tk.END, "-----------------")
        else:
            self.appointment_listbox.insert(tk.END, "No appointment found for the patient.")


    def get_patient_appointments(self, patient_ssn):
        query = """
        SELECT a.AppointmentID, a.Duration, a.Date, a.Floor, a.RoomNumber
        FROM appointment a
        JOIN participates p ON a.AppointmentID = p.AppointmentID
        WHERE p.PatientSSN = %s;
        """
        self.db_cursor.execute(query, (patient_ssn,))
        appointments_data = self.db_cursor.fetchall()
        appointments_list = []

        for appointment in appointments_data:
            appointment_info = {
                "AppointmentID": appointment[0],
                "Duration": appointment[1],
                "Date": appointment[2],
                "Floor": appointment[3],
                "RoomNumber": appointment[4]
            }
            appointments_list.append(appointment_info)

        return appointments_list



######################################################################################## 

    def get_companions(self, patient_ssn):
        query = """
        SELECT c.Name, c.Relationship, c.PhoneNumber, c.since, c.until
        FROM companion c
        WHERE c.PatientSSN = %s;
        """
        self.db_cursor.execute(query, (patient_ssn,))
        companions_data = self.db_cursor.fetchall()
        companions_list = []

        for companion in companions_data:
            companion_info = {
                "Name": companion[0],  
                "Relationship": companion[1],  
                "Phone Number": companion[2],  
                "Since": companion[3],  
                "Until": companion[4]  
            }
            companions_list.append(companion_info)

        return companions_list

    def display_companions(self, patient_ssn):
        companions = self.get_companions(patient_ssn)
        self.companion_listbox.delete(0, tk.END)

        if companions:
            for companion_info in companions:
                for key, value in companion_info.items():
                    self.companion_listbox.insert(tk.END, f"{key}: {value}")
                self.companion_listbox.insert(tk.END, "-----------------")
        else:
            self.companion_listbox.insert(tk.END, "No companions found for the patient.")

    def show_companion_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Companions", font=("Arial", 16)).pack(pady=10)
        self.companion_listbox = tk.Listbox(self)
        self.companion_listbox.pack(pady=10)
        self.display_companions(self.patient_ssn_var.get())
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)