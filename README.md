# 🏥 MediTrack — Hospital Management System

A desktop application for managing hospital operations, built with Python and Tkinter. MediTrack provides role-based access for patients, doctors, nurses, and administrators, backed by a MySQL database.

---

## Features

**Dashboard**
- Central hub with role-selection buttons (Patient, Nurse, Doctor, Admin)
- Collapsible sidebar navigation
- 1200×700 desktop window with a persistent header

**Patient Portal**
- SSN-based login
- View personal information (name, gender, blood type, address, phone)
- Book appointments by selecting a doctor specialty, day, and time slot
- View upcoming appointments (ID, duration, date, floor, room number)
- View companions (name, relationship, phone, dates)
- View prescriptions (diagnosis, medicines)

**Doctor Portal**
- Role-specific views for physician workflows

**Nurse Portal**
- Role-specific views for nursing staff

**Admin Portal**
- Administrative management interface

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| GUI | Tkinter + ttk |
| Image handling | Pillow (PIL) |
| Database | MySQL (via `mysql-connector-python`) |
| Data generation | Faker + Jupyter Notebooks |
| Database file | SQLite (`comp306project.db`) |

---

## Project Structure

```
hospital-management-system/
├── MediTrack.py              # Entry point — launches the app
├── Main.py                   # Root window, sidebar, and frame router
├── Dashboard.py              # Welcome screen with role-selection buttons
├── Patients.py               # Patient login and all patient features
├── Doctors.py                # Doctor portal
├── Nurses.py                 # Nurse portal
├── Admin.py                  # Admin portal
├── sql/                      # SQL schema and seed scripts
├── DataBasePopulator.ipynb   # Jupyter notebook to populate the database
├── FakerToCSV.ipynb          # Generates synthetic patient/staff data via Faker
├── comp306project.db         # SQLite database file
└── hospital.jpeg             # Dashboard background image
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- MySQL Server running locally
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/iremkrc/hospital-management-system.git
   cd hospital-management-system
   ```

2. **Install dependencies**
   ```bash
   pip install pillow mysql-connector-python
   ```
   For the data generation notebooks:
   ```bash
   pip install faker jupyter
   ```

3. **Set up the database**

   Start MySQL and create the schema using the scripts in the `sql/` folder:
   ```bash
   mysql -u root -p < sql/<schema_file>.sql
   ```
   Then populate the database by running `DataBasePopulator.ipynb` in Jupyter.

4. **Configure the database connection**

   Open `Patients.py` (and other role files as needed) and update the connection credentials:
   ```python
   self.db_connection = mysql.connector.connect(
       host="localhost",
       user="root",
       passwd="your_password",
       auth_plugin='mysql_native_password'
   )
   ```

5. **Run the application**
   ```bash
   python MediTrack.py
   ```

---

## Usage

On launch, the Dashboard presents four role buttons. Select your role to proceed:

- **I'm a Patient** — log in with your SSN to access appointments, prescriptions, and personal info.
- **I'm a Nurse** — access the nurse management panel.
- **I'm a Doctor** — access the doctor management panel.
- **I'm an Admin** — access administrative controls.

The sidebar (toggled with the ☰/✕ button) lets you switch between sections at any time.

---

## Database Schema

The MySQL database (`comp306project`) includes tables for:

- `patient` — patient demographics and credentials
- `doctor` — doctor profiles and expertise
- `appointment` — appointment records with date, floor, and room
- `participates` — links patients to appointments
- `prescription` / `prescription_medicine` — prescriptions and associated medicines
- `writes` — links prescriptions to patients
- `companion` — patient companions and relationships

---

## Data Generation

Two Jupyter notebooks are included for development and testing:

- **`FakerToCSV.ipynb`** — Uses the [Faker](https://faker.readthedocs.io/) library to generate realistic synthetic data and export it as CSV files.
- **`DataBasePopulator.ipynb`** — Reads those CSVs and inserts records into the MySQL database.

