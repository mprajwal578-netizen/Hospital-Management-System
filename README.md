# Hospital Management System

A student DBMS mini-project built with Python, Flask, and MySQL. It demonstrates relational tables, primary/foreign keys, constraints, CRUD operations, joins, a view, and summary reporting.

## Features
- Dashboard with patient, doctor, and appointment counts
- Add/list/delete patients
- Add/list/delete doctors
- Book appointments and update their status
- Appointment report using SQL joins and `GROUP BY`
- `appointment_report` SQL view

## Technology stack
- Python 3.10+
- Flask
- MySQL 8+
- mysql-connector-python
- HTML/CSS (Jinja templates)

## 1. Create the database
1. Start the MySQL Server.
2. Open MySQL Workbench and connect to your local server.
3. Open `schema.sql` and execute the complete script.
4. Confirm the `hospital_management` schema has `patients`, `doctors`, `appointments`, and `appointment_report`.

The SQL file includes demonstration records. Use fictional data only.

## 2. Configure the application
Open a terminal in this folder. Create and activate a virtual environment on Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt instead:
```bat
.venv\Scripts\activate.bat
```

Install packages:
```powershell
python -m pip install -r requirements.txt
```

Set the database password for this terminal session (replace the example with your actual local MySQL password):
```powershell
$env:DB_USER="root"
$env:DB_PASSWORD="YOUR_MYSQL_PASSWORD"
$env:DB_NAME="hospital_management"
```

Do not commit your real password to GitHub. `.env` is intentionally ignored by Git.

## 3. Run the website
```powershell
python app.py
```
Open `http://127.0.0.1:5000` in your browser. Keep the terminal running while you use the site. Press `Ctrl+C` to stop it.

## Troubleshooting
- **Access denied for user**: verify `DB_USER` and `DB_PASSWORD`; test the same login in Workbench.
- **Unknown database**: run `schema.sql` in Workbench first.
- **Can't connect to MySQL server**: check that the MySQL80 Windows service is running.
- **Template not found**: make sure the `templates` folder remains beside `app.py`.
- **Port 5000 busy**: close the other Flask app or change the port in `app.run()`.

## Database design
- `patients(patient_id PK, ...)`
- `doctors(doctor_id PK, ...)`
- `appointments(appointment_id PK, patient_id FK, doctor_id FK, ...)`

One patient can have many appointments; one doctor can have many appointments. `appointments` connects patients and doctors. Patient and doctor details are stored once, reducing update anomalies.

## Example SQL queries
```sql
-- List appointments with patient and doctor names
SELECT a.appointment_id, p.full_name, d.full_name, a.appointment_date, a.status
FROM appointments a
JOIN patients p ON p.patient_id = a.patient_id
JOIN doctors d ON d.doctor_id = a.doctor_id;

-- Count appointments by department
SELECT d.department, COUNT(*) AS total
FROM appointments a JOIN doctors d ON d.doctor_id = a.doctor_id
GROUP BY d.department;

-- Read the view
SELECT * FROM appointment_report;
```

## GitHub upload
1. Create a new empty repository named `hospital-management-system` on GitHub.
2. In this project folder, run:
```powershell
git init
git add .
git commit -m "Initial Hospital Management System project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/hospital-management-system.git
git push -u origin main
```
Replace `YOUR-USERNAME` with your GitHub username. Do not upload passwords or private patient data.

## Project report
See `PROJECT_REPORT.md` for the report structure. Capture your own screenshots after running the project and put them in `screenshots/`.
