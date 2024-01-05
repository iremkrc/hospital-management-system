import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ScrollableFrameUtil import ScrollableFrame


class NursesFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
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
        self.update_patient_combobox()

    def authenticate_nurse(self, ssn, password):
        return True

    def display_patients(self, listbox):
        patients = ['Patient A', 'Patient B', 'Patient C']
        listbox.delete(0, tk.END)
        for patient in patients:
            listbox.insert(tk.END, patient)

    def filter_patients(self, event):
        filter_text = self.patient_filter_var.get()
        self.display_patients()

    def display_appointments(self, listbox):
        # appointments = get_appointments()
        appointments = ["1", "2", "3"]
        listbox.delete(0, tk.END)
        for appointment in appointments:
            listbox.insert(tk.END, appointment)

    def clear_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

    def clear_login_ui(self):
        for widget in self.winfo_children():
            widget.destroy()

    def setup_main_menu(self):
        self.clear_ui()
        ttk.Button(self, text="List Patients", command=self.show_patients_ui).pack(pady=10)
        ttk.Button(self, text="List Appointments", command=self.show_appointments_ui).pack(pady=10)
        ttk.Button(self, text="Refer Nurses", command=self.show_refer_nurses_ui).pack(pady=10)

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

    def show_refer_nurses_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Refer a Nurse", font=("Arial", 16)).pack(pady=10)
        self.nurses_listbox = tk.Listbox(self)
        self.nurses_listbox.pack(pady=10)
        self.display_nurses()
        self.selected_nurse_var = tk.StringVar()
        ttk.Label(self, text="Select Nurse:").pack()
        self.nurses_combobox = ttk.Combobox(self, textvariable=self.selected_nurse_var, state="readonly")
        self.update_nurse_combobox()
        self.nurses_combobox.pack()
        ttk.Label(self, text="Reference Points:").pack()
        self.reference_point = tk.StringVar()
        ttk.Entry(self, textvariable=self.reference_point).pack()
        ttk.Button(self, text="Give Reference", command=self.give_reference).pack(pady=10)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def display_nurses(self):
        nurse_names = ['Nurse A', 'Nurse B', 'Nurse C']
        for name in nurse_names:
            self.nurses_listbox.insert(tk.END, name)

    def update_nurse_combobox(self):
        nurse_names = ['Nurse A', 'Nurse B', 'Nurse C']
        self.nurses_combobox['values'] = nurse_names

    def give_reference(self):
        selected_nurse = self.selected_nurse_var.get()
        points = self.reference_point.get()
        if selected_nurse and points:
            messagebox.showinfo("Reference Given", f"Reference given to {selected_nurse} with {points} points.")
        else:
            messagebox.showerror("Error", "Please select a nurse and enter reference points.")