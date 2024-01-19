import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector



class DoctorsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.patient_tree = None 
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
        return True 
    
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
        ttk.Button(self, text="List Patients", command=self.show_patients_ui).pack(pady=10)
        ttk.Button(self, text="List Appointments", command=self.show_appointments_ui).pack(pady=10)
        ttk.Button(self, text="Issue Prescription", command=self.show_prescription_ui).pack(pady=10)

    def show_patients_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Patients", font=("Arial", 16)).pack(pady=10)
        
        columns = ("PatientSSN", "PhoneNumber", "Name", "BirthDate", "BloodType", "City", "Street", "State", "Sex")
        patient_tree = ttk.Treeview(self, columns=columns, show='headings')

        for col in columns:
            patient_tree.heading(col, text=col)
            patient_tree.column(col, width=95)
        self.display_patients(patient_tree)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def show_appointments_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Appointments", font=("Arial", 16)).pack(pady=10)
        appointment_listbox = tk.Listbox(self)
        appointment_listbox.pack(pady=10)
        self.display_appointments(appointment_listbox)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def show_prescription_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Select Patient for Prescription", font=("Arial", 16)).pack(pady=10)

        # Using Treeview instead of Listbox
        columns = ("PatientSSN", "PhoneNumber", "Name", "BirthDate", "BloodType", "City", "Street", "State", "Sex")
        self.patient_tree = ttk.Treeview(self, columns=columns, show='headings')

        for col in columns:
            self.patient_tree.heading(col, text=col)
            self.patient_tree.column(col, width=95)
        
        # Display patients in the Treeview
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
                patient_ssn = selected_patient[0]  # Assuming the SSN is the first item in the list
                messagebox.showinfo("Prescription Issued", f"Prescription {prescription} issued to Patient {patient_ssn}.")
                self.prescription_text.delete("1.0", tk.END)
            else:
                messagebox.showerror("Error", "Please write a prescription.")
        else:
            messagebox.showerror("Error", "Please select a patient.")

    def clear_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

    def display_patients(self, patient_tree):
        query = "SELECT * FROM patient"
        self.db_cursor.execute(query)
        patients = self.db_cursor.fetchall()
        for patient in patients:
            patient_tree.insert("", 'end', values=(patient[0], patient[1], patient[2], patient[3], patient[4], patient[5], patient[6], patient[7], patient[8]))
        
        patient_tree.pack(pady=10)
    

    def display_appointments(self, listbox):
        #appointments = get_appointments()
        appointments = ["1", "2", "3"]
        listbox.delete(0, tk.END)
        for appointment in appointments:
            listbox.insert(tk.END, appointment)