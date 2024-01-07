import tkinter as tk
import sqlite3


conn = sqlite3.connect('comp306project.db')
cursor = conn.cursor()

def fetch_patient():
    patient_ssn = entry_patient_ssn.get()
    if authenticate_ssn(patient_ssn):
        query = "SELECT * FROM PATIENT WHERE PatientSSN = ?"
        cursor.execute(query, (patient_ssn,))
        patient_data = cursor.fetchone()
        if patient_data:
            display_patient_info(patient_data)
        else:
            clear_patient_info()
    else:
        clear_patient_info()
        patient_info.config(state=tk.NORMAL)
        patient_info.insert(tk.END, "Authentication failed. Invalid SSN.\n")
        patient_info.config(state=tk.DISABLED)


def authenticate_ssn(ssn):
    query = "SELECT PatientSSN FROM PATIENT WHERE PatientSSN = ?"
    cursor.execute(query, (ssn,))
    result = cursor.fetchone()
    return result is not None



def display_patient_info(data):
    clear_patient_info()
    patient_info.config(state=tk.NORMAL)
    patient_info.insert(tk.END, f"Patient SSN: {data[0]}\n")
    patient_info.insert(tk.END, f"Name: {data[2]}\n")
    patient_info.insert(tk.END, f"Birth Date: {data[3]}\n")
    patient_info.insert(tk.END, f"Blood Type: {data[4]}\n")
    patient_info.insert(tk.END, f"City: {data[5]}\n")
    patient_info.insert(tk.END, f"Street: {data[6]}\n")
    patient_info.insert(tk.END, f"State: {data[7]}\n")
    patient_info.insert(tk.END, f"Sex: {data[8]}\n")
    patient_info.config(state=tk.DISABLED)

def clear_patient_info():
    patient_info.config(state=tk.NORMAL)
    patient_info.delete('1.0', tk.END)
    patient_info.config(state=tk.DISABLED)


root = tk.Tk()
root.title("Patient Information")


label_patient_ssn = tk.Label(root, text="Enter Patient SSN:")
label_patient_ssn.pack()

entry_patient_ssn = tk.Entry(root)
entry_patient_ssn.pack()

button_fetch_patient = tk.Button(root, text="Fetch Patient", command=fetch_patient)
button_fetch_patient.pack()

patient_info = tk.Text(root, height=10, width=50)
patient_info.pack()
patient_info.config(state=tk.DISABLED)

root.mainloop()
