"""
Integration Testing for MediCare Hospital Management System
"""

import unittest
import sys
import os
import tempfile
import shutil
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.hospital_controller import HospitalController


class TestFullWorkflowIntegration(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.controller = HospitalController()
        self.controller.data_manager.DATA_DIR = self.test_dir
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def create_test_patient(self, name="John Doe"):
        patient_data = {
            'name': name,
            'phone': '0771234567',
            'email': f'{name.lower().replace(" ", ".")}@email.com',
            'address': '123 Main St, Colombo',
            'dob': '1985-05-15',
            'blood_group': 'O+',
            'emergency_contact': '0777654321'
        }
        return self.controller.add_patient(patient_data)
    
    def create_test_doctor(self, name="Dr. Sarah Johnson", specialization="Cardiology"):
        doctor_data = {
            'name': name,
            'phone': '0778888888',
            'email': f'{name.lower().replace(" ", ".")}@hospital.com',
            'address': 'Medical Center, Colombo',
            'specialization': specialization,
            'qualification': 'MBBS, MD',
            'experience': 12,
            'consultation_fee': 2500.00
        }
        return self.controller.add_doctor(doctor_data)
    
    def test_complete_patient_journey(self):
        print("\n=== Testing Complete Patient Journey ===")
        
        patient = self.create_test_patient("John Smith")
        self.assertIsNotNone(patient)
        print(f"✓ Patient registered: {patient.id}")
        
        doctor = self.create_test_doctor("Dr. Emily Brown", "Cardiology")
        self.assertIsNotNone(doctor)
        print(f"✓ Doctor registered: {doctor.id}")
        
        appointment_data = {
            'patient_id': patient.id,
            'doctor_id': doctor.id,
            'date': (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            'time': "10:30",
            'reason': "Chest pain"
        }
        appointment = self.controller.add_appointment(appointment_data)
        self.assertIsNotNone(appointment)
        print(f"✓ Appointment scheduled: {appointment.id}")
        
        self.controller.update_appointment_status(appointment.id, "Confirmed")
        confirmed = self.controller.get_appointment(appointment.id)
        self.assertEqual(confirmed.status, "Confirmed")
        print("✓ Appointment confirmed")
        
        treatment_data = {
            'patient_id': patient.id,
            'doctor_id': doctor.id,
            'diagnosis': "Acute Bronchitis",
            'prescription': "Amoxicillin 500mg",
            'notes': "Follow up in 1 week",
            'cost': 2500.00
        }
        treatment = self.controller.add_treatment(treatment_data)
        self.assertIsNotNone(treatment)
        print(f"✓ Treatment recorded: {treatment.id}")
        
        bills = self.controller.get_patient_bills(patient.id)
        self.assertEqual(len(bills), 1)
        print(f"✓ Bill created: Rs. {bills[0].total_amount}")
        
        self.controller.make_payment(bills[0].id, 2500.00)
        final_bill = self.controller.bills[bills[0].id]
        self.assertEqual(final_bill.status, "Paid")
        print("✓ Payment completed")
        
        self.controller.update_appointment_status(appointment.id, "Completed")
        print("✓ Appointment completed")
        
        print("\nComplete patient journey test PASSED!")
    
    def test_multiple_doctor_consultations(self):
        print("\n=== Testing Multiple Doctor Consultations ===")
        
        patient = self.create_test_patient("Robert Wilson")
        print(f"Patient: {patient.name}")
        
        doctors = []
        specialties = [
            ("Dr. James Wilson", "Cardiology", 2500),
            ("Dr. Maria Garcia", "Neurology", 2800),
            ("Dr. David Chen", "Orthopedics", 2200)
        ]
        
        for name, spec, fee in specialties:
            doctor = self.create_test_doctor(name, spec)
            doctors.append(doctor)
            print(f"  Doctor: {doctor.name}")
        
        for i, doctor in enumerate(doctors):
            appointment_data = {
                'patient_id': patient.id,
                'doctor_id': doctor.id,
                'date': (datetime.now() + timedelta(days=i+1)).strftime("%Y-%m-%d"),
                'time': f"{10 + i}:00",
                'reason': f"Consultation for {doctor.specialization}"
            }
            appointment = self.controller.add_appointment(appointment_data)
            self.controller.update_appointment_status(appointment.id, "Confirmed")
        
        total_cost = 0
        for doctor in doctors:
            treatment_data = {
                'patient_id': patient.id,
                'doctor_id': doctor.id,
                'diagnosis': f"{doctor.specialization} consultation",
                'prescription': "Prescribed medication",
                'notes': "Follow up",
                'cost': doctor.consultation_fee * 1.2
            }
            treatment = self.controller.add_treatment(treatment_data)
            total_cost += treatment.cost
            print(f"  Treatment from Dr. {doctor.name}: Rs. {treatment.cost}")
        
        bills = self.controller.get_patient_bills(patient.id)
        self.assertEqual(len(bills), 1)
        print(f"✓ Total bill: Rs. {total_cost}")
        
        self.controller.make_payment(bills[0].id, total_cost)
        print("✓ Payment completed")
        
        print("\nMultiple doctor consultations test PASSED!")
    
    def test_data_persistence(self):
        print("\n=== Testing Data Persistence ===")
        
        patient = self.create_test_patient("Persist Patient")
        doctor = self.create_test_doctor("Dr. Persist", "Cardiology")
        
        appointment_data = {
            'patient_id': patient.id,
            'doctor_id': doctor.id,
            'date': '2024-03-20',
            'time': '10:00',
            'reason': 'Checkup'
        }
        appointment = self.controller.add_appointment(appointment_data)
        
        treatment_data = {
            'patient_id': patient.id,
            'doctor_id': doctor.id,
            'diagnosis': 'Test',
            'prescription': 'Medicine',
            'notes': 'Notes',
            'cost': 1000.00
        }
        treatment = self.controller.add_treatment(treatment_data)
        
        print(f"✓ Added: Patient, Doctor, Appointment, Treatment")
        
        new_controller = HospitalController()
        new_controller.data_manager.DATA_DIR = self.test_dir
        new_controller.load_all_data()
        
        loaded_patient = new_controller.get_patient(patient.id)
        self.assertIsNotNone(loaded_patient)
        self.assertEqual(loaded_patient.name, patient.name)
        
        loaded_appointment = new_controller.get_appointment(appointment.id)
        self.assertIsNotNone(loaded_appointment)
        
        print("✓ All data loaded successfully")
        print("\nData persistence test PASSED!")


def run_integration_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestFullWorkflowIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\nALL INTEGRATION TESTS PASSED!")
    else:
        print("\nSome integration tests failed.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_integration_tests()



def test_unique_patient_ids(self):
    id1 = data_manager.generate_id("PAT")
    id2 = data_manager.generate_id("PAT")

    self.assertNotEqual(id1, id2)