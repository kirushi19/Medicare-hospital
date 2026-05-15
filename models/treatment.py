from datetime import datetime

class Treatment:
    """Treatment class (Single Responsibility Principle)"""
    
    def __init__(self, treatment_id, patient_id, doctor_id, diagnosis, prescription, notes, cost):
        self._id = treatment_id
        self._patient_id = patient_id
        self._doctor_id = doctor_id
        self._diagnosis = diagnosis
        self._prescription = prescription
        self._notes = notes
        self._cost = cost
        self._date = datetime.now().strftime("%Y-%m-%d")
        self._time = datetime.now().strftime("%H:%M:%S")
    
    @property
    def id(self):
        return self._id
    
    @property
    def patient_id(self):
        return self._patient_id
    
    @property
    def doctor_id(self):
        return self._doctor_id
    
    @property
    def diagnosis(self):
        return self._diagnosis
    
    @property
    def prescription(self):
        return self._prescription
    
    @property
    def notes(self):
        return self._notes
    
    @property
    def cost(self):
        return self._cost
    
    @property
    def date(self):
        return self._date
    
    @property
    def time(self):
        return self._time
    
    def get_details(self):
        return {
            'ID': self.id,
            'Patient ID': self.patient_id,
            'Doctor ID': self.doctor_id,
            'Date': self.date,
            'Diagnosis': self.diagnosis,
            'Cost': f"Rs. {self.cost}"
        }
    
    def to_dict(self):
        return {
            'id': self._id,
            'patient_id': self._patient_id,
            'doctor_id': self._doctor_id,
            'diagnosis': self._diagnosis,
            'prescription': self._prescription,
            'notes': self._notes,
            'cost': self._cost,
            'date': self._date,
            'time': self._time
        }
    
    @classmethod
    def from_dict(cls, data):
        treatment = cls(
            data['id'],
            data['patient_id'],
            data['doctor_id'],
            data['diagnosis'],
            data['prescription'],
            data['notes'],
            data['cost']
        )
        treatment._date = data['date']
        treatment._time = data['time']
        return treatment