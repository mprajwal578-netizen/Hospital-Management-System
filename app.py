import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-for-local-development")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "hospital_management"),
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def query_db(sql, params=(), fetch=False):
    conn = get_db()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        result = cur.fetchall() if fetch else None
        conn.commit()
        cur.close()
        return result
    finally:
        conn.close()

@app.route("/")
def index():
    try:
        stats = {
            "patients": query_db("SELECT COUNT(*) AS n FROM patients", fetch=True)[0]["n"],
            "doctors": query_db("SELECT COUNT(*) AS n FROM doctors", fetch=True)[0]["n"],
            "appointments": query_db("SELECT COUNT(*) AS n FROM appointments", fetch=True)[0]["n"],
        }
        recent = query_db("""
            SELECT a.appointment_id, p.full_name AS patient, d.full_name AS doctor,
                   a.appointment_date, a.status
            FROM appointments a
            JOIN patients p ON p.patient_id = a.patient_id
            JOIN doctors d ON d.doctor_id = a.doctor_id
            ORDER BY a.appointment_date DESC LIMIT 5
        """, fetch=True)
        return render_template("index.html", stats=stats, recent=recent)
    except Error as e:
        return render_template("error.html", message=str(e), setup=True), 500

@app.route("/patients", methods=["GET", "POST"])
def patients():
    if request.method == "POST":
        name = request.form.get("full_name", "").strip()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "")
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip() or None
        address = request.form.get("address", "").strip() or None
        if not name or not age.isdigit() or int(age) < 0:
            flash("Enter a patient name and a valid age.", "danger")
            return redirect(url_for("patients"))
        try:
            query_db("""INSERT INTO patients
                (full_name, age, gender, phone, email, address)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (name, int(age), gender, phone, email, address))
            flash("Patient added successfully.", "success")
        except Error as e:
            flash(f"Could not add patient: {e}", "danger")
        return redirect(url_for("patients"))
    rows = query_db("SELECT * FROM patients ORDER BY patient_id DESC", fetch=True)
    return render_template("patients.html", patients=rows)

@app.route("/patients/delete/<int:patient_id>", methods=["POST"])
def delete_patient(patient_id):
    try:
        query_db("DELETE FROM patients WHERE patient_id=%s", (patient_id,))
        flash("Patient deleted. Related appointments are also removed.", "success")
    except Error as e:
        flash(f"Could not delete patient: {e}", "danger")
    return redirect(url_for("patients"))

@app.route("/doctors", methods=["GET", "POST"])
def doctors():
    if request.method == "POST":
        name = request.form.get("full_name", "").strip()
        department = request.form.get("department", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip() or None
        if not name or not department:
            flash("Doctor name and department are required.", "danger")
            return redirect(url_for("doctors"))
        try:
            query_db("""INSERT INTO doctors (full_name, department, phone, email)
                        VALUES (%s, %s, %s, %s)""", (name, department, phone, email))
            flash("Doctor added successfully.", "success")
        except Error as e:
            flash(f"Could not add doctor: {e}", "danger")
        return redirect(url_for("doctors"))
    rows = query_db("SELECT * FROM doctors ORDER BY doctor_id DESC", fetch=True)
    return render_template("doctors.html", doctors=rows)

@app.route("/doctors/delete/<int:doctor_id>", methods=["POST"])
def delete_doctor(doctor_id):
    try:
        query_db("DELETE FROM doctors WHERE doctor_id=%s", (doctor_id,))
        flash("Doctor deleted. Related appointments are also removed.", "success")
    except Error as e:
        flash(f"Could not delete doctor: {e}", "danger")
    return redirect(url_for("doctors"))

@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    if request.method == "POST":
        patient_id = request.form.get("patient_id", "")
        doctor_id = request.form.get("doctor_id", "")
        date = request.form.get("appointment_date", "")
        reason = request.form.get("reason", "").strip() or None
        if not (patient_id.isdigit() and doctor_id.isdigit() and date):
            flash("Choose a patient, doctor, and appointment date.", "danger")
            return redirect(url_for("appointments"))
        try:
            query_db("""INSERT INTO appointments
                (patient_id, doctor_id, appointment_date, reason)
                VALUES (%s, %s, %s, %s)""",
                (int(patient_id), int(doctor_id), date, reason))
            flash("Appointment booked successfully.", "success")
        except Error as e:
            flash(f"Could not book appointment: {e}", "danger")
        return redirect(url_for("appointments"))
    patients_list = query_db("SELECT patient_id, full_name FROM patients ORDER BY full_name", fetch=True)
    doctors_list = query_db("SELECT doctor_id, full_name, department FROM doctors ORDER BY full_name", fetch=True)
    rows = query_db("""
        SELECT a.*, p.full_name AS patient, d.full_name AS doctor, d.department
        FROM appointments a
        JOIN patients p ON p.patient_id=a.patient_id
        JOIN doctors d ON d.doctor_id=a.doctor_id
        ORDER BY a.appointment_date DESC
    """, fetch=True)
    return render_template("appointments.html", appointments=rows,
                           patients=patients_list, doctors=doctors_list)

@app.route("/appointments/status/<int:appointment_id>", methods=["POST"])
def update_status(appointment_id):
    status = request.form.get("status", "")
    if status not in ("Scheduled", "Completed", "Cancelled"):
        flash("Invalid appointment status.", "danger")
    else:
        try:
            query_db("UPDATE appointments SET status=%s WHERE appointment_id=%s",
                     (status, appointment_id))
            flash("Appointment status updated.", "success")
        except Error as e:
            flash(f"Could not update status: {e}", "danger")
    return redirect(url_for("appointments"))

@app.route("/reports")
def reports():
    try:
        rows = query_db("""
            SELECT d.full_name AS doctor, d.department,
                   COUNT(a.appointment_id) AS total_appointments
            FROM doctors d
            LEFT JOIN appointments a ON a.doctor_id=d.doctor_id
            GROUP BY d.doctor_id, d.full_name, d.department
            ORDER BY total_appointments DESC, d.full_name
        """, fetch=True)
        return render_template("reports.html", reports=rows)
    except Error as e:
        return render_template("error.html", message=str(e), setup=False), 500

@app.errorhandler(404)
def not_found(_error):
    return render_template("error.html", message="The page you requested was not found.", setup=False), 404

if __name__ == "__main__":
    app.run(debug=True)
