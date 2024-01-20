"""
Replace your function with one of the following functions. 
"""

def authenticate_nurse(self, nurse_id, password):
    query = "SELECT * FROM nurse WHERE nurse.employeeId = %s;"
    self.db_cursor.execute(query, (nurse_id,))
    nurse = self.db_cursor.fetchone()

    if nurse and password == "1234567890":
        self.nurse_id = nurse_id
        return True
    else:
        return False
    
def authenticate_doctor(self, doctor_id, password):
    query = "SELECT * FROM doctor WHERE doctor.employeeId = %s;"
    self.db_cursor.execute(query, (doctor_id,))
    doctor = self.db_cursor.fetchone()

    if doctor and password == "1234567890":
        self.doctor_id = doctor_id
        return True
    else:
        return False
    
def authenticate_admin(self, admin_id, password):
    if admin_id == "00000" and password == "1234567890":
        self.admin_id = admin_id
        return True
    else:
        return False
    
def authenticate_patient(self, ssn, password):
    return True # Delete this line after connecting database to your frame 
    # Add necessary attributes to the class. The __init__ should look like below:
    """
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.nurse_id = 11270 #hardcoded
        self.db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Enter your passwd here",
        auth_plugin='mysql_native_password'
        )
        print(self.db_connection)
        self.db_cursor = self.db_connection.cursor(buffered=True)
        self.db_cursor.execute("USE comp306project")
        self.pack(fill="both", expand=True)
        self.setup_login_ui()
    """
    # The init above belongs to NursesFrame. Remember to change variable name of nurse_id to ssn.
    query = "SELECT * FROM patient WHERE patient.ssn = %s;"
    self.db_cursor.execute(query, (ssn,))
    patient = self.db_cursor.fetchone()

    if patient and password == "1234567890":
        self.ssn = ssn
        return True
    else:
        return False