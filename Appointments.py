import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ScrollableFrameUtil import ScrollableFrame

class AppointmentsFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="white", height=10000, padx=10, pady=10)
        self.pack_propagate(False)
        
        style = ttk.Style()
        style.configure('Curved.TFrame', borderwidth=5, relief="ridge", highlightthickness=10)
        options_frame = ttk.Frame(self, style='Curved.TFrame')
        options_frame.pack(side="right", padx=10, pady=10, fill="y")

        list_button = ttk.Button(options_frame, text="List", command=self.list_appointments, width=20)
        list_button.pack(side="top", padx=10, pady=10)
        
        self.sort_var = tk.StringVar()
        sort_dropdown = ttk.Combobox(options_frame, textvariable=self.sort_var, background="lightgray", values=["Date Sort", "Clinic Sort"], state="readonly")
        sort_dropdown.bind("<Button-1>", lambda event: sort_dropdown.focus())
        sort_dropdown.pack(side="top", padx=10, pady=10)

        self.filter_var = tk.StringVar()
        self.filter_listbox = tk.Listbox(options_frame, selectmode=tk.MULTIPLE, exportselection=0, width=21)
        filter_options = ["All", "Past Appointments", "Upcoming Appointments", "Specific Clinic"]
        for option in filter_options:
            self.filter_listbox.insert(tk.END, option)
        self.filter_listbox.pack(side="top", padx=10, pady=10)
        
        self.appointments_area = tk.Frame(self)
        self.appointments_area.pack(padx=10, pady=10, fill="both", expand=True, side="left")
        
        self.scrollable_frame = ScrollableFrame(self.appointments_area)
        self.scrollable_frame.pack(expand=True, fill="both")
        
    def mouse_scroll(self, event):
        if event.delta:
            self.appointments_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def update_scrollregion(self, event=None):
        self.appointments_canvas.configure(scrollregion=self.appointments_canvas.bbox("all"))


    def list_appointments(self):
        sort_type = self.sort_var.get()
        selected_filters = [self.filter_listbox.get(idx) for idx in self.filter_listbox.curselection()]

        params = []
        for selected_filter in selected_filters:
            if selected_filter == "All":
                params.append("all_appointments")
            elif selected_filter == "Past Appointments":
                params.append("past_appointments")
            elif selected_filter == "Upcoming Appointments":
                params.append("upcoming_appointments")
            elif selected_filter == "Specific Clinic":
                params.append("specific_clinic")

        if sort_type == "Date Sort":
            params.append("date_sort")
        elif sort_type == "Clinic Sort":
            params.append("clinic_sort")

        user_id = "user123"
        appointments = get_appointments(user_id, params)

        self.update_appointments_text(appointments)
        

    def update_appointments_text(self, appointments):
        for widget in self.scrollable_frame.scrollable_frame.winfo_children():
            widget.destroy()

        for appointment in appointments:
            appointment_frame = ttk.Frame(self.scrollable_frame.scrollable_frame, padding=(5,5,5,5), style='Curved.TFrame')
            appointment_frame.pack(fill="x", pady=5)

            appointment_label = ttk.Label(appointment_frame, text=f"{appointment}", style='TLabel')
            appointment_label.pack(side="left", fill="x")

            cancel_button = ttk.Button(appointment_frame, text="Cancel", command=lambda app_id=appointment[0]: self.cancel_appointment_popup(app_id))
            cancel_button.pack(side="right", padx=5)
            
        

    def cancel_appointment_popup(self, appointment_id=None):
        if appointment_id is None and not self.appointment_id_entry.get():
            return
        appointment_id = appointment_id or self.appointment_id_entry.get()
        
        result = messagebox.askquestion("Cancel Appointment", f"Are you sure to cancel appointment {appointment_id}?")
        if result == "yes":
            self.cancel_appointment(appointment_id)

    def cancel_appointment(self, appointment_id):
        print(f"Cancelling appointment {appointment_id}")

        for widget in self.scrollable_frame.scrollable_frame.winfo_children():
            if isinstance(widget, ttk.Frame):
                appointment_info = widget.winfo_children()[0].cget("text")
                if appointment_id in appointment_info:
                    widget.destroy()
                    break

def cancel_appointment(appointment_id):
    print(f"Cancelling appointment {appointment_id}")
    

def get_appointments(user_id, params):
    return [("Appointment 1", "2023-01-01", "Clinic A"),
            ("Appointment 2", "2023-02-01", "Clinic B")] * 100




