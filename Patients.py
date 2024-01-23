import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from Appointments import AppointmentsFrame, get_appointments

class PatientsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(fill="both", expand=True)
        self.appointments_list = []
        self.appointments_controller = AppointmentsFrame()
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
            messagebox.showerror("Login Failed", "Patient SSN and Password cannot be empty.")
            return

        if self.authenticate_patient(patient_ssn, password):
            messagebox.showinfo("Login Successful", "Welcome!")
            self.clear_login_ui()
            self.setup_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid Patient SSN or password")

    def authenticate_patient(self, ssn, password):
        return True

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


    def display_prescriptions(self):
        prescriptions = self.get_prescriptions()  
        self.prescriptions_listbox.delete(0, tk.END)
        for prescription in prescriptions:
            self.prescriptions_listbox.insert(tk.END, prescription)

    def get_patient_info(self):
        return "Patient Information:\nName: John Doe\nAge: 30\nGender: Male\n"

    def get_prescriptions(self):
        return ["Prescription 1", "Prescription 2", "Prescription 3"]


    def setup_main_menu(self):
        self.clear_ui()
        ttk.Button(self, text="Make Appointment", command=self.show_make_appointment_ui).pack(pady=10)
        ttk.Button(self, text="List Appointments", command=self.show_appointments_ui).pack(pady=10)
        ttk.Button(self, text="List Companions", command=self.show_companion_ui).pack(pady=10)


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

    def make_appointment(self):
        selected_doctor = self.selected_doctor_var.get()
        appointment = self.appointment_text.get("1.0", tk.END).strip()

        if selected_doctor:
            messagebox.showinfo("Appointment made", f"Appointment made with {selected_doctor}.")
            self.appointment_text.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Please select a doctor.")



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
        doctor_names = ['Doctor A', 'Doctor B', 'Doctor C']
        self.doctor_combobox['values'] = doctor_names

    def update_day_combobox(self):
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thusday', 'Friday']
        self.day_combobox['values'] = day_names

    def update_time_combobox(self):
        time_names = ['12:00', '13:00', '15:00',  '16:00']
        self.time_combobox['values'] = time_names


    def display_doctors(self, listbox):
        doctors = ['Doctor A', 'Doctor B', 'Doctor C']
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


    def show_appointments_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Appointments", font=("Arial", 16)).pack(pady=10)
        appointment_listbox = tk.Listbox(self)
        appointment_listbox.pack(pady=10)
        self.display_appointments(appointment_listbox)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)


    def show_companion_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Companions", font=("Arial", 16)).pack(pady=10)
        companion_listbox = tk.Listbox(self)
        companion_listbox.pack(pady=10)
        self.display_companion(companion_listbox)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)


    def display_appointments(self, listbox):
        appointments = get_appointments(self)
        #appointments = ["1", "2", "3"]
        listbox.delete(0, tk.END)
        for appointment in appointments:
            listbox.insert(tk.END, appointment)


    def display_companion(self, listbox):
        companions = ['Companion A', 'Companion B', 'Companion C']
        listbox.delete(0, tk.END)
        for c in companions:
            listbox.insert(tk.END, c)

    
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
