from abc import ABC, abstractmethod
from datetime import datetime

class Person(ABC):
    """Base class for all persons in the system (Open/Closed Principle)"""
    
    def __init__(self, person_id, name, phone, email, address):
        self._id = person_id
        self._name = name
        self._phone = phone
        self._email = email
        self._address = address
        self._created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Getters and Setters (Encapsulation)
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, value):
        self._phone = value
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        self._email = value
    
    @property
    def address(self):
        return self._address
    
    @address.setter
    def address(self, value):
        self._address = value
    
    @property
    def created_date(self):
        return self._created_date
    
    @abstractmethod
    def get_details(self):
        """Abstract method to be implemented by subclasses"""
        pass
    
    def to_dict(self):
        """Convert object to dictionary for storage"""
        return {
            'id': self._id,
            'name': self._name,
            'phone': self._phone,
            'email': self._email,
            'address': self._address,
            'created_date': self._created_date
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create object from dictionary"""
        return cls(
            data['id'],
            data['name'],
            data['phone'],
            data['email'],
            data['address']
        )