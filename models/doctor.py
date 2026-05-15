from models.person import Person

class Doctor(Person):
    """Doctor class inheriting from Person (Single Responsibility Principle)"""
    
    def __init__(self, doctor_id, name, phone, email, address, specialization, qualification, experience, consultation_fee):
        super().__init__(doctor_id, name, phone, email, address)
        self._specialization = specialization
        self._qualification = qualification
        self._experience = experience
        self._consultation_fee = consultation_fee
        self._availability = []  # List of available time slots
        self._appointments = []
    
    @property
    def specialization(self):
        return self._specialization
    
    @specialization.setter
    def specialization(self, value):
        self._specialization = value
    
    @property
    def qualification(self):
        return self._qualification
    
    @property
    def experience(self):
        return self._experience
    
    @property
    def consultation_fee(self):
        return self._consultation_fee
    
    @consultation_fee.setter
    def consultation_fee(self, value):
        self._consultation_fee = value
    
    @property
    def availability(self):
        return self._availability
    
    def add_availability(self, day, time_slot):
        self._availability.append({'day': day, 'time': time_slot})
    
    def add_appointment(self, appointment_id):
        self._appointments.append(appointment_id)
    
    def get_details(self):
        """Implementation of abstract method"""
        return {
            'ID': self.id,
            'Name': self.name,
            'Specialization': self.specialization,
            'Qualification': self.qualification,
            'Experience': f"{self.experience} years",
            'Fee': f"Rs. {self.consultation_fee}",
            'Phone': self.phone
        }
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'specialization': self._specialization,
            'qualification': self._qualification,
            'experience': self._experience,
            'consultation_fee': self._consultation_fee,
            'availability': self._availability,
            'appointments': self._appointments
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        doctor = cls(
            data['id'],
            data['name'],
            data['phone'],
            data['email'],
            data['address'],
            data['specialization'],
            data['qualification'],
            data['experience'],
            data['consultation_fee']
        )
        doctor._availability = data.get('availability', [])
        doctor._appointments = data.get('appointments', [])
        return doctor