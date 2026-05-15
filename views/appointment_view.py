import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from utils.theme import PremiumTheme

class AppointmentView:
    """Appointment management view with full CRUD operations"""
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.selected_appointment_id = None
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.parent, bg=PremiumTheme.BACKGROUND)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Split into left (form) and right (list)
        left_frame = tk.Frame(main_container, bg=PremiumTheme.CARD_BG, width=400)
        left_frame.pack(side='left', fill='both', padx=(0, 20))
        left_frame.pack_propagate(False)
        
        right_frame = tk.Frame(main_container, bg=PremiumTheme.CARD_BG)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # ========== LEFT FRAME - FORM ==========
        # Create a canvas with scrollbar for the form
        form_canvas = tk.Canvas(left_frame, bg=PremiumTheme.CARD_BG, highlightthickness=0)
        form_canvas.pack(side='left', fill='both', expand=True)
        
        form_scrollbar = ttk.Scrollbar(left_frame, orient='vertical', command=form_canvas.yview)
        form_scrollbar.pack(side='right', fill='y')
        
        form_canvas.configure(yscrollcommand=form_scrollbar.set)
        
        # Frame inside canvas for form content
        form_content = tk.Frame(form_canvas, bg=PremiumTheme.CARD_BG)
        form_canvas.create_window((0, 0), window=form_content, anchor='nw', width=380)
        
        def configure_form_scroll(event):
            form_canvas.configure(scrollregion=form_canvas.bbox('all'))
        
        form_content.bind('<Configure>', configure_form_scroll)
        
        # Form title
        form_title = tk.Label(
            form_content,
            text="📅 Schedule Appointment",
            font=("Segoe UI", 16, "bold"),
            fg=PremiumTheme.PRIMARY,
            bg=PremiumTheme.CARD_BG
        )
        form_title.pack(pady=20)
        
        # Form fields
        fields_frame = tk.Frame(form_content, bg=PremiumTheme.CARD_BG)
        fields_frame.pack(fill='x', padx=20, pady=10)
        
        # Patient Selection
        tk.Label(
            fields_frame,
            text="Select Patient *",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.patient_combo = ttk.Combobox(
            fields_frame,
            font=("Segoe UI", 11),
            state='readonly',
            height=10
        )
        self.patient_combo.pack(fill='x', ipady=5)
        
        # Doctor Selection
        tk.Label(
            fields_frame,
            text="Select Doctor *",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.doctor_combo = ttk.Combobox(
            fields_frame,
            font=("Segoe UI", 11),
            state='readonly',
            height=10
        )
        self.doctor_combo.pack(fill='x', ipady=5)
        
        # Date
        tk.Label(
            fields_frame,
            text="Date (YYYY-MM-DD) *",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.date_entry = tk.Entry(
            fields_frame,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1
        )
        self.date_entry.pack(fill='x', ipady=8)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Time
        tk.Label(
            fields_frame,
            text="Time (HH:MM) *",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.time_entry = tk.Entry(
            fields_frame,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1
        )
        self.time_entry.pack(fill='x', ipady=8)
        self.time_entry.insert(0, "09:00")
        
        # Reason
        tk.Label(
            fields_frame,
            text="Reason for Visit *",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.reason_text = tk.Text(
            fields_frame,
            font=("Segoe UI", 11),
            height=4,
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1
        )
        self.reason_text.pack(fill='x', ipady=5)
        
        # Status (for update)
        tk.Label(
            fields_frame,
            text="Status",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.status_combo = ttk.Combobox(
            fields_frame,
            values=['Pending', 'Confirmed', 'Completed', 'Cancelled'],
            font=("Segoe UI", 11),
            state='readonly'
        )
        self.status_combo.pack(fill='x', ipady=5)
        self.status_combo.set('Pending')
        
        # ===== BUTTONS - VISIBLE NOW =====
        button_frame = tk.Frame(form_content, bg=PremiumTheme.CARD_BG)
        button_frame.pack(fill='x', padx=20, pady=30)
        
        # ADD APPOINTMENT BUTTON - GREEN
        self.add_btn = tk.Button(
            button_frame,
            text="➕ SCHEDULE APPOINTMENT",
            font=("Segoe UI", 14, "bold"),
            bg=PremiumTheme.SUCCESS,
            fg='white',
            activebackground=PremiumTheme.SUCCESS,
            activeforeground='white',
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            height=2,
            command=self.add_appointment
        )
        self.add_btn.pack(fill='x', pady=5)
        
        # UPDATE BUTTON - YELLOW
        self.update_btn = tk.Button(
            button_frame,
            text="✏️ UPDATE STATUS",
            font=("Segoe UI", 14, "bold"),
            bg=PremiumTheme.WARNING,
            fg='white',
            activebackground=PremiumTheme.WARNING,
            activeforeground='white',
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            height=2,
            command=self.update_appointment,
            state='disabled'
        )
        self.update_btn.pack(fill='x', pady=5)
        
        # CLEAR BUTTON - GRAY
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑️ CLEAR FORM",
            font=("Segoe UI", 14, "bold"),
            bg=PremiumTheme.MEDIUM_GRAY,
            fg='white',
            activebackground=PremiumTheme.MEDIUM_GRAY,
            activeforeground='white',
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            height=2,
            command=self.clear_form
        )
        self.clear_btn.pack(fill='x', pady=5)
        
        # ========== RIGHT FRAME - LIST ==========
        list_title = tk.Label(
            right_frame,
            text="📋 Appointments",
            font=("Segoe UI", 16, "bold"),
            fg=PremiumTheme.PRIMARY,
            bg=PremiumTheme.CARD_BG
        )
        list_title.pack(pady=20)
        
        # Filter frame
        filter_frame = tk.Frame(right_frame, bg=PremiumTheme.CARD_BG)
        filter_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            filter_frame,
            text="Filter by Status:",
            font=("Segoe UI", 10),
            bg=PremiumTheme.CARD_BG,
            fg=PremiumTheme.MEDIUM_GRAY
        ).pack(side='left', padx=(0, 10))
        
        self.filter_combo = ttk.Combobox(
            filter_frame,
            values=['All', 'Pending', 'Confirmed', 'Completed', 'Cancelled'],
            font=("Segoe UI", 11),
            state='readonly',
            width=15
        )
        self.filter_combo.pack(side='left')
        self.filter_combo.set('All')
        self.filter_combo.bind('<<ComboboxSelected>>', self.filter_appointments)
        
        # Search bar
        search_frame = tk.Frame(right_frame, bg=PremiumTheme.CARD_BG)
        search_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            search_frame,
            text="🔍",
            font=("Segoe UI", 14),
            bg=PremiumTheme.CARD_BG,
            fg=PremiumTheme.MEDIUM_GRAY
        ).pack(side='left', padx=(0, 10))
        
        self.search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1
        )
        self.search_entry.pack(side='left', fill='x', expand=True, ipady=8)
        self.search_entry.bind('<KeyRelease>', self.search_appointments)
        
        # Treeview
        tree_frame = tk.Frame(right_frame, bg=PremiumTheme.CARD_BG)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Patient', 'Doctor', 'Date', 'Time', 'Reason', 'Status'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15
        )
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Define headings
        self.tree.heading('ID', text='Appointment ID')
        self.tree.heading('Patient', text='Patient')
        self.tree.heading('Doctor', text='Doctor')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Time', text='Time')
        self.tree.heading('Reason', text='Reason')
        self.tree.heading('Status', text='Status')
        
        # Set column widths
        self.tree.column('ID', width=150)
        self.tree.column('Patient', width=150)
        self.tree.column('Doctor', width=150)
        self.tree.column('Date', width=100)
        self.tree.column('Time', width=80)
        self.tree.column('Reason', width=200)
        self.tree.column('Status', width=100)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Configure tag colors for status
        self.tree.tag_configure('Pending', background='#fff3cd')
        self.tree.tag_configure('Confirmed', background='#d4edda')
        self.tree.tag_configure('Completed', background='#d1ecf1')
        self.tree.tag_configure('Cancelled', background='#f8d7da')
        
        # Bind selection
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # DELETE BUTTON
        self.delete_btn = tk.Button(
            right_frame,
            text="🗑️ DELETE APPOINTMENT",
            font=("Segoe UI", 14, "bold"),
            bg=PremiumTheme.DANGER,
            fg='white',
            activebackground=PremiumTheme.DANGER,
            activeforeground='white',
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            height=2,
            command=self.delete_appointment
        )
        self.delete_btn.pack(fill='x', padx=20, pady=10)
    
    def load_data(self):
        """Load all data"""
        patients = self.controller.get_all_patients()
        self.patient_dict = {f"{p.name} ({p.id})": p.id for p in patients}
        self.patient_combo['values'] = list(self.patient_dict.keys())
        
        doctors = self.controller.get_all_doctors()
        self.doctor_dict = {f"Dr. {p.name} ({p.id})": p.id for p in doctors}
        self.doctor_combo['values'] = list(self.doctor_dict.keys())
        
        self.load_appointments()
    
    def load_appointments(self):
        """Load all appointments"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        patients = {p.id: p.name for p in self.controller.get_all_patients()}
        doctors = {d.id: f"Dr. {d.name}" for d in self.controller.get_all_doctors()}
        
        appointments = self.controller.get_all_appointments()
        for apt in appointments:
            patient_name = patients.get(apt.patient_id, "Unknown")
            doctor_name = doctors.get(apt.doctor_id, "Unknown")
            
            self.tree.insert('', 'end', values=(
                apt.id,
                patient_name,
                doctor_name,
                apt.date,
                apt.time,
                apt.reason[:30] + "..." if len(apt.reason) > 30 else apt.reason,
                apt.status
            ), tags=(apt.status, apt.id))
    
    def filter_appointments(self, event=None):
        """Filter appointments"""
        filter_status = self.filter_combo.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        patients = {p.id: p.name for p in self.controller.get_all_patients()}
        doctors = {d.id: f"Dr. {d.name}" for d in self.controller.get_all_doctors()}
        
        appointments = self.controller.get_all_appointments()
        for apt in appointments:
            if filter_status == 'All' or apt.status == filter_status:
                patient_name = patients.get(apt.patient_id, "Unknown")
                doctor_name = doctors.get(apt.doctor_id, "Unknown")
                
                self.tree.insert('', 'end', values=(
                    apt.id,
                    patient_name,
                    doctor_name,
                    apt.date,
                    apt.time,
                    apt.reason[:30] + "..." if len(apt.reason) > 30 else apt.reason,
                    apt.status
                ), tags=(apt.status, apt.id))
    
    def search_appointments(self, event=None):
        """Search appointments"""
        search_term = self.search_entry.get().lower()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        patients = {p.id: p.name for p in self.controller.get_all_patients()}
        doctors = {d.id: f"Dr. {d.name}" for d in self.controller.get_all_doctors()}
        
        appointments = self.controller.get_all_appointments()
        for apt in appointments:
            patient_name = patients.get(apt.patient_id, "Unknown")
            doctor_name = doctors.get(apt.doctor_id, "Unknown")
            
            if (search_term in patient_name.lower() or 
                search_term in apt.reason.lower()):
                self.tree.insert('', 'end', values=(
                    apt.id,
                    patient_name,
                    doctor_name,
                    apt.date,
                    apt.time,
                    apt.reason[:30] + "..." if len(apt.reason) > 30 else apt.reason,
                    apt.status
                ), tags=(apt.status, apt.id))
    
    def add_appointment(self):
        """Add new appointment"""
        try:
            if not self.patient_combo.get():
                messagebox.showerror("Error", "Select a patient!")
                return
            if not self.doctor_combo.get():
                messagebox.showerror("Error", "Select a doctor!")
                return
            if not self.date_entry.get().strip():
                messagebox.showerror("Error", "Enter date!")
                return
            if not self.time_entry.get().strip():
                messagebox.showerror("Error", "Enter time!")
                return
            if not self.reason_text.get('1.0', 'end-1c').strip():
                messagebox.showerror("Error", "Enter reason!")
                return
            
            appointment_data = {
                'patient_id': self.patient_dict[self.patient_combo.get()],
                'doctor_id': self.doctor_dict[self.doctor_combo.get()],
                'date': self.date_entry.get().strip(),
                'time': self.time_entry.get().strip(),
                'reason': self.reason_text.get('1.0', 'end-1c').strip()
            }
            
            appointment = self.controller.add_appointment(appointment_data)
            
            if appointment:
                messagebox.showinfo("Success", f"Appointment scheduled!\nID: {appointment.id}")
                self.load_appointments()
                self.clear_form()
            else:
                messagebox.showerror("Error", "Failed to schedule")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def update_appointment(self):
        """Update appointment status"""
        if not self.selected_appointment_id:
            messagebox.showwarning("Warning", "Select an appointment!")
            return
        
        try:
            new_status = self.status_combo.get()
            if not new_status:
                messagebox.showerror("Error", "Select a status!")
                return
            
            if self.controller.update_appointment_status(self.selected_appointment_id, new_status):
                messagebox.showinfo("Success", "Status updated!")
                self.load_appointments()
                self.clear_form()
                self.update_btn.config(state='disabled')
            else:
                messagebox.showerror("Error", "Failed to update")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def delete_appointment(self):
        """Delete appointment"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select an appointment!")
            return
        
        if messagebox.askyesno("Confirm", "Delete this appointment?"):
            item = self.tree.item(selection[0])
            appointment_id = item['tags'][1]
            
            if self.controller.delete_appointment(appointment_id):
                messagebox.showinfo("Success", "Appointment deleted!")
                self.load_appointments()
                self.clear_form()
                self.update_btn.config(state='disabled')
    
    def clear_form(self):
        """Clear form"""
        self.patient_combo.set('')
        self.doctor_combo.set('')
        self.date_entry.delete(0, 'end')
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.time_entry.delete(0, 'end')
        self.time_entry.insert(0, "09:00")
        self.reason_text.delete('1.0', 'end')
        self.status_combo.set('Pending')
        
        self.selected_appointment_id = None
        self.update_btn.config(state='disabled')
    
    def on_select(self, event):
        """Handle selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.selected_appointment_id = item['tags'][1]
            current_status = item['tags'][0]
            
            self.status_combo.set(current_status)
            self.update_btn.config(state='normal')