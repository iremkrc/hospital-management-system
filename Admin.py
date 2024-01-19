import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector


class AdminFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="write your own password",
        auth_plugin='mysql_native_password'
        )
        print(self.db_connection)
        self.db_cursor = self.db_connection.cursor(buffered=True)
        self.db_cursor.execute("USE comp306project")

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
        return True 
    
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
        self.display_patients(patient_tree)

        ttk.Button(self, text="Add Patient", command=self.add_patient_ui).pack(pady=10)

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

    def show_doctors_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Doctors", font=("Arial", 16)).pack(pady=10)
        columns = ("EmployeeId", "EmployeeSSN", "Name", "Sex", "BirthDate", "Salary", "HireDate", "City", "Street", "State", "Title", "Expertise", "Bonus")
        doctors_tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            doctors_tree.heading(col, text=col)
            doctors_tree.column(col, width=95)
        self.display_doctors(doctors_tree)
        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

    def show_nurses_ui(self):
        self.clear_ui()
        ttk.Label(self, text="Nurses", font=("Arial", 16)).pack(pady=10)
        columns = ("EmployeeId", "EmployeeSSN", "Name", "Sex", "BirthDate", "Salary", "HireDate", "City", "Street", "State")
        nurses_tree = ttk.Treeview(self, columns=columns, show='headings')

        for col in columns:
            nurses_tree.heading(col, text=col)
            nurses_tree.column(col, width=95)
        self.display_nurses(nurses_tree)

        ttk.Button(self, text="Back", command=self.setup_main_menu).pack(pady=10)

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

        # Creating a frame for the Treeview and Scrollbar
        frame = ttk.Frame(self)
        frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Creating the Treeview widget
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adding a horizontal scrollbar
        h_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        tree.configure(xscrollcommand=h_scroll.set)

        # Defining the columns
        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, anchor=tk.CENTER, width=100)

        # Inserting the rows
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

        # Creating a frame for the Treeview and Scrollbar
        frame = ttk.Frame(self)
        frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Creating the Treeview widget
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adding a horizontal scrollbar
        h_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        tree.configure(xscrollcommand=h_scroll.set)

        # Defining the columns
        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, anchor=tk.CENTER, width=100)

        # Inserting the rows
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

        # Creating a frame for the Treeview and Scrollbar
        frame = ttk.Frame(self)
        frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Creating the Treeview widget
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adding a horizontal scrollbar
        h_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        tree.configure(xscrollcommand=h_scroll.set)

        # Defining the columns
        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, anchor=tk.CENTER, width=100)

        # Inserting the rows
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

        # Creating a frame for the Treeview and Scrollbar
        frame = ttk.Frame(self)
        frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Creating the Treeview widget
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adding a horizontal scrollbar
        h_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        tree.configure(xscrollcommand=h_scroll.set)

        # Defining the columns
        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, anchor=tk.CENTER, width=100)

        # Inserting the rows
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
            doctor_tree.insert("", 'end', values=(doctor[0], doctor[1], doctor[2], doctor[3], doctor[4], doctor[5], doctor[6], doctor[7], doctor[8], doctor[10], doctor[11], doctor[12], doctor[13]))
        doctor_tree.pack(pady=10)


    def display_nurses(self, nurse_tree):
        query = "select * from employee, nurse where nurse.employeeId = employee.employeeId;"
        self.db_cursor.execute(query)
        nurses = self.db_cursor.fetchall()
        for nurse in nurses:
            nurse_tree.insert("", 'end', values=(nurse[0], nurse[1], nurse[2], nurse[3], nurse[4], nurse[5], nurse[6], nurse[7], nurse[8], nurse[9]))
        nurse_tree.pack(pady=10)

    def execute_sql(self):
        # Clear the listbox
        self.sql_listbox.delete(0, tk.END)
        sql = self.sql_text.get("1.0", tk.END)
        try:
            self.db_cursor.execute(sql)
            results = self.db_cursor.fetchall()
            print(results)
            for name in results:
                self.sql_listbox.insert(tk.END, name)
        except Exception as e:
            print(e)