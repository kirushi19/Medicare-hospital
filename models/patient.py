from models.person import Person

class Patient(Person):
    """Patient class inheriting from Person (Single Responsibility Principle)"""
    
    def __init__(self, patient_id, name, phone, email, address, date_of_birth, blood_group, emergency_contact):
        super().__init__(patient_id, name, phone, email, address)
        self._date_of_birth = date_of_birth
        self._blood_group = blood_group
        self._emergency_contact = emergency_contact
        self._medical_history = []
        self._appointments = []
    
    @property
    def date_of_birth(self):
        return self._date_of_birth
    
    @date_of_birth.setter
    def date_of_birth(self, value):
        self._date_of_birth = value
    
    @property
    def blood_group(self):
        return self._blood_group
    
    @blood_group.setter
    def blood_group(self, value):
        self._blood_group = value
    
    @property
    def emergency_contact(self):
        return self._emergency_contact
    
    @emergency_contact.setter
    def emergency_contact(self, value):
        self._emergency_contact = value
    
    @property
    def medical_history(self):
        return self._medical_history
    
    def add_medical_record(self, record):
        self._medical_history.append(record)
    
    def add_appointment(self, appointment_id):
        self._appointments.append(appointment_id)
    
    def get_details(self):
        """Implementation of abstract method"""
        return {
            'ID': self.id,
            'Name': self.name,
            'Phone': self.phone,
            'Email': self.email,
            'DOB': self.date_of_birth,
            'Blood Group': self.blood_group,
            'Emergency Contact': self.emergency_contact
        }
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'date_of_birth': self._date_of_birth,
            'blood_group': self._blood_group,
            'emergency_contact': self._emergency_contact,
            'medical_history': self._medical_history,
            'appointments': self._appointments
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        patient = cls(
            data['id'],
            data['name'],
            data['phone'],
            data['email'],
            data['address'],
            data['date_of_birth'],
            data['blood_group'],
            data['emergency_contact']
        )
        patient._medical_history = data.get('medical_history', [])
        patient._appointments = data.get('appointments', [])
        return patient