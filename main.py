import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add the project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers.hospital_controller import HospitalController
from views.login_view import LoginView
from views.main_window import MainWindow
from utils.theme import PremiumTheme
from utils.animations import Animations

class MediCareHospitalApp:
    """Main application class"""
    
    def __init__(self):
        self.controller = None
        self.main_window = None
    
    def run(self):
        """Start the application"""
        try:
            # Initialize controller first
            self.controller = HospitalController()
            # Show login screen
            login = LoginView(self.on_login_success)
            login.run()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize: {str(e)}")
    
    def on_login_success(self):
        """Handle successful login"""
        try:
            # Show main window
            self.main_window = MainWindow(self.controller)
            self.main_window.run()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open main window: {str(e)}")

def main():
    """Entry point"""
    try:
        app = MediCareHospitalApp()
        app.run()
    except Exception as e:
        # Show error message
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")
        root.destroy()

if __name__ == "__main__":
    main()