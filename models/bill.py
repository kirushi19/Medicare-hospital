from datetime import datetime

class Bill:
    """Bill class (Single Responsibility Principle)"""
    
    STATUS_UNPAID = "Unpaid"
    STATUS_PAID = "Paid"
    STATUS_PARTIAL = "Partially Paid"
    
    def __init__(self, bill_id, patient_id):
        self._id = bill_id
        self._patient_id = patient_id
        self._items = []  # List of bill items
        self._total_amount = 0
        self._paid_amount = 0
        self._status = self.STATUS_UNPAID
        self._created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @property
    def id(self):
        return self._id
    
    @property
    def patient_id(self):
        return self._patient_id
    
    @property
    def items(self):
        return self._items
    
    @property
    def total_amount(self):
        return self._total_amount
    
    @property
    def paid_amount(self):
        return self._paid_amount
    
    @property
    def status(self):
        return self._status
    
    @property
    def created_date(self):
        return self._created_date
    
    def add_item(self, description, quantity, unit_price):
        """Add an item to the bill"""
        item = {
            'description': description,
            'quantity': quantity,
            'unit_price': unit_price,
            'total': quantity * unit_price
        }
        self._items.append(item)
        self._calculate_total()
    
    def _calculate_total(self):
        """Calculate total bill amount"""
        self._total_amount = sum(item['total'] for item in self._items)
        self._update_status()
    
    def make_payment(self, amount):
        """Process a payment"""
        self._paid_amount += amount
        self._update_status()
    
    def _update_status(self):
        """Update bill status based on payment"""
        if self._paid_amount >= self._total_amount:
            self._status = self.STATUS_PAID
        elif self._paid_amount > 0:
            self._status = self.STATUS_PARTIAL
        else:
            self._status = self.STATUS_UNPAID
    
    def get_details(self):
        return {
            'Bill ID': self.id,
            'Patient ID': self.patient_id,
            'Total Amount': f"Rs. {self.total_amount}",
            'Paid Amount': f"Rs. {self.paid_amount}",
            'Balance': f"Rs. {self.total_amount - self.paid_amount}",
            'Status': self.status,
            'Date': self.created_date
        }
    
    def to_dict(self):
        return {
            'id': self._id,
            'patient_id': self._patient_id,
            'items': self._items,
            'total_amount': self._total_amount,
            'paid_amount': self._paid_amount,
            'status': self._status,
            'created_date': self._created_date
        }
    
    @classmethod
    def from_dict(cls, data):
        bill = cls(data['id'], data['patient_id'])
        bill._items = data['items']
        bill._total_amount = data['total_amount']
        bill._paid_amount = data['paid_amount']
        bill._status = data['status']
        bill._created_date = data['created_date']
        return bill