from models import Patient, Doctor, Appointment, Treatment, Bill
from controllers.data_manager import DataManager

class HospitalController:
    """Main controller class (Single Responsibility Principle)"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.patients = {}
        self.doctors = {}
        self.appointments = {}
        self.treatments = {}
        self.bills = {}
        
        # Load all data
        self.load_all_data()
    
    def load_all_data(self):
        """Load all data from storage"""
        # Load patients
        patients_data = self.data_manager.load_data('patients.json')
        for data in patients_data:
            patient = Patient.from_dict(data)
            self.patients[patient.id] = patient
        
        # Load doctors
        doctors_data = self.data_manager.load_data('doctors.json')
        for data in doctors_data:
            doctor = Doctor.from_dict(data)
            self.doctors[doctor.id] = doctor
        
        # Load appointments
        appointments_data = self.data_manager.load_data('appointments.json')
        for data in appointments_data:
            appointment = Appointment.from_dict(data)
            self.appointments[appointment.id] = appointment
        
        # Load treatments
        treatments_data = self.data_manager.load_data('treatments.json')
        for data in treatments_data:
            treatment = Treatment.from_dict(data)
            self.treatments[treatment.id] = treatment
        
        # Load bills
        bills_data = self.data_manager.load_data('bills.json')
        for data in bills_data:
            bill = Bill.from_dict(data)
            self.bills[bill.id] = bill
    
    def save_all_data(self):
        """Save all data to storage"""
        # Save patients
        patients_data = [p.to_dict() for p in self.patients.values()]
        self.data_manager.save_data('patients.json', patients_data)
        
        # Save doctors
        doctors_data = [d.to_dict() for d in self.doctors.values()]
        self.data_manager.save_data('doctors.json', doctors_data)
        
        # Save appointments
        appointments_data = [a.to_dict() for a in self.appointments.values()]
        self.data_manager.save_data('appointments.json', appointments_data)
        
        # Save treatments
        treatments_data = [t.to_dict() for t in self.treatments.values()]
        self.data_manager.save_data('treatments.json', treatments_data)
        
        # Save bills
        bills_data = [b.to_dict() for b in self.bills.values()]
        self.data_manager.save_data('bills.json', bills_data)
    
    # Patient operations
    def add_patient(self, patient_data):
        """Add a new patient"""
        patient_id = self.data_manager.generate_id('PAT')
        patient = Patient(
            patient_id,
            patient_data['name'],
            patient_data['phone'],
            patient_data['email'],
            patient_data['address'],
            patient_data['dob'],
            patient_data['blood_group'],
            patient_data['emergency_contact']
        )
        self.patients[patient_id] = patient
        self.save_all_data()
        return patient
    
    def get_all_patients(self):
        """Get all patients"""
        return list(self.patients.values())
    
    def get_patient(self, patient_id):
        """Get patient by ID"""
        return self.patients.get(patient_id)
    
    def update_patient(self, patient_id, updated_data):
        """Update patient information"""
        patient = self.get_patient(patient_id)
        if patient:
            for key, value in updated_data.items():
                if hasattr(patient, key):
                    setattr(patient, f"_{key}", value)
            self.save_all_data()
            return True
        return False
    
    def delete_patient(self, patient_id):
        """Delete patient"""
        if patient_id in self.patients:
            del self.patients[patient_id]
            self.save_all_data()
            return True
        return False
    
    # Doctor operations
    def add_doctor(self, doctor_data):
        """Add a new doctor"""
        doctor_id = self.data_manager.generate_id('DOC')
        doctor = Doctor(
            doctor_id,
            doctor_data['name'],
            doctor_data['phone'],
            doctor_data['email'],
            doctor_data['address'],
            doctor_data['specialization'],
            doctor_data['qualification'],
            doctor_data['experience'],
            doctor_data['consultation_fee']
        )
        self.doctors[doctor_id] = doctor
        self.save_all_data()
        return doctor
    
    def get_all_doctors(self):
        """Get all doctors"""
        return list(self.doctors.values())
    
    def get_doctor(self, doctor_id):
        """Get doctor by ID"""
        return self.doctors.get(doctor_id)
    
    def update_doctor(self, doctor_id, updated_data):
        """Update doctor information"""
        doctor = self.get_doctor(doctor_id)
        if doctor:
            for key, value in updated_data.items():
                if hasattr(doctor, key):
                    setattr(doctor, f"_{key}", value)
            self.save_all_data()
            return True
        return False
    
    def delete_doctor(self, doctor_id):
        """Delete doctor"""
        if doctor_id in self.doctors:
            del self.doctors[doctor_id]
            self.save_all_data()
            return True
        return False
    
    # Appointment operations
    def add_appointment(self, appointment_data):
        """Add a new appointment"""
        appointment_id = self.data_manager.generate_id('APT')
        appointment = Appointment(
            appointment_id,
            appointment_data['patient_id'],
            appointment_data['doctor_id'],
            appointment_data['date'],
            appointment_data['time'],
            appointment_data['reason']
        )
        self.appointments[appointment_id] = appointment
        
        # Update patient and doctor appointments
        patient = self.get_patient(appointment_data['patient_id'])
        if patient:
            patient.add_appointment(appointment_id)
        
        doctor = self.get_doctor(appointment_data['doctor_id'])
        if doctor:
            doctor.add_appointment(appointment_id)
        
        self.save_all_data()
        return appointment
    
    def get_all_appointments(self):
        """Get all appointments"""
        return list(self.appointments.values())
    
    def get_appointment(self, appointment_id):
        """Get appointment by ID"""
        return self.appointments.get(appointment_id)
    
    def update_appointment_status(self, appointment_id, status):
        """Update appointment status"""
        appointment = self.get_appointment(appointment_id)
        if appointment:
            if status == "Confirmed":
                appointment.confirm()
            elif status == "Completed":
                appointment.complete()
            elif status == "Cancelled":
                appointment.cancel()
            self.save_all_data()
            return True
        return False
    
    def delete_appointment(self, appointment_id):
        """Delete appointment"""
        if appointment_id in self.appointments:
            del self.appointments[appointment_id]
            self.save_all_data()
            return True
        return False
    
    # Treatment operations
    def add_treatment(self, treatment_data):
        """Add a new treatment"""
        treatment_id = self.data_manager.generate_id('TRT')
        treatment = Treatment(
            treatment_id,
            treatment_data['patient_id'],
            treatment_data['doctor_id'],
            treatment_data['diagnosis'],
            treatment_data['prescription'],
            treatment_data['notes'],
            treatment_data['cost']
        )
        self.treatments[treatment_id] = treatment
        
        # Create bill for treatment
        self.create_bill(treatment_data['patient_id'], treatment_id, treatment_data['cost'])
        
        self.save_all_data()
        return treatment
    
    def get_all_treatments(self):
        """Get all treatments"""
        return list(self.treatments.values())
    
    def get_patient_treatments(self, patient_id):
        """Get treatments for a specific patient"""
        return [t for t in self.treatments.values() if t.patient_id == patient_id]
    
    # Bill operations
    def create_bill(self, patient_id, treatment_id, amount):
        """Create a new bill"""
        bill_id = self.data_manager.generate_id('BIL')
        
        # Check if patient already has an unpaid bill
        existing_bill = None
        for bill in self.bills.values():
            if bill.patient_id == patient_id and bill.status != Bill.STATUS_PAID:
                existing_bill = bill
                break
        
        if existing_bill:
            # Add to existing bill
            existing_bill.add_item(f"Treatment {treatment_id}", 1, amount)
            bill = existing_bill
        else:
            # Create new bill
            bill = Bill(bill_id, patient_id)
            bill.add_item(f"Treatment {treatment_id}", 1, amount)
            self.bills[bill_id] = bill
        
        self.save_all_data()
        return bill
    
    def get_all_bills(self):
        """Get all bills"""
        return list(self.bills.values())
    
    def get_patient_bills(self, patient_id):
        """Get bills for a specific patient"""
        return [b for b in self.bills.values() if b.patient_id == patient_id]
    
    def make_payment(self, bill_id, amount):
        """Make a payment for a bill"""
        bill = self.bills.get(bill_id)
        if bill:
            bill.make_payment(amount)
            self.save_all_data()
            return True
        return False
    
    # Report operations
    def generate_patient_report(self):
        """Generate patient statistics report"""
        total_patients = len(self.patients)
        total_appointments = len(self.appointments)
        total_treatments = len(self.treatments)
        total_bills = len(self.bills)
        total_revenue = sum(b.total_amount for b in self.bills.values())
        total_paid = sum(b.paid_amount for b in self.bills.values())
        
        return {
            'total_patients': total_patients,
            'total_appointments': total_appointments,
            'total_treatments': total_treatments,
            'total_bills': total_bills,
            'total_revenue': total_revenue,
            'total_paid': total_paid,
            'outstanding': total_revenue - total_paid
        }
    
    def generate_doctor_report(self):
        """Generate doctor performance report"""
        report = {}
        for doctor in self.doctors.values():
            doctor_appointments = [a for a in self.appointments.values() if a.doctor_id == doctor.id]
            doctor_treatments = [t for t in self.treatments.values() if t.doctor_id == doctor.id]
            
            report[doctor.name] = {
                'appointments': len(doctor_appointments),
                'treatments': len(doctor_treatments),
                'revenue': sum(t.cost for t in doctor_treatments)
            }
        
        return report