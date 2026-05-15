import json
import os
from datetime import datetime

class DataManager:
    """Manages data persistence (Dependency Inversion Principle)"""
    
    DATA_DIR = "data"
    
    def __init__(self):
        # Create data directory if it doesn't exist
        if not os.path.exists(self.DATA_DIR):
            os.makedirs(self.DATA_DIR)
    
    def save_data(self, filename, data):
        """Save data to JSON file"""
        filepath = os.path.join(self.DATA_DIR, filename)
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load_data(self, filename):
        """Load data from JSON file"""
        filepath = os.path.join(self.DATA_DIR, filename)
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading data: {e}")
            return []
    
    def generate_id(self, prefix):
        """Generate a unique ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{prefix}_{timestamp}"