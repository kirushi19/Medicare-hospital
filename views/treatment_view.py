import tkinter as tk
from tkinter import ttk, messagebox
from utils.theme import PremiumTheme

class TreatmentView:
    """Treatment recording view with full CRUD operations"""
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.selected_treatment_id = None
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
            text="💊 Record Treatment",
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
        
        # Diagnosis
        tk.Label(
            fields_frame,
            text="Diagnosis *",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.diagnosis_entry = tk.Entry(
            fields_frame,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1
        )
        self.diagnosis_entry.pack(fill='x', ipady=8)
        
        # Prescription
        tk.Label(
            fields_frame,
            text="Prescription *",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.prescription_text = tk.Text(
            fields_frame,
            font=("Segoe UI", 11),
            height=4,
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1
        )
        self.prescription_text.pack(fill='x', ipady=5)
        
        # Notes
        tk.Label(
            fields_frame,
            text="Additional Notes",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.notes_text = tk.Text(
            fields_frame,
            font=("Segoe UI", 11),
            height=3,
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1
        )
        self.notes_text.pack(fill='x', ipady=5)
        
        # Cost
        tk.Label(
            fields_frame,
            text="Treatment Cost (Rs.) *",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.cost_entry = tk.Entry(
            fields_frame,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1
        )
        self.cost_entry.pack(fill='x', ipady=8)
        
        # ===== BUTTONS - VISIBLE NOW =====
        button_frame = tk.Frame(form_content, bg=PremiumTheme.CARD_BG)
        button_frame.pack(fill='x', padx=20, pady=30)
        
        # ADD TREATMENT BUTTON - GREEN
        self.add_btn = tk.Button(
            button_frame,
            text="➕ RECORD TREATMENT",
            font=("Segoe UI", 14, "bold"),
            bg=PremiumTheme.SUCCESS,
            fg='white',
            activebackground=PremiumTheme.SUCCESS,
            activeforeground='white',
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            height=2,
            command=self.add_treatment
        )
        self.add_btn.pack(fill='x', pady=5)
        
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
        # Create notebook for tabs
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: All Treatments
        self.all_frame = tk.Frame(self.notebook, bg=PremiumTheme.CARD_BG)
        self.notebook.add(self.all_frame, text='All Treatments')
        self.setup_all_treatments_tab()
        
        # Tab 2: Patient History
        self.history_frame = tk.Frame(self.notebook, bg=PremiumTheme.CARD_BG)
        self.notebook.add(self.history_frame, text='Patient History')
        self.setup_patient_history_tab()
    
    def setup_all_treatments_tab(self):
        """Setup all treatments tab"""
        # Search bar
        search_frame = tk.Frame(self.all_frame, bg=PremiumTheme.CARD_BG)
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
        self.search_entry.bind('<KeyRelease>', self.search_treatments)
        
        # Treeview
        tree_frame = tk.Frame(self.all_frame, bg=PremiumTheme.CARD_BG)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Patient', 'Doctor', 'Date', 'Diagnosis', 'Cost'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15
        )
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Define headings
        self.tree.heading('ID', text='Treatment ID')
        self.tree.heading('Patient', text='Patient')
        self.tree.heading('Doctor', text='Doctor')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Diagnosis', text='Diagnosis')
        self.tree.heading('Cost', text='Cost (Rs.)')
        
        # Set column widths
        self.tree.column('ID', width=150)
        self.tree.column('Patient', width=150)
        self.tree.column('Doctor', width=150)
        self.tree.column('Date', width=100)
        self.tree.column('Diagnosis', width=200)
        self.tree.column('Cost', width=100)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def setup_patient_history_tab(self):
        """Setup patient history tab"""
        # Patient selection
        select_frame = tk.Frame(self.history_frame, bg=PremiumTheme.CARD_BG)
        select_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            select_frame,
            text="Select Patient:",
            font=("Segoe UI", 11, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left', padx=(0, 10))
        
        self.history_patient_combo = ttk.Combobox(
            select_frame,
            font=("Segoe UI", 11),
            state='readonly',
            width=40
        )
        self.history_patient_combo.pack(side='left')
        self.history_patient_combo.bind('<<ComboboxSelected>>', self.load_patient_history)
        
        # Treeview for patient history
        tree_frame = tk.Frame(self.history_frame, bg=PremiumTheme.CARD_BG)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.history_tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Date', 'Doctor', 'Diagnosis', 'Cost'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15
        )
        
        vsb.config(command=self.history_tree.yview)
        hsb.config(command=self.history_tree.xview)
        
        # Define headings
        self.history_tree.heading('ID', text='Treatment ID')
        self.history_tree.heading('Date', text='Date')
        self.history_tree.heading('Doctor', text='Doctor')
        self.history_tree.heading('Diagnosis', text='Diagnosis')
        self.history_tree.heading('Cost', text='Cost (Rs.)')
        
        # Set column widths
        self.history_tree.column('ID', width=150)
        self.history_tree.column('Date', width=100)
        self.history_tree.column('Doctor', width=150)
        self.history_tree.column('Diagnosis', width=250)
        self.history_tree.column('Cost', width=100)
        
        # Grid layout
        self.history_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def load_data(self):
        """Load all data"""
        # Load patients
        patients = self.controller.get_all_patients()
        self.patient_dict = {f"{p.name} ({p.id})": p.id for p in patients}
        self.patient_combo['values'] = list(self.patient_dict.keys())
        self.history_patient_combo['values'] = list(self.patient_dict.keys())
        
        # Load doctors
        doctors = self.controller.get_all_doctors()
        self.doctor_dict = {f"Dr. {p.name} ({p.id})": p.id for p in doctors}
        self.doctor_combo['values'] = list(self.doctor_dict.keys())
        
        # Load treatments
        self.load_treatments()
    
    def load_treatments(self):
        """Load all treatments"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        patients = {p.id: p.name for p in self.controller.get_all_patients()}
        doctors = {d.id: f"Dr. {d.name}" for d in self.controller.get_all_doctors()}
        
        treatments = self.controller.get_all_treatments()
        for treatment in treatments:
            patient_name = patients.get(treatment.patient_id, "Unknown")
            doctor_name = doctors.get(treatment.doctor_id, "Unknown")
            
            self.tree.insert('', 'end', values=(
                treatment.id,
                patient_name,
                doctor_name,
                treatment.date,
                treatment.diagnosis[:30] + "..." if len(treatment.diagnosis) > 30 else treatment.diagnosis,
                f"Rs. {treatment.cost}"
            ), tags=(treatment.id,))
    
    def search_treatments(self, event=None):
        """Search treatments"""
        search_term = self.search_entry.get().lower()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        patients = {p.id: p.name for p in self.controller.get_all_patients()}
        doctors = {d.id: f"Dr. {d.name}" for d in self.controller.get_all_doctors()}
        
        treatments = self.controller.get_all_treatments()
        for treatment in treatments:
            patient_name = patients.get(treatment.patient_id, "Unknown")
            doctor_name = doctors.get(treatment.doctor_id, "Unknown")
            
            if (search_term in patient_name.lower() or 
                search_term in treatment.diagnosis.lower()):
                self.tree.insert('', 'end', values=(
                    treatment.id,
                    patient_name,
                    doctor_name,
                    treatment.date,
                    treatment.diagnosis[:30] + "..." if len(treatment.diagnosis) > 30 else treatment.diagnosis,
                    f"Rs. {treatment.cost}"
                ), tags=(treatment.id,))
    
    def load_patient_history(self, event=None):
        """Load patient history"""
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        selection = self.history_patient_combo.get()
        if not selection:
            return
        
        patient_id = self.patient_dict[selection]
        treatments = self.controller.get_patient_treatments(patient_id)
        
        doctors = {d.id: f"Dr. {d.name}" for d in self.controller.get_all_doctors()}
        
        for treatment in treatments:
            doctor_name = doctors.get(treatment.doctor_id, "Unknown")
            
            self.history_tree.insert('', 'end', values=(
                treatment.id,
                treatment.date,
                doctor_name,
                treatment.diagnosis,
                f"Rs. {treatment.cost}"
            ), tags=(treatment.id,))
    
    def add_treatment(self):
        """Add new treatment"""
        try:
            if not self.patient_combo.get():
                messagebox.showerror("Error", "Please select a patient!")
                return
            if not self.doctor_combo.get():
                messagebox.showerror("Error", "Please select a doctor!")
                return
            if not self.diagnosis_entry.get().strip():
                messagebox.showerror("Error", "Please enter diagnosis!")
                return
            if not self.cost_entry.get().strip():
                messagebox.showerror("Error", "Please enter cost!")
                return
            
            treatment_data = {
                'patient_id': self.patient_dict[self.patient_combo.get()],
                'doctor_id': self.doctor_dict[self.doctor_combo.get()],
                'diagnosis': self.diagnosis_entry.get().strip(),
                'prescription': self.prescription_text.get('1.0', 'end-1c').strip(),
                'notes': self.notes_text.get('1.0', 'end-1c').strip(),
                'cost': float(self.cost_entry.get())
            }
            
            treatment = self.controller.add_treatment(treatment_data)
            
            if treatment:
                messagebox.showinfo("Success", f"Treatment recorded!\nID: {treatment.id}")
                self.load_treatments()
                self.clear_form()
            else:
                messagebox.showerror("Error", "Failed to record treatment")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for cost")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def clear_form(self):
        """Clear form"""
        self.patient_combo.set('')
        self.doctor_combo.set('')
        self.diagnosis_entry.delete(0, 'end')
        self.prescription_text.delete('1.0', 'end')
        self.notes_text.delete('1.0', 'end')
        self.cost_entry.delete(0, 'end')