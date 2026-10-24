CREATE DATABASE IF NOT EXISTS hospital_management;
USE hospital_management;

CREATE TABLE IF NOT EXISTS patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    age INT NOT NULL CHECK (age >= 0),
    gender ENUM('Female','Male','Other','Prefer not to say') NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(120) UNIQUE,
    address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    department VARCHAR(80) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(120) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATETIME NOT NULL,
    reason VARCHAR(255),
    status ENUM('Scheduled','Completed','Cancelled') NOT NULL DEFAULT 'Scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_appointment_patient FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id) ON DELETE CASCADE,
    CONSTRAINT fk_appointment_doctor FOREIGN KEY (doctor_id)
        REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    INDEX idx_appointment_date (appointment_date)
);

CREATE OR REPLACE VIEW appointment_report AS
SELECT a.appointment_id, p.full_name AS patient_name, d.full_name AS doctor_name,
       d.department, a.appointment_date, a.status, a.reason
FROM appointments a
JOIN patients p ON p.patient_id = a.patient_id
JOIN doctors d ON d.doctor_id = a.doctor_id;

INSERT IGNORE INTO patients (patient_id, full_name, age, gender, phone, email, address) VALUES
(1, 'Aarav Patil', 25, 'Male', '9000000001', 'aarav.demo@example.com', 'Nagpur'),
(2, 'Ananya Sharma', 31, 'Female', '9000000002', 'ananya.demo@example.com', 'Wardha');

INSERT IGNORE INTO doctors (doctor_id, full_name, department, phone, email) VALUES
(1, 'Dr. Meera Deshmukh', 'General Medicine', '9111111111', 'meera.demo@example.com'),
(2, 'Dr. Rahul Joshi', 'Cardiology', '9222222222', 'rahul.demo@example.com');

INSERT IGNORE INTO appointments
(appointment_id, patient_id, doctor_id, appointment_date, reason, status) VALUES
(1, 1, 1, '2026-11-02 10:30:00', 'Routine check-up', 'Scheduled'),
(2, 2, 2, '2026-11-03 12:00:00', 'Consultation', 'Scheduled');
