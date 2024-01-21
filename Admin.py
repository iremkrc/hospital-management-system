import random
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector


class AdminFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="24632463",
        auth_plugin='mysql_native_password'
        )
        self.db_cursor = self.db_connection.cursor(buffered=True)
        self.db_cursor.execute("USE comp306project")
        self.selected_doctor_info = None
        self.selected_nurse_info = None
        self.selected_patient_info = None
        
        self.pack(fill="both", expand=True)
        self.selected_patient_var = tk.StringVar()
        self.setup_login_ui()

    def setup_login_ui(self):
        self.login_label = ttk.Label(self, text="Admin Login", font=("Arial", 18))
        self.login_label.pack(pady=10)
        self.admin_id_var = tk.StringVar()
        self.admin_password_var = tk.StringVar()
        ttk.Label(self, text="admin ID:").pack()
        ttk.Entry(self, textvariable=self.admin_id_var).pack()
        ttk.Label(self, text="Password:").pack()
        ttk.Entry(self, textvariable=self.admin_password_var, show="*").pack()
        ttk.Button(self, text="Login", command=self.admin_login).pack(pady=10)

    def admin_login(self):
        admin_id = self.admin_id_var.get()
        password = self.admin_password_var.get()

        if not admin_id or not password:
            messagebox.showerror("Login Failed", "admin ID and Password cannot be empty.")
            return

        if self.authenticate_admin(admin_id, password):
            messagebox.showinfo("Login Successful", "Welcome!")
            self.clear_login_ui()
            self.setup_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid admin ID or password")

    def authenticate_admin(self, admin_id, password):
        if admin_id == "admin" and password == "admin":
            return True
        return False 
    
    def load_admin_functions(self):
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
        ttk.Button(self, text="List Doctors", command=self.show_doctors_ui).pack(pady=10)
        ttk.Button(self, text="List Nurses", command=self.show_nurses_ui).pack(pady=10)
        ttk.Button(self, text="Enter SQL Query", command=self.show_sql_ui).pack(pady=10)
        ttk.Button(self, text="Others", command=self.show_queries_ui).pack(pady=10)

    """
    def show_patients_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Patients", font=("Arial", 16)).pack(pady=10)
        patient_listbox = tk.Listbox(self)
        patient_listbox.pack(pady=10)
        self.display_patients(patient_listbox)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)
    """

    def show_patients_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Patients", font=("Arial", 16)).pack(pady=10)

        columns = ("PatientSSN", "PhoneNumber", "Name", "BirthDate", "BloodType", "City", "Street", "State", "Sex")
        patient_tree = ttk.Treeview(self, columns=columns, show='headings')

        for col in columns:
            patient_tree.heading(col, text=col)
            patient_tree.column(col, width=95)

        def on_patient_selected(event):
            selected_item = patient_tree.selection()[0]
            self.selected_patient_info = patient_tree.item(selected_item)['values']
        
        patient_tree.bind("<<TreeviewSelect>>", on_patient_selected)
        self.display_patients(patient_tree)

        ttk.Button(self, text="Add Patient", command=self.add_patient_ui).pack(pady=10)
        ttk.Button(self, text="Delete Patient", command=self.delete_patient_query).pack(pady=10)

        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def add_patient_ui(self):
        self.clear_ui()

        ttk.Label(self, text="Patient SSN (Numeric)").pack(pady=2)
        patient_ssn_var = tk.StringVar()
        ttk.Entry(self, textvariable=patient_ssn_var).pack(pady=2)

        ttk.Label(self, text="Phone Number").pack(pady=2)
        phone_number_var = tk.StringVar()
        ttk.Entry(self, textvariable=phone_number_var).pack(pady=2)

        ttk.Label(self, text="Name").pack(pady=2)
        name_var = tk.StringVar()
        ttk.Entry(self, textvariable=name_var).pack(pady=2)

        ttk.Label(self, text="Birth Date (YYYY-MM-DD)").pack(pady=2)
        birth_date_var = tk.StringVar()
        ttk.Entry(self, textvariable=birth_date_var).pack(pady=2)

        ttk.Label(self, text="Blood Type (e.g., A+, O-)").pack(pady=2)
        blood_type_var = tk.StringVar()
        ttk.Entry(self, textvariable=blood_type_var).pack(pady=2)

        ttk.Label(self, text="City").pack(pady=2)
        city_var = tk.StringVar()
        ttk.Entry(self, textvariable=city_var).pack(pady=2)

        ttk.Label(self, text="Street").pack(pady=2)
        street_var = tk.StringVar()
        ttk.Entry(self, textvariable=street_var).pack(pady=2)

        ttk.Label(self, text="State").pack(pady=2)
        state_var = tk.StringVar()
        ttk.Entry(self, textvariable=state_var).pack(pady=2)

        ttk.Label(self, text="Sex (M/F)").pack(pady=2)
        sex_var = tk.StringVar()
        ttk.Entry(self, textvariable=sex_var).pack(pady=2)

        ttk.Button(self, text="Submit", command=lambda: self.submit_patient_info(
            patient_ssn_var.get(), phone_number_var.get(), name_var.get(),
            birth_date_var.get(), blood_type_var.get(), city_var.get(), street_var.get(),
            state_var.get(), sex_var.get())).pack(pady=10)

        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def submit_patient_info(self, patient_ssn_var, phone_number_var, name_var,
                            birth_date_var, blood_type_var, city_var, street_var,
                            state_var, sex_var):

        query = """
        INSERT INTO patient (PatientSSN, PhoneNumber, Name, BirthDate, BloodType, City, Street, State, Sex) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = (patient_ssn_var, phone_number_var, name_var,
                birth_date_var, blood_type_var, city_var, street_var,
                state_var, sex_var)

        try:
            self.db_cursor.execute(query, data)
            self.db_connection.commit()
            tk.messagebox.showinfo("Success", "Patient added to the system")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")
            print(e)

        self.show_patients_ui()

    def delete_patient_query(self):
        patient_ssn = self.selected_patient_info[0]
        delete_part = "DELETE FROM participates where PatientSSN = " + str(patient_ssn)
        delete_patient = "DELETE FROM patient where PatientSSN = " + str(patient_ssn)
        try:
            self.db_cursor.execute(delete_part)
            self.db_cursor.execute(delete_patient)
            self.db_connection.commit()
            tk.messagebox.showinfo("Success", "Patient deleted")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")
            print(e)

        self.show_patients_ui()

    def show_doctors_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Doctors", font=("Arial", 16)).pack(pady=10)
        columns = ("EmployeeId", "EmployeeSSN", "Name", "Sex", "BirthDate", "Salary", "HireDate", "City", "Street", "State", "Title", "Expertise", "Bonus")
        doctors_tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            doctors_tree.heading(col, text=col)
            doctors_tree.column(col, width=95)

        def on_doctor_selected(event):
            selected_item = doctors_tree.selection()[0]
            self.selected_doctor_info = doctors_tree.item(selected_item)['values']

        doctors_tree.bind("<<TreeviewSelect>>", on_doctor_selected)
        self.display_doctors(doctors_tree)

        ttk.Button(self, text="Add Doctor", command=self.add_doctor_ui).pack(pady=10)
        ttk.Button(self, text="Delete Doctor", command=self.delete_doctor_query).pack(pady=10)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def add_doctor_ui(self):
        self.clear_ui()

        row = 0
        col = 0

        ttk.Label(self, text="Employee SSN (Numeric)").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        employee_ssn_var = tk.StringVar()
        ttk.Entry(self, textvariable=employee_ssn_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="Name").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        name_var = tk.StringVar()
        ttk.Entry(self, textvariable=name_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="Sex (M/F)").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        sex_var = tk.StringVar()
        ttk.Entry(self, textvariable=sex_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="Birth Date (YYYY-MM-DD)").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        birth_date_var = tk.StringVar()
        ttk.Entry(self, textvariable=birth_date_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="Salary (Real)").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        salary_var = tk.StringVar()
        ttk.Entry(self, textvariable=salary_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="Hire Date (YYYY-MM-DD)").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        hire_date_var = tk.StringVar()
        ttk.Entry(self, textvariable=hire_date_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="City").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        city_var = tk.StringVar()
        ttk.Entry(self, textvariable=city_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="Street").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        street_var = tk.StringVar()
        ttk.Entry(self, textvariable=street_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="State").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        state_var = tk.StringVar()
        ttk.Entry(self, textvariable=state_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="Title").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        title_var = tk.StringVar()
        ttk.Entry(self, textvariable=title_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="Expertise").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        expertise_var = tk.StringVar()
        ttk.Entry(self, textvariable=expertise_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="Bonus").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        bonus_var = tk.StringVar()
        ttk.Entry(self, textvariable=bonus_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Button(self, text="Submit", command=lambda: self.submit_doctor_info(
            employee_ssn_var.get(), name_var.get(), sex_var.get(),
            birth_date_var.get(), salary_var.get(), hire_date_var.get(), city_var.get(),
            street_var.get(), state_var.get(), title_var.get(), expertise_var.get(), bonus_var.get())
                   ).grid(row=row, column=col, padx=5, pady=10, columnspan=2)

        row += 1

        ttk.Button(self, text="Back", command=self.setup_main_menu).grid(row=row, column=col, padx=5, pady=10,
                                                                         columnspan=2)

    def submit_doctor_info(self, employee_ssn_var, name_var, sex_var,
                            birth_date_var, salary_var, hire_date_var, city_var,
                            street_var, state_var, title_var, expertise_var, bonus_var):

        query_1 = """
        INSERT INTO employee (EmployeeId, EmployeeSSN, Name, Sex, BirthDate, Salary, HireDate, City, Street, State) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        query_2 = """
        INSERT INTO doctor (EmployeeId, Title, Expertise, Bonus)
        VALUES (%s, %s, %s, %s)
        """
        employeeId = random.randint(10**7, 10**8)
        data_1 = (employeeId, employee_ssn_var, name_var,
                sex_var, birth_date_var, salary_var, hire_date_var,
                city_var, street_var, state_var)
        data_2 = (employeeId, title_var, expertise_var, bonus_var)

        try:
            self.db_cursor.execute(query_1, data_1)
            self.db_cursor.execute(query_2, data_2)
            self.db_connection.commit()
            tk.messagebox.showinfo("Success", "Doctor added to the system")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")
            print(e)

        self.show_doctors_ui()

    def delete_doctor_query(self):
        employee_id = self.selected_doctor_info[0]
        delete_part = "DELETE FROM participates where EmployeeId = " + str(employee_id)
        delete_writes = "DELETE FROM writes where DoctorId = " + str(employee_id)
        delete_doctor = "DELETE FROM doctor where EmployeeId = " + str(employee_id)
        delete_emp = "DELETE FROM employee where EmployeeId = " + str(employee_id)
        try:
            self.db_cursor.execute(delete_part)
            self.db_cursor.execute(delete_writes)
            self.db_cursor.execute(delete_doctor)
            self.db_cursor.execute(delete_emp)
            self.db_connection.commit()
            tk.messagebox.showinfo("Success", "Doctor deleted")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")
            print(e)

        self.show_doctors_ui()

    def show_nurses_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Nurses", font=("Arial", 16)).pack(pady=10)

        columns = (
        "EmployeeId", "EmployeeSSN", "Name", "Sex", "BirthDate", "Salary", "HireDate", "City", "Street", "State")
        nurses_tree = ttk.Treeview(self, columns=columns, show='headings')

        for col in columns:
            nurses_tree.heading(col, text=col)
            nurses_tree.column(col, width=95)

        def on_nurse_selected(event):
            selected_item = nurses_tree.selection()[0]
            self.selected_nurse_info = nurses_tree.item(selected_item)['values']

        nurses_tree.bind("<<TreeviewSelect>>", on_nurse_selected)
        self.display_nurses(nurses_tree)
        ttk.Button(self, text="Add Nurse", command=self.add_nurse_ui).pack(pady=10)
        ttk.Button(self, text="Add Certificate", command=self.add_certificate_ui).pack(pady=10)
        ttk.Button(self, text="Delete Nurse", command=self.delete_nurse_query).pack(pady=10)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def add_certificate_ui(self):
        self.clear_ui()

        ttk.Label(self, text="Certificate").pack()
        certificate_var = tk.StringVar()
        certificate_entry = ttk.Entry(self, textvariable=certificate_var)
        certificate_entry.pack()

        ttk.Button(self, text="Add Certificate",
                   command=lambda: self.add_certificate_query(certificate_var.get())).pack()
        ttk.Button(self, text="Back", command=self.show_nurses_ui).pack()

    def add_certificate_query(self, certificate_var):
        employee_id = self.selected_nurse_info[0]
        query = """
        INSERT INTO nurse_certificates (EmployeeId, Certificate) 
        VALUES (%s, %s)
        """
        data = (employee_id, certificate_var)
        try:
            self.db_cursor.execute(query, data)
            self.db_connection.commit()
            tk.messagebox.showinfo("Success", "Certification is added.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")
            print(e)

        self.show_nurses_ui()

    def delete_nurse_query(self):
        employee_id = self.selected_nurse_info[0]
        delete_cert = "DELETE FROM nurse_certificates where EmployeeId = " + str(employee_id)
        delete_ref = "DELETE FROM nurse_references where RefereeNurseId = " + str(employee_id)
        delete_ref2 = "DELETE FROM nurse_references where RefererNurseId = " + str(employee_id)
        delete_nurse = "DELETE FROM nurse where EmployeeId = " + str(employee_id)
        delete_emp = "DELETE FROM employee where EmployeeId = " + str(employee_id)
        try:
            self.db_cursor.execute(delete_cert)
            self.db_cursor.execute(delete_ref)
            self.db_cursor.execute(delete_ref2)
            self.db_cursor.execute(delete_nurse)
            self.db_cursor.execute(delete_emp)
            self.db_connection.commit()
            tk.messagebox.showinfo("Success", "Nurse deleted")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")
            print(e)

        self.show_nurses_ui()

    def add_nurse_ui(self):
        self.clear_ui()

        row = 0
        col = 0

        ttk.Label(self, text="Employee SSN (Numeric)").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        employee_ssn_var = tk.StringVar()
        ttk.Entry(self, textvariable=employee_ssn_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="Name").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        name_var = tk.StringVar()
        ttk.Entry(self, textvariable=name_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="Sex (M/F)").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        sex_var = tk.StringVar()
        ttk.Entry(self, textvariable=sex_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="Birth Date (YYYY-MM-DD)").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        birth_date_var = tk.StringVar()
        ttk.Entry(self, textvariable=birth_date_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="Salary (Real)").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        salary_var = tk.StringVar()
        ttk.Entry(self, textvariable=salary_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="Hire Date (YYYY-MM-DD)").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        hire_date_var = tk.StringVar()
        ttk.Entry(self, textvariable=hire_date_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="City").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        city_var = tk.StringVar()
        ttk.Entry(self, textvariable=city_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="Street").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        street_var = tk.StringVar()
        ttk.Entry(self, textvariable=street_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Label(self, text="State").grid(row=row, column=col, padx=5, pady=5, sticky='w')
        state_var = tk.StringVar()
        ttk.Entry(self, textvariable=state_var).grid(row=row, column=col + 1, padx=5, pady=5)
        row += 1

        ttk.Button(self, text="Submit", command=lambda: self.submit_nurse_info(
            employee_ssn_var.get(), name_var.get(), sex_var.get(),
            birth_date_var.get(), salary_var.get(), hire_date_var.get(), city_var.get(),
            street_var.get(), state_var.get())).grid(row=row, column=col, padx=5, pady=10, columnspan=2)

        row += 1

        ttk.Button(self, text="Back", command=self.setup_main_menu).grid(row=row, column=col, padx=5, pady=10,
                                                                         columnspan=2)

    def submit_nurse_info(self, employee_ssn_var, name_var, sex_var,
                            birth_date_var, salary_var, hire_date_var, city_var,
                            street_var, state_var):

        query_1 = """
        INSERT INTO employee (EmployeeId, EmployeeSSN, Name, Sex, BirthDate, Salary, HireDate, City, Street, State) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        query_2 = """
        INSERT INTO nurse (EmployeeId)
        VALUES (%s)
        """
        employeeId = random.randint(10**7, 10**8)
        data_1 = (employeeId, employee_ssn_var, name_var,
                sex_var, birth_date_var, salary_var, hire_date_var,
                city_var, street_var, state_var)
        data_2 = (employeeId, )

        try:
            self.db_cursor.execute(query_1, data_1)
            self.db_cursor.execute(query_2, data_2)
            self.db_connection.commit()
            tk.messagebox.showinfo("Success", "Nurse added to the system")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")
            print(e)

        self.show_nurses_ui()


    def show_sql_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Enter an SQL query:", font=("Arial", 16)).pack(pady=10)
        self.sql_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=5)
        self.sql_text.pack(pady=10)
        ttk.Button(self, text="Execute", command=self.execute_sql).pack(pady=10)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)
        ttk.Label(self, text="Result:", font=("Arial", 16)).pack(pady=10)
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sql_listbox = tk.Listbox(self, yscrollcommand=scrollbar.set)
        self.sql_listbox.pack(pady=10)

    def show_query_1_ui(self):
        self.clear_ui()
        query = """        
        SELECT e.EmployeeId, e.State, e.Salary, e.Name, TopNurses.averageRating, experiencedNurses.numberOfCertificate
        FROM EMPLOYEE e
        JOIN (
            SELECT RefereeNurseId, AVG(Rating) as averageRating
            FROM NURSE_REFERENCES
            GROUP BY RefereeNurseId
            having averageRating >= 5
        ) AS TopNurses ON e.EmployeeId = TopNurses.RefereeNurseId
        JOIN NURSE n ON e.EmployeeId = n.EmployeeId
        JOIN (
            select n2.EmployeeId, COUNT(*) as numberOfCertificate
            from NURSE n2, nurse_certificates nc
            where n2.EmployeeId = nc.EmployeeId
            group by n2.EmployeeId
            having count(*) >= 2
        ) AS experiencedNurses on e.EmployeeId = experiencedNurses.EmployeeId
        WHERE (e.State = "Ohio")
        ORDER BY TopNurses.averageRating DESC;
        """
        self.db_cursor.execute(query)
        columns = [description[0] for description in self.db_cursor.description]
        result = self.db_cursor.fetchall()

        ttk.Label(self, text="Query 1 Result", font=("Arial", 16)).pack(pady=10)

        frame = ttk.Frame(self)
        frame.pack(pady=10, fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(frame, columns=columns, show='headings')
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        h_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        tree.configure(xscrollcommand=h_scroll.set)

        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, anchor=tk.CENTER, width=100)

        for row in result:
            tree.insert('', tk.END, values=row)

        ttk.Button(self, text="Back", command=self.show_queries_ui).pack(pady=10)

    def show_query_2_ui(self):
        self.clear_ui()
        query = "select * from doctor where doctor.employeeid > 900000;"
        self.db_cursor.execute(query)
        columns = [description[0] for description in self.db_cursor.description]
        result = self.db_cursor.fetchall()

        ttk.Label(self, text="Query 2 Result", font=("Arial", 16)).pack(pady=10)

        frame = ttk.Frame(self)
        frame.pack(pady=10, fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(frame, columns=columns, show='headings')
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        h_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        tree.configure(xscrollcommand=h_scroll.set)

        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, anchor=tk.CENTER, width=100)

        for row in result:
            tree.insert('', tk.END, values=row)

        ttk.Button(self, text="Back", command=self.show_queries_ui).pack(pady=10)

    def show_query_3_ui(self):
        self.clear_ui()
        query = "select * from doctor where doctor.employeeid > 900000;"
        self.db_cursor.execute(query)
        columns = [description[0] for description in self.db_cursor.description]
        result = self.db_cursor.fetchall()

        ttk.Label(self, text="Query 3 Result", font=("Arial", 16)).pack(pady=10)

        frame = ttk.Frame(self)
        frame.pack(pady=10, fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(frame, columns=columns, show='headings')
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        h_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        tree.configure(xscrollcommand=h_scroll.set)

        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, anchor=tk.CENTER, width=100)

        for row in result:
            tree.insert('', tk.END, values=row)

        ttk.Button(self, text="Back", command=self.show_queries_ui).pack(pady=10)

    def show_query_4_ui(self):
        self.clear_ui()
        query = "select * from doctor where doctor.employeeid > 900000;"
        self.db_cursor.execute(query)
        columns = [description[0] for description in self.db_cursor.description]
        result = self.db_cursor.fetchall()

        ttk.Label(self, text="Query 4 Result", font=("Arial", 16)).pack(pady=10)

        frame = ttk.Frame(self)
        frame.pack(pady=10, fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(frame, columns=columns, show='headings')
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        h_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        tree.configure(xscrollcommand=h_scroll.set)

        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, anchor=tk.CENTER, width=100)

        for row in result:
            tree.insert('', tk.END, values=row)

        ttk.Button(self, text="Back", command=self.show_queries_ui).pack(pady=10)

    def show_query_5_ui(self):
        self.clear_ui()
        query = "select * from doctor where doctor.employeeid > 900000;"
        self.db_cursor.execute(query)
        columns = [description[0] for description in self.db_cursor.description]
        result = self.db_cursor.fetchall()
        ttk.Label(self, text="Query 5 Result", font=("Arial", 16)).pack(pady=10)
        tree = ttk.Treeview(self, columns=columns, show='headings')
        tree.pack(pady=10, fill=tk.BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, anchor=tk.CENTER)

        for row in result:
            tree.insert('', tk.END, values=row)

        ttk.Button(self, text="Back", command=self.show_queries_ui).pack(pady=10)

    def show_queries_ui(self):
        self.clear_ui()
        ttk.Button(self, text="Query1", command=self.show_query_1_ui).pack(pady=10)
        ttk.Button(self, text="Query2", command=self.show_query_2_ui).pack(pady=10)
        ttk.Button(self, text="Query3", command=self.show_query_3_ui).pack(pady=10)
        ttk.Button(self, text="Query4", command=self.show_query_4_ui).pack(pady=10)
        ttk.Button(self, text="Query5", command=self.show_query_5_ui).pack(pady=10)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    # def on_patient_selected(self, event):
    #     selection = self.patient_listbox.curselection()
    #     if selection:
    #         index = selection[0]
    #         selected_patient = self.patient_listbox.get(index)
    #         self.selected_patient_var.set(selected_patient)

    def filter_patients(self, event):
        filter_text = self.patient_filter_var.get()
        self.display_patients()

    def update_patient_combobox(self):
        patients = ['Patient A', 'Patient B', 'Patient C']
        self.selected_patient_combobox['values'] = patients

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

    def display_doctors(self, doctor_tree):
        query = "select * from employee, doctor where doctor.employeeId = employee.employeeId;"
        self.db_cursor.execute(query)
        doctors = self.db_cursor.fetchall()
        for doctor in doctors:
            doctor_tree.insert("", 'end', values=(doctor[0], doctor[1], doctor[2], doctor[3], doctor[4], doctor[5], doctor[6], doctor[7], doctor[8], doctor[9], doctor[11], doctor[12], doctor[13]))
        doctor_tree.pack(pady=10)


    def display_nurses(self, nurse_tree):
        query = "select * from employee, nurse where nurse.employeeId = employee.employeeId;"
        self.db_cursor.execute(query)
        nurses = self.db_cursor.fetchall()
        for nurse in nurses:
            nurse_tree.insert("", 'end', values=(nurse[0], nurse[1], nurse[2], nurse[3], nurse[4], nurse[5], nurse[6], nurse[7], nurse[8], nurse[9]))
        nurse_tree.pack(pady=10)

    def execute_sql(self):
        self.sql_listbox.delete(0, tk.END)
        sql = self.sql_text.get("1.0", tk.END)
        try:
            self.db_cursor.execute(sql)
            results = self.db_cursor.fetchall()
            for name in results:
                self.sql_listbox.insert(tk.END, name)
        except Exception as e:
            print(e)