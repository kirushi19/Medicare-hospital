from datetime import datetime

class Appointment:
    """Appointment class (Single Responsibility Principle)"""
    
    STATUS_PENDING = "Pending"
    STATUS_CONFIRMED = "Confirmed"
    STATUS_COMPLETED = "Completed"
    STATUS_CANCELLED = "Cancelled"
    
    def __init__(self, appointment_id, patient_id, doctor_id, date, time, reason):
        self._id = appointment_id
        self._patient_id = patient_id
        self._doctor_id = doctor_id
        self._date = date
        self._time = time
        self._reason = reason
        self._status = self.STATUS_PENDING
        self._created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
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
    def date(self):
        return self._date
    
    @date.setter
    def date(self, value):
        self._date = value
    
    @property
    def time(self):
        return self._time
    
    @time.setter
    def time(self, value):
        self._time = value
    
    @property
    def reason(self):
        return self._reason
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        self._status = value
    
    @property
    def created_date(self):
        return self._created_date
    
    def confirm(self):
        self._status = self.STATUS_CONFIRMED
    
    def complete(self):
        self._status = self.STATUS_COMPLETED
    
    def cancel(self):
        self._status = self.STATUS_CANCELLED
    
    def get_details(self):
        return {
            'ID': self.id,
            'Patient ID': self.patient_id,
            'Doctor ID': self.doctor_id,
            'Date': self.date,
            'Time': self.time,
            'Reason': self.reason,
            'Status': self.status
        }
    
    def to_dict(self):
        return {
            'id': self._id,
            'patient_id': self._patient_id,
            'doctor_id': self._doctor_id,
            'date': self._date,
            'time': self._time,
            'reason': self._reason,
            'status': self._status,
            'created_date': self._created_date
        }
    
    @classmethod
    def from_dict(cls, data):
        appointment = cls(
            data['id'],
            data['patient_id'],
            data['doctor_id'],
            data['date'],
            data['time'],
            data['reason']
        )
        appointment._status = data['status']
        appointment._created_date = data['created_date']
        return appointment