"""
Unit Testing for MediCare Hospital Management System
"""

import unittest
import sys
import os
import tempfile
import shutil
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.person import Person
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.treatment import Treatment
from models.bill import Bill
from controllers.data_manager import DataManager
from controllers.hospital_controller import HospitalController


class TestPersonModel(unittest.TestCase):
    def setUp(self):
        class TestPerson(Person):
            def get_details(self):
                return {'name': self.name}
        
        self.person = TestPerson(
            "P001", "John Doe", "1234567890", 
            "john@example.com", "123 Main St"
        )
    
    def test_person_initialization(self):
        self.assertEqual(self.person.id, "P001")
        self.assertEqual(self.person.name, "John Doe")
    
    def test_name_setter(self):
        self.person.name = "Jane Doe"
        self.assertEqual(self.person.name, "Jane Doe")
    
    def test_phone_setter(self):
        self.person.phone = "0987654321"
        self.assertEqual(self.person.phone, "0987654321")
    
    def test_to_dict(self):
        result = self.person.to_dict()
        self.assertEqual(result['id'], "P001")
        self.assertEqual(result['name'], "John Doe")


class TestPatientModel(unittest.TestCase):
    def setUp(self):
        self.patient = Patient(
            "PAT001", "John Smith", "0771234567", 
            "john@email.com", "Colombo", "1990-01-15", 
            "O+", "0777654321"
        )
    
    def test_patient_initialization(self):
        self.assertEqual(self.patient.id, "PAT001")
        self.assertEqual(self.patient.name, "John Smith")
        self.assertEqual(self.patient.blood_group, "O+")
    
    def test_blood_group_setter(self):
        self.patient.blood_group = "A+"
        self.assertEqual(self.patient.blood_group, "A+")
    
    def test_add_medical_record(self):
        record = "Flu diagnosis"
        self.patient.add_medical_record(record)
        self.assertIn(record, self.patient.medical_history)
    
    def test_add_appointment(self):
        self.patient.add_appointment("APT001")
        self.assertIn("APT001", self.patient._appointments)
    
    def test_get_details(self):
        details = self.patient.get_details()
        self.assertEqual(details['ID'], "PAT001")
    
    def test_to_dict(self):
        result = self.patient.to_dict()
        self.assertEqual(result['id'], "PAT001")
    
    def test_from_dict(self):
        data = {
            'id': 'PAT002',
            'name': 'Jane Doe',
            'phone': '0778888888',
            'email': 'jane@email.com',
            'address': 'Kandy',
            'date_of_birth': '1995-05-20',
            'blood_group': 'B+',
            'emergency_contact': '0779999999',
            'medical_history': [],
            'appointments': [],
            'created_date': '2024-01-01 10:00:00'
        }
        patient = Patient.from_dict(data)
        self.assertEqual(patient.id, "PAT002")
        self.assertEqual(patient.blood_group, "B+")


class TestDoctorModel(unittest.TestCase):
    def setUp(self):
        self.doctor = Doctor(
            "DOC001", "Dr. Kirushiyan", "0771234567",
            "dr@hospital.com", "Colombo", "Cardiology",
            "MBBS, MD", 10, 1500.00
        )
    
    def test_doctor_initialization(self):
        self.assertEqual(self.doctor.id, "DOC001")
        self.assertEqual(self.doctor.name, "Dr. Kirushiyan")
        self.assertEqual(self.doctor.specialization, "Cardiology")
        self.assertEqual(self.doctor.consultation_fee, 1500.00)
    
    def test_consultation_fee_setter(self):
        self.doctor.consultation_fee = 2000.00
        self.assertEqual(self.doctor.consultation_fee, 2000.00)
    
    def test_add_availability(self):
        self.doctor.add_availability("Monday", "09:00-12:00")
        self.assertEqual(len(self.doctor.availability), 1)
    
    def test_get_details(self):
        details = self.doctor.get_details()
        self.assertEqual(details['ID'], "DOC001")
    
    def test_to_dict(self):
        result = self.doctor.to_dict()
        self.assertEqual(result['id'], "DOC001")
    
    def test_from_dict(self):
        data = {
            'id': 'DOC002',
            'name': 'Dr. Sarah',
            'phone': '0778888888',
            'email': 'sarah@hospital.com',
            'address': 'Galle',
            'specialization': 'Neurology',
            'qualification': 'MD',
            'experience': 8,
            'consultation_fee': 1800.00,
            'availability': [],
            'appointments': [],
            'created_date': '2024-01-01 10:00:00'
        }
        doctor = Doctor.from_dict(data)
        self.assertEqual(doctor.id, "DOC002")
        self.assertEqual(doctor.specialization, "Neurology")


