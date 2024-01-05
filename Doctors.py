import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext



class DoctorsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
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
        self.patient_filter_entry.bind("<Return>", self.filter_patients)
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
        self.update_patient_combobox()

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
        patient_listbox = tk.Listbox(self)
        patient_listbox.pack(pady=10)
        self.display_patients(patient_listbox)
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
        self.patient_listbox = tk.Listbox(self)
        self.patient_listbox.pack(pady=10)
        self.patient_listbox.bind('<<ListboxSelect>>', self.on_patient_selected)
        self.display_patients(self.patient_listbox)
        ttk.Label(self, text="Prescription:").pack()
        self.prescription_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=10)
        self.prescription_text.pack(pady=10)
        ttk.Button(self, text="Issue Prescription", command=self.issue_prescription).pack(pady=10)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def on_patient_selected(self, event):
        selection = self.patient_listbox.curselection()
        if selection:
            index = selection[0]
            selected_patient = self.patient_listbox.get(index)
            self.selected_patient_var.set(selected_patient)

    def filter_patients(self, event):
        filter_text = self.patient_filter_var.get()
        self.display_patients()

    def update_patient_combobox(self):
        patients = ['Patient A', 'Patient B', 'Patient C']
        self.selected_patient_combobox['values'] = patients

    def issue_prescription(self):
        selection = self.patient_listbox.curselection()
        if selection:
            selected_patient = self.patient_listbox.get(selection[0])
            prescription = self.prescription_text.get("1.0", tk.END).strip()
            if prescription:
                messagebox.showinfo("Prescription Issued", f"Prescription issued to {selected_patient}.")
                self.prescription_text.delete("1.0", tk.END)
            else:
                messagebox.showerror("Error", "Please write a prescription.")
        else:
            messagebox.showerror("Error", "Please select a patient.")

    def clear_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

    def display_patients(self, listbox):
        patients = ['Patient A', 'Patient B', 'Patient C']
        listbox.delete(0, tk.END)
        for patient in patients:
            listbox.insert(tk.END, patient)

    def display_appointments(self, listbox):
        #appointments = get_appointments()
        appointments = ["1", "2", "3"]
        listbox.delete(0, tk.END)
        for appointment in appointments:
            listbox.insert(tk.END, appointment)