class TestAppointmentModel(unittest.TestCase):
    def setUp(self):
        self.appointment = Appointment(
            "APT001", "PAT001", "DOC001", 
            "2024-03-15", "10:30", "Regular checkup"
        )
    
    def test_appointment_initialization(self):
        self.assertEqual(self.appointment.id, "APT001")
        self.assertEqual(self.appointment.status, "Pending")
    
    def test_confirm_appointment(self):
        self.appointment.confirm()
        self.assertEqual(self.appointment.status, "Confirmed")
    
    def test_complete_appointment(self):
        self.appointment.complete()
        self.assertEqual(self.appointment.status, "Completed")
    
    def test_cancel_appointment(self):
        self.appointment.cancel()
        self.assertEqual(self.appointment.status, "Cancelled")
    
    def test_to_dict(self):
        result = self.appointment.to_dict()
        self.assertEqual(result['id'], "APT001")
    
    def test_from_dict(self):
        data = {
            'id': 'APT002',
            'patient_id': 'PAT002',
            'doctor_id': 'DOC002',
            'date': '2024-03-16',
            'time': '14:00',
            'reason': 'Fever',
            'status': 'Confirmed',
            'created_date': '2024-03-01 09:00:00'
        }
        appointment = Appointment.from_dict(data)
        self.assertEqual(appointment.id, "APT002")
        self.assertEqual(appointment.status, "Confirmed")


class TestTreatmentModel(unittest.TestCase):
    def setUp(self):
        self.treatment = Treatment(
            "TRT001", "PAT001", "DOC001",
            "Acute Bronchitis", "Amoxicillin 500mg",
            "Chest X-ray recommended", 2500.00
        )
    
    def test_treatment_initialization(self):
        self.assertEqual(self.treatment.id, "TRT001")
        self.assertEqual(self.treatment.diagnosis, "Acute Bronchitis")
        self.assertEqual(self.treatment.cost, 2500.00)
    
    def test_to_dict(self):
        result = self.treatment.to_dict()
        self.assertEqual(result['id'], "TRT001")
    
    def test_from_dict(self):
        data = {
            'id': 'TRT002',
            'patient_id': 'PAT002',
            'doctor_id': 'DOC002',
            'diagnosis': 'Flu',
            'prescription': 'Paracetamol',
            'notes': 'Rest',
            'cost': 500.00,
            'date': '2024-03-01',
            'time': '10:30:00'
        }
        treatment = Treatment.from_dict(data)
        self.assertEqual(treatment.id, "TRT002")
        self.assertEqual(treatment.diagnosis, "Flu")


class TestBillModel(unittest.TestCase):
    def setUp(self):
        self.bill = Bill("BIL001", "PAT001")
        self.bill.add_item("Consultation", 1, 1500.00)
        self.bill.add_item("Medicine", 2, 250.00)
    
    def test_bill_initialization(self):
        self.assertEqual(self.bill.id, "BIL001")
        self.assertEqual(self.bill.status, "Unpaid")
    
    def test_calculate_total(self):
        self.assertEqual(self.bill.total_amount, 2000.00)
    
    def test_make_payment_full(self):
        self.bill.make_payment(2000.00)
        self.assertEqual(self.bill.status, "Paid")
    
    def test_make_payment_partial(self):
        self.bill.make_payment(1000.00)
        self.assertEqual(self.bill.status, "Partially Paid")
    
    def test_to_dict(self):
        result = self.bill.to_dict()
        self.assertEqual(result['id'], "BIL001")
    
    def test_from_dict(self):
        data = {
            'id': 'BIL002',
            'patient_id': 'PAT002',
            'items': [],
            'total_amount': 1000,
            'paid_amount': 500,
            'status': 'Partially Paid',
            'created_date': '2024-03-01 10:00:00'
        }
        bill = Bill.from_dict(data)
        self.assertEqual(bill.id, "BIL002")


class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.data_manager = DataManager()
        self.data_manager.DATA_DIR = self.test_dir
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_save_and_load_data(self):
        test_data = [{'id': 1, 'name': 'Test'}]
        result = self.data_manager.save_data('test.json', test_data)
        self.assertTrue(result)
        
        loaded = self.data_manager.load_data('test.json')
        self.assertEqual(len(loaded), 1)
    
    def test_load_nonexistent_file(self):
        data = self.data_manager.load_data('nonexistent.json')
        self.assertEqual(data, [])
    
    def test_generate_id(self):
        id1 = self.data_manager.generate_id("PAT")
        id2 = self.data_manager.generate_id("PAT")
        self.assertTrue(id1.startswith("PAT_"))
        self.assertNotEqual(id1, id2)


class TestHospitalController(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.controller = HospitalController()
        self.controller.data_manager.DATA_DIR = self.test_dir
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_add_and_get_patient(self):
        patient_data = {
            'name': 'Test Patient',
            'phone': '0771234567',
            'email': 'test@email.com',
            'address': 'Test Address',
            'dob': '1990-01-01',
            'blood_group': 'O+',
            'emergency_contact': '0777654321'
        }
        patient = self.controller.add_patient(patient_data)
        self.assertIsNotNone(patient)
        
        retrieved = self.controller.get_patient(patient.id)
        self.assertEqual(retrieved.name, 'Test Patient')
    
    def test_update_patient(self):
        patient_data = {
            'name': 'Original',
            'phone': '0771234567',
            'email': 'test@email.com',
            'address': 'Address',
            'dob': '1990-01-01',
            'blood_group': 'O+',
            'emergency_contact': '0777654321'
        }
        patient = self.controller.add_patient(patient_data)
        
        result = self.controller.update_patient(patient.id, {'name': 'Updated'})
        self.assertTrue(result)
        
        updated = self.controller.get_patient(patient.id)
        self.assertEqual(updated.name, 'Updated')
    
    def test_delete_patient(self):
        patient_data = {
            'name': 'Delete Me',
            'phone': '0771234567',
            'email': 'delete@email.com',
            'address': 'Address',
            'dob': '1990-01-01',
            'blood_group': 'O+',
            'emergency_contact': '0777654321'
        }
        patient = self.controller.add_patient(patient_data)
        
        result = self.controller.delete_patient(patient.id)
        self.assertTrue(result)
        self.assertIsNone(self.controller.get_patient(patient.id))
    
    def test_add_and_get_doctor(self):
        doctor_data = {
            'name': 'Dr. Test',
            'phone': '0771234567',
            'email': 'dr@hospital.com',
            'address': 'Hospital',
            'specialization': 'Cardiology',
            'qualification': 'MBBS',
            'experience': 5,
            'consultation_fee': 1000.00
        }
        doctor = self.controller.add_doctor(doctor_data)
        self.assertIsNotNone(doctor)
        
        retrieved = self.controller.get_doctor(doctor.id)
        self.assertEqual(retrieved.name, 'Dr. Test')
    
    def test_add_and_get_appointment(self):
        patient_data = {
            'name': 'Appt Patient',
            'phone': '0771234567',
            'email': 'appt@email.com',
            'address': 'Address',
            'dob': '1990-01-01',
            'blood_group': 'O+',
            'emergency_contact': '0777654321'
        }
        patient = self.controller.add_patient(patient_data)
        
        doctor_data = {
            'name': 'Dr. Appt',
            'phone': '0771234567',
            'email': 'drappt@hospital.com',
            'address': 'Address',
            'specialization': 'Cardiology',
            'qualification': 'MBBS',
            'experience': 5,
            'consultation_fee': 1000.00
        }
        doctor = self.controller.add_doctor(doctor_data)
        
        appointment_data = {
            'patient_id': patient.id,
            'doctor_id': doctor.id,
            'date': '2024-03-20',
            'time': '10:00',
            'reason': 'Checkup'
        }
        appointment = self.controller.add_appointment(appointment_data)
        self.assertIsNotNone(appointment)
    
    def test_add_treatment(self):
        patient_data = {
            'name': 'Treatment Patient',
            'phone': '0771234567',
            'email': 'treatment@email.com',
            'address': 'Address',
            'dob': '1990-01-01',
            'blood_group': 'O+',
            'emergency_contact': '0777654321'
        }
        patient = self.controller.add_patient(patient_data)
        
        doctor_data = {
            'name': 'Dr. Treatment',
            'phone': '0771234567',
            'email': 'drtreat@hospital.com',
            'address': 'Address',
            'specialization': 'Cardiology',
            'qualification': 'MBBS',
            'experience': 5,
            'consultation_fee': 1000.00
        }
        doctor = self.controller.add_doctor(doctor_data)
        
        treatment_data = {
            'patient_id': patient.id,
            'doctor_id': doctor.id,
            'diagnosis': 'Cold',
            'prescription': 'Medicine',
            'notes': 'Rest',
            'cost': 500.00
        }
        treatment = self.controller.add_treatment(treatment_data)
        self.assertIsNotNone(treatment)
    
    def test_get_nonexistent_patient(self):
        patient = self.controller.get_patient("NONEXISTENT")
        self.assertIsNone(patient)


def run_all_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestPersonModel))
    suite.addTests(loader.loadTestsFromTestCase(TestPatientModel))
    suite.addTests(loader.loadTestsFromTestCase(TestDoctorModel))
    suite.addTests(loader.loadTestsFromTestCase(TestAppointmentModel))
    suite.addTests(loader.loadTestsFromTestCase(TestTreatmentModel))
    suite.addTests(loader.loadTestsFromTestCase(TestBillModel))
    suite.addTests(loader.loadTestsFromTestCase(TestDataManager))
    suite.addTests(loader.loadTestsFromTestCase(TestHospitalController))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print("UNIT TEST SUMMARY")
    print("=" * 60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL UNIT TESTS PASSED!")
    else:
        print("\n❌ Some unit tests failed.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_all_tests()