import tkinter as tk
from tkinter import ttk, messagebox
from utils.theme import PremiumTheme
from datetime import datetime

class BillingView:
    """Billing management view with full CRUD operations"""
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.selected_bill_id = None
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.parent, bg=PremiumTheme.BACKGROUND)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Split into left (form) and right (list)
        left_frame = tk.Frame(main_container, bg=PremiumTheme.CARD_BG, width=500)
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
        form_canvas.create_window((0, 0), window=form_content, anchor='nw', width=480)
        
        def configure_form_scroll(event):
            form_canvas.configure(scrollregion=form_canvas.bbox('all'))
        
        form_content.bind('<Configure>', configure_form_scroll)
        
        # Form title
        form_title = tk.Label(
            form_content,
            text="💰 Create New Bill",
            font=("Segoe UI", 20, "bold"),
            fg=PremiumTheme.PRIMARY,
            bg=PremiumTheme.CARD_BG
        )
        form_title.pack(pady=20)
        
        # Form fields
        fields_frame = tk.Frame(form_content, bg=PremiumTheme.CARD_BG)
        fields_frame.pack(fill='x', padx=20, pady=5)
        
        # Patient Selection
        tk.Label(
            fields_frame,
            text="Select Patient *",
            font=("Segoe UI", 12, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(5, 5))
        
        self.patient_combo = ttk.Combobox(
            fields_frame,
            font=("Segoe UI", 11),
            state='readonly',
            height=10
        )
        self.patient_combo.pack(fill='x', ipady=5)
        
        # Bill Date
        tk.Label(
            fields_frame,
            text="Bill Date",
            font=("Segoe UI", 12, "bold"),
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
        self.date_entry.config(state='readonly')
        
        # ===== DOCTOR CONSULTATION FEE =====
        fee_section = tk.LabelFrame(
            fields_frame,
            text=" Doctor Consultation ",
            font=("Segoe UI", 12, "bold"),
            fg=PremiumTheme.PRIMARY,
            bg=PremiumTheme.CARD_BG,
            relief='solid',
            borderwidth=1
        )
        fee_section.pack(fill='x', pady=15)
        
        # Doctor Selection
        tk.Label(
            fee_section,
            text="Select Doctor",
            font=("Segoe UI", 11),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', padx=10, pady=(10, 5))
        
        self.doctor_combo = ttk.Combobox(
            fee_section,
            font=("Segoe UI", 11),
            state='readonly',
            height=10
        )
        self.doctor_combo.pack(fill='x', padx=10, ipady=5)
        self.doctor_combo.bind('<<ComboboxSelected>>', self.on_doctor_select)
        
        # Consultation Fee
        fee_frame = tk.Frame(fee_section, bg=PremiumTheme.CARD_BG)
        fee_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            fee_frame,
            text="Consultation Fee (Rs.):",
            font=("Segoe UI", 11),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left')
        
        self.consultation_fee_var = tk.StringVar()
        self.consultation_fee_entry = tk.Entry(
            fee_frame,
            textvariable=self.consultation_fee_var,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1,
            width=15
        )
        self.consultation_fee_entry.pack(side='right', ipady=5)
        self.consultation_fee_entry.bind('<KeyRelease>', self.calculate_total)
        
        # Include in bill checkbox
        self.include_consultation = tk.BooleanVar(value=True)
        tk.Checkbutton(
            fee_section,
            text="Include in bill",
            variable=self.include_consultation,
            bg=PremiumTheme.CARD_BG,
            fg=PremiumTheme.DARK,
            font=("Segoe UI", 10),
            command=self.calculate_total
        ).pack(anchor='w', padx=10, pady=(0, 10))
        
        # ===== HOSPITAL CHARGES =====
        hospital_section = tk.LabelFrame(
            fields_frame,
            text=" Hospital Charges ",
            font=("Segoe UI", 12, "bold"),
            fg=PremiumTheme.PRIMARY,
            bg=PremiumTheme.CARD_BG,
            relief='solid',
            borderwidth=1
        )
        hospital_section.pack(fill='x', pady=15)
        
        # Room Charges
        room_frame = tk.Frame(hospital_section, bg=PremiumTheme.CARD_BG)
        room_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            room_frame,
            text="Room Charges (Rs.):",
            font=("Segoe UI", 11),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left')
        
        self.room_charges_var = tk.StringVar()
        self.room_charges_entry = tk.Entry(
            room_frame,
            textvariable=self.room_charges_var,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1,
            width=15
        )
        self.room_charges_entry.pack(side='right', ipady=5)
        self.room_charges_entry.bind('<KeyRelease>', self.calculate_total)
        
        # Lab Charges
        lab_frame = tk.Frame(hospital_section, bg=PremiumTheme.CARD_BG)
        lab_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            lab_frame,
            text="Lab Charges (Rs.):",
            font=("Segoe UI", 11),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left')
        
        self.lab_charges_var = tk.StringVar()
        self.lab_charges_entry = tk.Entry(
            lab_frame,
            textvariable=self.lab_charges_var,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1,
            width=15
        )
        self.lab_charges_entry.pack(side='right', ipady=5)
        self.lab_charges_entry.bind('<KeyRelease>', self.calculate_total)
        
        # Pharmacy/Medicine Charges
        pharmacy_frame = tk.Frame(hospital_section, bg=PremiumTheme.CARD_BG)
        pharmacy_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            pharmacy_frame,
            text="Medicine Charges (Rs.):",
            font=("Segoe UI", 11),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left')
        
        self.pharmacy_charges_var = tk.StringVar()
        self.pharmacy_charges_entry = tk.Entry(
            pharmacy_frame,
            textvariable=self.pharmacy_charges_var,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1,
            width=15
        )
        self.pharmacy_charges_entry.pack(side='right', ipady=5)
        self.pharmacy_charges_entry.bind('<KeyRelease>', self.calculate_total)
        
        # Other Hospital Charges
        other_hospital_frame = tk.Frame(hospital_section, bg=PremiumTheme.CARD_BG)
        other_hospital_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            other_hospital_frame,
            text="Other Charges (Rs.):",
            font=("Segoe UI", 11),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left')
        
        self.other_hospital_var = tk.StringVar()
        self.other_hospital_entry = tk.Entry(
            other_hospital_frame,
            textvariable=self.other_hospital_var,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1,
            width=15
        )
        self.other_hospital_entry.pack(side='right', ipady=5)
        self.other_hospital_entry.bind('<KeyRelease>', self.calculate_total)
        
        # ===== TREATMENT FEES =====
        treatment_section = tk.LabelFrame(
            fields_frame,
            text=" Treatment Fees ",
            font=("Segoe UI", 12, "bold"),
            fg=PremiumTheme.PRIMARY,
            bg=PremiumTheme.CARD_BG,
            relief='solid',
            borderwidth=1
        )
        treatment_section.pack(fill='x', pady=15)
        
        # Procedure Fees
        procedure_frame = tk.Frame(treatment_section, bg=PremiumTheme.CARD_BG)
        procedure_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            procedure_frame,
            text="Procedure Fees (Rs.):",
            font=("Segoe UI", 11),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left')
        
        self.procedure_fee_var = tk.StringVar()
        self.procedure_fee_entry = tk.Entry(
            procedure_frame,
            textvariable=self.procedure_fee_var,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1,
            width=15
        )
        self.procedure_fee_entry.pack(side='right', ipady=5)
        self.procedure_fee_entry.bind('<KeyRelease>', self.calculate_total)
        
        # Surgery Fees
        surgery_frame = tk.Frame(treatment_section, bg=PremiumTheme.CARD_BG)
        surgery_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            surgery_frame,
            text="Surgery Fees (Rs.):",
            font=("Segoe UI", 11),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left')
        
        self.surgery_fee_var = tk.StringVar()
        self.surgery_fee_entry = tk.Entry(
            surgery_frame,
            textvariable=self.surgery_fee_var,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1,
            width=15
        )
        self.surgery_fee_entry.pack(side='right', ipady=5)
        self.surgery_fee_entry.bind('<KeyRelease>', self.calculate_total)
        
        # Therapy Fees
        therapy_frame = tk.Frame(treatment_section, bg=PremiumTheme.CARD_BG)
        therapy_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            therapy_frame,
            text="Therapy Fees (Rs.):",
            font=("Segoe UI", 11),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left')
        
        self.therapy_fee_var = tk.StringVar()
        self.therapy_fee_entry = tk.Entry(
            therapy_frame,
            textvariable=self.therapy_fee_var,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1,
            width=15
        )
        self.therapy_fee_entry.pack(side='right', ipady=5)
        self.therapy_fee_entry.bind('<KeyRelease>', self.calculate_total)
        
        # Other Treatment Fees
        other_treatment_frame = tk.Frame(treatment_section, bg=PremiumTheme.CARD_BG)
        other_treatment_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            other_treatment_frame,
            text="Other Treatment (Rs.):",
            font=("Segoe UI", 11),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left')
        
        self.other_treatment_var = tk.StringVar()
        self.other_treatment_entry = tk.Entry(
            other_treatment_frame,
            textvariable=self.other_treatment_var,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1,
            width=15
        )
        self.other_treatment_entry.pack(side='right', ipady=5)
        self.other_treatment_entry.bind('<KeyRelease>', self.calculate_total)
        
        # ===== ADDITIONAL CUSTOM ITEMS =====
        custom_section = tk.LabelFrame(
            fields_frame,
            text=" Custom Items ",
            font=("Segoe UI", 12, "bold"),
            fg=PremiumTheme.PRIMARY,
            bg=PremiumTheme.CARD_BG,
            relief='solid',
            borderwidth=1
        )
        custom_section.pack(fill='x', pady=15)
        
        # Items container with scrollbar for custom items
        items_container = tk.Frame(custom_section, bg=PremiumTheme.CARD_BG)
        items_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Headers
        header_frame = tk.Frame(items_container, bg=PremiumTheme.CARD_BG)
        header_frame.pack(fill='x', pady=5)
        
        tk.Label(header_frame, text="Description", font=("Segoe UI", 10, "bold"), 
                bg=PremiumTheme.CARD_BG, fg=PremiumTheme.DARK).pack(side='left', padx=(0, 40))
        tk.Label(header_frame, text="Qty", font=("Segoe UI", 10, "bold"), 
                bg=PremiumTheme.CARD_BG, fg=PremiumTheme.DARK).pack(side='left', padx=(0, 30))
        tk.Label(header_frame, text="Price", font=("Segoe UI", 10, "bold"), 
                bg=PremiumTheme.CARD_BG, fg=PremiumTheme.DARK).pack(side='left', padx=(0, 30))
        tk.Label(header_frame, text="Total", font=("Segoe UI", 10, "bold"), 
                bg=PremiumTheme.CARD_BG, fg=PremiumTheme.DARK).pack(side='left')
        
        # Canvas for scrolling custom items
        items_canvas = tk.Canvas(items_container, bg=PremiumTheme.CARD_BG, highlightthickness=0, height=120)
        items_canvas.pack(side='left', fill='both', expand=True)
        
        items_scrollbar = ttk.Scrollbar(items_container, orient='vertical', command=items_canvas.yview)
        items_scrollbar.pack(side='right', fill='y')
        
        items_canvas.configure(yscrollcommand=items_scrollbar.set)
        
        # Frame inside canvas for items
        self.items_frame = tk.Frame(items_canvas, bg=PremiumTheme.CARD_BG)
        items_canvas.create_window((0, 0), window=self.items_frame, anchor='nw', width=400)
        
        def configure_items_scroll(event):
            items_canvas.configure(scrollregion=items_canvas.bbox('all'))
        
        self.items_frame.bind('<Configure>', configure_items_scroll)
        
        # List to store custom item entries
        self.custom_item_entries = []
        
        # Add first custom item row
        self.add_custom_item_row()
        
        # Add Item Button
        add_item_btn = tk.Button(
            custom_section,
            text="➕ Add Custom Item",
            font=("Segoe UI", 10),
            bg=PremiumTheme.INFO,
            fg='white',
            activebackground=PremiumTheme.INFO,
            activeforeground='white',
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            command=self.add_custom_item_row
        )
        add_item_btn.pack(pady=5)
        
        # ===== TOTAL AMOUNT =====
        total_frame = tk.Frame(fields_frame, bg=PremiumTheme.CARD_BG, relief='solid', borderwidth=1)
        total_frame.pack(fill='x', pady=20, ipady=10)
        
        tk.Label(
            total_frame,
            text="TOTAL BILL AMOUNT:",
            font=("Segoe UI", 14, "bold"),
            fg=PremiumTheme.DARK,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left', padx=20)
        
        self.total_amount_label = tk.Label(
            total_frame,
            text="Rs. 0.00",
            font=("Segoe UI", 18, "bold"),
            fg=PremiumTheme.SUCCESS,
            bg=PremiumTheme.CARD_BG
        )
        self.total_amount_label.pack(side='right', padx=20)
        
        # ===== BUTTONS =====
        button_frame = tk.Frame(form_content, bg=PremiumTheme.CARD_BG)
        button_frame.pack(fill='x', padx=20, pady=20)
        
        # CREATE BILL BUTTON - GREEN
        self.create_btn = tk.Button(
            button_frame,
            text="💰 CREATE BILL",
            font=("Segoe UI", 16, "bold"),
            bg=PremiumTheme.SUCCESS,
            fg='white',
            activebackground=PremiumTheme.SUCCESS,
            activeforeground='white',
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            height=2,
            command=self.create_bill
        )
        self.create_btn.pack(fill='x', pady=5)
        
        # CLEAR BUTTON - GRAY
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑️ CLEAR FORM",
            font=("Segoe UI", 16, "bold"),
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
        
        # Tab 1: All Bills
        self.bills_frame = tk.Frame(self.notebook, bg=PremiumTheme.CARD_BG)
        self.notebook.add(self.bills_frame, text='💰 All Bills')
        self.setup_bills_tab()
        
        # Tab 2: Make Payment
        self.payment_frame = tk.Frame(self.notebook, bg=PremiumTheme.CARD_BG)
        self.notebook.add(self.payment_frame, text='💳 Make Payment')
        self.setup_payment_tab()
        
        # Tab 3: Patient Bills
        self.patient_frame = tk.Frame(self.notebook, bg=PremiumTheme.CARD_BG)
        self.notebook.add(self.patient_frame, text='👤 Patient Bills')
        self.setup_patient_bills_tab()
    
    def add_custom_item_row(self):
        """Add a new custom item row to the bill form"""
        row_frame = tk.Frame(self.items_frame, bg=PremiumTheme.CARD_BG)
        row_frame.pack(fill='x', pady=2)
        
        # Item Description
        desc_entry = tk.Entry(
            row_frame,
            font=("Segoe UI", 10),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1,
            width=18
        )
        desc_entry.pack(side='left', padx=(0, 5), ipady=3)
        
        # Quantity
        qty_entry = tk.Entry(
            row_frame,
            font=("Segoe UI", 10),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1,
            width=5
        )
        qty_entry.pack(side='left', padx=(0, 5), ipady=3)
        qty_entry.insert(0, "1")
        
        # Unit Price
        price_entry = tk.Entry(
            row_frame,
            font=("Segoe UI", 10),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1,
            width=8
        )
        price_entry.pack(side='left', padx=(0, 5), ipady=3)
        
        # Item Total Label
        item_total_label = tk.Label(
            row_frame,
            text="Rs. 0",
            font=("Segoe UI", 10),
            bg=PremiumTheme.CARD_BG,
            fg=PremiumTheme.DARK,
            width=10
        )
        item_total_label.pack(side='left', padx=(0, 5))
        
        # Remove button (only if more than one row)
        if len(self.custom_item_entries) > 0:
            remove_btn = tk.Button(
                row_frame,
                text="✖",
                font=("Segoe UI", 8, "bold"),
                bg=PremiumTheme.DANGER,
                fg='white',
                activebackground=PremiumTheme.DANGER,
                activeforeground='white',
                relief='flat',
                borderwidth=0,
                cursor='hand2',
                width=2,
                command=lambda: self.remove_custom_item_row(row_frame)
            )
            remove_btn.pack(side='left')
        
        # Bind events to update totals
        def update_item_total(event=None):
            try:
                qty = float(qty_entry.get()) if qty_entry.get() else 0
                price = float(price_entry.get()) if price_entry.get() else 0
                total = qty * price
                item_total_label.config(text=f"Rs. {total:.0f}")
                self.calculate_total()
            except ValueError:
                item_total_label.config(text="Rs. 0")
                self.calculate_total()
        
        qty_entry.bind('<KeyRelease>', update_item_total)
        price_entry.bind('<KeyRelease>', update_item_total)
        
        # Store entries
        self.custom_item_entries.append({
            'frame': row_frame,
            'desc': desc_entry,
            'qty': qty_entry,
            'price': price_entry,
            'total_label': item_total_label
        })
    
    def remove_custom_item_row(self, row_frame):
        """Remove a custom item row"""
        if len(self.custom_item_entries) > 1:
            # Find and remove the entry
            for entry in self.custom_item_entries:
                if entry['frame'] == row_frame:
                    self.custom_item_entries.remove(entry)
                    break
            # Destroy the frame
            row_frame.destroy()
            self.calculate_total()
    
    def on_doctor_select(self, event=None):
        """When doctor is selected, auto-fill consultation fee"""
        selection = self.doctor_combo.get()
        if selection:
            doctor_id = self.doctor_dict[selection]
            doctor = self.controller.get_doctor(doctor_id)
            if doctor:
                self.consultation_fee_var.set(str(doctor.consultation_fee))
                self.calculate_total()
    
    def calculate_total(self, event=None):
        """Calculate total amount from all fees and items"""
        total = 0
        
        # Doctor consultation fee
        if self.include_consultation.get():
            try:
                cons_fee = float(self.consultation_fee_var.get()) if self.consultation_fee_var.get() else 0
                total += cons_fee
            except ValueError:
                pass
        
        # Hospital charges
        try:
            room = float(self.room_charges_var.get()) if self.room_charges_var.get() else 0
            total += room
        except ValueError:
            pass
        
        try:
            lab = float(self.lab_charges_var.get()) if self.lab_charges_var.get() else 0
            total += lab
        except ValueError:
            pass
        
        try:
            pharmacy = float(self.pharmacy_charges_var.get()) if self.pharmacy_charges_var.get() else 0
            total += pharmacy
        except ValueError:
            pass
        
        try:
            other_hospital = float(self.other_hospital_var.get()) if self.other_hospital_var.get() else 0
            total += other_hospital
        except ValueError:
            pass
        
        # Treatment fees
        try:
            procedure = float(self.procedure_fee_var.get()) if self.procedure_fee_var.get() else 0
            total += procedure
        except ValueError:
            pass
        
        try:
            surgery = float(self.surgery_fee_var.get()) if self.surgery_fee_var.get() else 0
            total += surgery
        except ValueError:
            pass
        
        try:
            therapy = float(self.therapy_fee_var.get()) if self.therapy_fee_var.get() else 0
            total += therapy
        except ValueError:
            pass
        
        try:
            other_treatment = float(self.other_treatment_var.get()) if self.other_treatment_var.get() else 0
            total += other_treatment
        except ValueError:
            pass
        
        # Custom items
        for item in self.custom_item_entries:
            try:
                qty = float(item['qty'].get()) if item['qty'].get() else 0
                price = float(item['price'].get()) if item['price'].get() else 0
                total += qty * price
            except ValueError:
                pass
        
        self.total_amount_label.config(text=f"Rs. {total:.2f}")
    
    def setup_bills_tab(self):
        """Setup all bills tab"""
        # Title
        title = tk.Label(
            self.bills_frame,
            text="📋 All Bills",
            font=("Segoe UI", 16, "bold"),
            fg=PremiumTheme.PRIMARY,
            bg=PremiumTheme.CARD_BG
        )
        title.pack(pady=10)
        
        # Search bar
        search_frame = tk.Frame(self.bills_frame, bg=PremiumTheme.CARD_BG)
        search_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            search_frame,
            text="🔍",
            font=("Segoe UI", 12),
            bg=PremiumTheme.CARD_BG,
            fg=PremiumTheme.MEDIUM_GRAY
        ).pack(side='left', padx=(0, 5))
        
        self.search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 10),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1
        )
        self.search_entry.pack(side='left', fill='x', expand=True, ipady=5)
        self.search_entry.bind('<KeyRelease>', self.search_bills)
        
        # Treeview
        tree_frame = tk.Frame(self.bills_frame, bg=PremiumTheme.CARD_BG)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        self.bills_tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Patient', 'Date', 'Total', 'Paid', 'Balance', 'Status'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=12
        )
        
        vsb.config(command=self.bills_tree.yview)
        hsb.config(command=self.bills_tree.xview)
        
        # Define headings
        self.bills_tree.heading('ID', text='Bill ID')
        self.bills_tree.heading('Patient', text='Patient')
        self.bills_tree.heading('Date', text='Date')
        self.bills_tree.heading('Total', text='Total (Rs.)')
        self.bills_tree.heading('Paid', text='Paid (Rs.)')
        self.bills_tree.heading('Balance', text='Balance (Rs.)')
        self.bills_tree.heading('Status', text='Status')
        
        # Set column widths
        self.bills_tree.column('ID', width=130)
        self.bills_tree.column('Patient', width=130)
        self.bills_tree.column('Date', width=80)
        self.bills_tree.column('Total', width=80)
        self.bills_tree.column('Paid', width=80)
        self.bills_tree.column('Balance', width=80)
        self.bills_tree.column('Status', width=100)
        
        # Grid layout
        self.bills_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Configure tag colors
        self.bills_tree.tag_configure('Unpaid', background='#f8d7da')
        self.bills_tree.tag_configure('Partially Paid', background='#fff3cd')
        self.bills_tree.tag_configure('Paid', background='#d4edda')
        
        # Bind selection
        self.bills_tree.bind('<<TreeviewSelect>>', self.on_bill_select)
        
        # Bill details frame
        details_frame = tk.Frame(self.bills_frame, bg=PremiumTheme.CARD_BG, relief='solid', borderwidth=1)
        details_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            details_frame,
            text="📄 Bill Details",
            font=("Segoe UI", 12, "bold"),
            fg=PremiumTheme.PRIMARY,
            bg=PremiumTheme.CARD_BG
        ).pack(pady=5)
        
        self.details_text = tk.Text(
            details_frame,
            font=("Courier", 9),
            height=8,
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1,
            state='disabled'
        )
        self.details_text.pack(fill='x', padx=10, pady=5)
    
    def setup_payment_tab(self):
        """Setup payment tab"""
        # Title
        title = tk.Label(
            self.payment_frame,
            text="💳 Make a Payment",
            font=("Segoe UI", 16, "bold"),
            fg=PremiumTheme.PRIMARY,
            bg=PremiumTheme.CARD_BG
        )
        title.pack(pady=10)
        
        # Payment form
        form_frame = tk.Frame(self.payment_frame, bg=PremiumTheme.CARD_BG, relief='solid', borderwidth=1)
        form_frame.pack(fill='x', padx=20, pady=10)
        
        # Bill selection
        tk.Label(
            form_frame,
            text="Select Bill:",
            font=("Segoe UI", 11, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).grid(row=0, column=0, padx=10, pady=8, sticky='w')
        
        self.payment_bill_combo = ttk.Combobox(
            form_frame,
            font=("Segoe UI", 10),
            state='readonly',
            width=45
        )
        self.payment_bill_combo.grid(row=0, column=1, padx=10, pady=8)
        self.payment_bill_combo.bind('<<ComboboxSelected>>', self.on_payment_bill_select)
        
        # Bill info
        self.payment_info_label = tk.Label(
            form_frame,
            text="Select a bill to view details",
            font=("Segoe UI", 10),
            fg=PremiumTheme.DARK,
            bg=PremiumTheme.LIGHT_GRAY,
            justify='left',
            padx=8,
            pady=8
        )
        self.payment_info_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='ew')
        
        # Payment amount
        tk.Label(
            form_frame,
            text="Payment Amount (Rs.):",
            font=("Segoe UI", 11, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).grid(row=2, column=0, padx=10, pady=8, sticky='w')
        
        self.payment_amount_entry = tk.Entry(
            form_frame,
            font=("Segoe UI", 10),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1,
            width=20
        )
        self.payment_amount_entry.grid(row=2, column=1, padx=10, pady=8, sticky='w')
        
        # Payment method
        tk.Label(
            form_frame,
            text="Payment Method:",
            font=("Segoe UI", 11, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).grid(row=3, column=0, padx=10, pady=8, sticky='w')
        
        self.payment_method = ttk.Combobox(
            form_frame,
            values=['Cash', 'Credit Card', 'Debit Card', 'Insurance', 'Online'],
            font=("Segoe UI", 10),
            state='readonly',
            width=20
        )
        self.payment_method.grid(row=3, column=1, padx=10, pady=8, sticky='w')
        self.payment_method.set('Cash')
        
        # PAYMENT BUTTON
        self.pay_btn = tk.Button(
            form_frame,
            text="✅ PROCESS PAYMENT",
            font=("Segoe UI", 12, "bold"),
            bg=PremiumTheme.SUCCESS,
            fg='white',
            activebackground=PremiumTheme.SUCCESS,
            activeforeground='white',
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            height=1,
            command=self.make_payment
        )
        self.pay_btn.grid(row=4, column=0, columnspan=2, pady=15, ipadx=20)
    
    def setup_patient_bills_tab(self):
        """Setup patient bills tab"""
        # Title
        title = tk.Label(
            self.patient_frame,
            text="👤 Patient Bills",
            font=("Segoe UI", 16, "bold"),
            fg=PremiumTheme.PRIMARY,
            bg=PremiumTheme.CARD_BG
        )
        title.pack(pady=10)
        
        # Patient selection
        select_frame = tk.Frame(self.patient_frame, bg=PremiumTheme.CARD_BG)
        select_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            select_frame,
            text="Select Patient:",
            font=("Segoe UI", 11, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left', padx=(0, 10))
        
        self.patient_bills_combo = ttk.Combobox(
            select_frame,
            font=("Segoe UI", 10),
            state='readonly',
            width=40
        )
        self.patient_bills_combo.pack(side='left')
        self.patient_bills_combo.bind('<<ComboboxSelected>>', self.load_patient_bills)
        
        # Treeview for patient bills
        tree_frame = tk.Frame(self.patient_frame, bg=PremiumTheme.CARD_BG)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.patient_bills_tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Date', 'Total', 'Paid', 'Balance', 'Status'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=12
        )
        
        vsb.config(command=self.patient_bills_tree.yview)
        hsb.config(command=self.patient_bills_tree.xview)
        
        # Define headings
        self.patient_bills_tree.heading('ID', text='Bill ID')
        self.patient_bills_tree.heading('Date', text='Date')
        self.patient_bills_tree.heading('Total', text='Total (Rs.)')
        self.patient_bills_tree.heading('Paid', text='Paid (Rs.)')
        self.patient_bills_tree.heading('Balance', text='Balance (Rs.)')
        self.patient_bills_tree.heading('Status', text='Status')
        
        # Set column widths
        self.patient_bills_tree.column('ID', width=130)
        self.patient_bills_tree.column('Date', width=80)
        self.patient_bills_tree.column('Total', width=80)
        self.patient_bills_tree.column('Paid', width=80)
        self.patient_bills_tree.column('Balance', width=80)
        self.patient_bills_tree.column('Status', width=100)
        
        # Grid layout
        self.patient_bills_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Configure tag colors
        self.patient_bills_tree.tag_configure('Unpaid', background='#f8d7da')
        self.patient_bills_tree.tag_configure('Partially Paid', background='#fff3cd')
        self.patient_bills_tree.tag_configure('Paid', background='#d4edda')
    
    def load_data(self):
        """Load all data"""
        # Load patients
        patients = self.controller.get_all_patients()
        self.patient_dict = {f"{p.name} ({p.id})": p.id for p in patients}
        self.patient_combo['values'] = list(self.patient_dict.keys())
        self.patient_bills_combo['values'] = list(self.patient_dict.keys())
        
        # Load doctors
        doctors = self.controller.get_all_doctors()
        self.doctor_dict = {f"Dr. {p.name} ({p.id})": p.id for p in doctors}
        self.doctor_combo['values'] = list(self.doctor_dict.keys())
        
        # Load bills
        self.load_bills()
        self.load_payment_bills()
    
    def load_bills(self):
        """Load all bills"""
        for item in self.bills_tree.get_children():
            self.bills_tree.delete(item)
        
        patients = {p.id: p.name for p in self.controller.get_all_patients()}
        
        bills = self.controller.get_all_bills()
        for bill in bills:
            patient_name = patients.get(bill.patient_id, "Unknown")
            balance = bill.total_amount - bill.paid_amount
            
            self.bills_tree.insert('', 'end', values=(
                bill.id,
                patient_name,
                bill.created_date[:10],
                f"Rs. {bill.total_amount:.2f}",
                f"Rs. {bill.paid_amount:.2f}",
                f"Rs. {balance:.2f}",
                bill.status
            ), tags=(bill.status,), iid=bill.id)
    
    def load_payment_bills(self):
        """Load unpaid bills"""
        bills = self.controller.get_all_bills()
        unpaid_bills = []
        
        patients = {p.id: p.name for p in self.controller.get_all_patients()}
        
        for bill in bills:
            if bill.status != 'Paid':
                patient_name = patients.get(bill.patient_id, "Unknown")
                balance = bill.total_amount - bill.paid_amount
                display = f"{bill.id} - {patient_name} - Balance: Rs. {balance:.2f}"
                unpaid_bills.append(display)
        
        self.payment_bill_combo['values'] = unpaid_bills
    
    def create_bill(self):
        """Create a new bill manually"""
        try:
            # Validate patient selection
            if not self.patient_combo.get():
                messagebox.showerror("Error", "Please select a patient!")
                return
            
            # Get patient ID
            patient_id = self.patient_dict[self.patient_combo.get()]
            
            # Create bill ID
            bill_id = self.controller.data_manager.generate_id('BIL')
            
            # Create bill object
            from models.bill import Bill
            bill = Bill(bill_id, patient_id)
            
            items_added = False
            
            # Add doctor consultation fee
            if self.include_consultation.get() and self.consultation_fee_var.get():
                try:
                    cons_fee = float(self.consultation_fee_var.get())
                    if cons_fee > 0:
                        doctor_name = self.doctor_combo.get() if self.doctor_combo.get() else "Doctor"
                        bill.add_item(f"Consultation - {doctor_name}", 1, cons_fee)
                        items_added = True
                except ValueError:
                    pass
            
            # Add hospital charges
            try:
                room = float(self.room_charges_var.get()) if self.room_charges_var.get() else 0
                if room > 0:
                    bill.add_item("Room Charges", 1, room)
                    items_added = True
            except ValueError:
                pass
            
            try:
                lab = float(self.lab_charges_var.get()) if self.lab_charges_var.get() else 0
                if lab > 0:
                    bill.add_item("Lab Charges", 1, lab)
                    items_added = True
            except ValueError:
                pass
            
            try:
                pharmacy = float(self.pharmacy_charges_var.get()) if self.pharmacy_charges_var.get() else 0
                if pharmacy > 0:
                    bill.add_item("Medicine Charges", 1, pharmacy)
                    items_added = True
            except ValueError:
                pass
            
            try:
                other_hospital = float(self.other_hospital_var.get()) if self.other_hospital_var.get() else 0
                if other_hospital > 0:
                    bill.add_item("Other Hospital Charges", 1, other_hospital)
                    items_added = True
            except ValueError:
                pass
            
            # Add treatment fees
            try:
                procedure = float(self.procedure_fee_var.get()) if self.procedure_fee_var.get() else 0
                if procedure > 0:
                    bill.add_item("Procedure Fees", 1, procedure)
                    items_added = True
            except ValueError:
                pass
            
            try:
                surgery = float(self.surgery_fee_var.get()) if self.surgery_fee_var.get() else 0
                if surgery > 0:
                    bill.add_item("Surgery Fees", 1, surgery)
                    items_added = True
            except ValueError:
                pass
            
            try:
                therapy = float(self.therapy_fee_var.get()) if self.therapy_fee_var.get() else 0
                if therapy > 0:
                    bill.add_item("Therapy Fees", 1, therapy)
                    items_added = True
            except ValueError:
                pass
            
            try:
                other_treatment = float(self.other_treatment_var.get()) if self.other_treatment_var.get() else 0
                if other_treatment > 0:
                    bill.add_item("Other Treatment Fees", 1, other_treatment)
                    items_added = True
            except ValueError:
                pass
            
            # Add custom items
            for item in self.custom_item_entries:
                desc = item['desc'].get().strip()
                qty = item['qty'].get().strip()
                price = item['price'].get().strip()
                
                if desc and qty and price:
                    try:
                        qty_val = float(qty)
                        price_val = float(price)
                        if qty_val > 0 and price_val > 0:
                            bill.add_item(desc, qty_val, price_val)
                            items_added = True
                    except ValueError:
                        messagebox.showerror("Error", "Please enter valid numbers for custom items!")
                        return
            
            if not items_added:
                messagebox.showerror("Error", "Please add at least one charge or item to the bill!")
                return
            
            # Save bill
            self.controller.bills[bill_id] = bill
            self.controller.save_all_data()
            
            messagebox.showinfo("Success", f"Bill created successfully!\nBill ID: {bill_id}\nTotal Amount: Rs. {bill.total_amount:.2f}")
            
            # Refresh data
            self.load_bills()
            self.load_payment_bills()
            
            # Clear form
            self.clear_form()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create bill: {str(e)}")
    
    def clear_form(self):
        """Clear the create bill form"""
        self.patient_combo.set('')
        self.doctor_combo.set('')
        self.consultation_fee_var.set('')
        self.include_consultation.set(True)
        
        # Clear hospital charges
        self.room_charges_var.set('')
        self.lab_charges_var.set('')
        self.pharmacy_charges_var.set('')
        self.other_hospital_var.set('')
        
        # Clear treatment fees
        self.procedure_fee_var.set('')
        self.surgery_fee_var.set('')
        self.therapy_fee_var.set('')
        self.other_treatment_var.set('')
        
        # Remove all custom item rows except first
        while len(self.custom_item_entries) > 1:
            self.remove_custom_item_row(self.custom_item_entries[-1]['frame'])
        
        # Clear first custom item row
        if self.custom_item_entries:
            self.custom_item_entries[0]['desc'].delete(0, 'end')
            self.custom_item_entries[0]['qty'].delete(0, 'end')
            self.custom_item_entries[0]['qty'].insert(0, "1")
            self.custom_item_entries[0]['price'].delete(0, 'end')
            self.custom_item_entries[0]['total_label'].config(text="Rs. 0")
        
        self.total_amount_label.config(text="Rs. 0.00")
    
    def search_bills(self, event=None):
        """Search bills"""
        search_term = self.search_entry.get().lower()
        
        for item in self.bills_tree.get_children():
            self.bills_tree.delete(item)
        
        patients = {p.id: p.name for p in self.controller.get_all_patients()}
        
        bills = self.controller.get_all_bills()
        for bill in bills:
            patient_name = patients.get(bill.patient_id, "Unknown")
            balance = bill.total_amount - bill.paid_amount
            
            if (search_term in patient_name.lower() or 
                search_term in bill.id.lower()):
                self.bills_tree.insert('', 'end', values=(
                    bill.id,
                    patient_name,
                    bill.created_date[:10],
                    f"Rs. {bill.total_amount:.2f}",
                    f"Rs. {bill.paid_amount:.2f}",
                    f"Rs. {balance:.2f}",
                    bill.status
                ), tags=(bill.status,), iid=bill.id)
    
    def load_patient_bills(self, event=None):
        """Load patient bills"""
        for item in self.patient_bills_tree.get_children():
            self.patient_bills_tree.delete(item)
        
        selection = self.patient_bills_combo.get()
        if not selection:
            return
        
        patient_id = self.patient_dict[selection]
        bills = self.controller.get_patient_bills(patient_id)
        
        for bill in bills:
            balance = bill.total_amount - bill.paid_amount
            
            self.patient_bills_tree.insert('', 'end', values=(
                bill.id,
                bill.created_date[:10],
                f"Rs. {bill.total_amount:.2f}",
                f"Rs. {bill.paid_amount:.2f}",
                f"Rs. {balance:.2f}",
                bill.status
            ), tags=(bill.status,))
    
    def on_bill_select(self, event):
        """Handle bill selection"""
        selection = self.bills_tree.selection()
        if selection:
            bill_id = selection[0]
            bill = self.controller.bills.get(bill_id)
            
            if bill:
                self.details_text.config(state='normal')
                self.details_text.delete('1.0', 'end')
                
                patient = self.controller.get_patient(bill.patient_id)
                patient_name = patient.name if patient else "Unknown"
                
                details = "=" * 40 + "\n"
                details += f"BILL DETAILS\n"
                details += "=" * 40 + "\n\n"
                details += f"Bill ID: {bill.id}\n"
                details += f"Patient: {patient_name}\n"
                details += f"Date: {bill.created_date}\n"
                details += f"Status: {bill.status}\n\n"
                details += "Items:\n"
                details += "-" * 30 + "\n"
                
                for item in bill.items:
                    details += f"{item['description']}\n"
                    details += f"  {item['quantity']} x Rs.{item['unit_price']} = Rs.{item['total']}\n"
                
                details += "-" * 30 + "\n"
                details += f"Total: Rs.{bill.total_amount:.2f}\n"
                details += f"Paid: Rs.{bill.paid_amount:.2f}\n"
                details += f"Balance: Rs.{bill.total_amount - bill.paid_amount:.2f}\n"
                
                self.details_text.insert('1.0', details)
                self.details_text.config(state='disabled')
    
    def on_payment_bill_select(self, event):
        """Handle payment bill selection"""
        selection = self.payment_bill_combo.get()
        if selection:
            bill_id = selection.split(' - ')[0]
            bill = self.controller.bills.get(bill_id)
            
            if bill:
                patient = self.controller.get_patient(bill.patient_id)
                patient_name = patient.name if patient else "Unknown"
                balance = bill.total_amount - bill.paid_amount
                
                info = f"Bill ID: {bill_id}\n"
                info += f"Patient: {patient_name}\n"
                info += f"Total: Rs.{bill.total_amount:.2f}\n"
                info += f"Paid: Rs.{bill.paid_amount:.2f}\n"
                info += f"Balance: Rs.{balance:.2f}\n"
                info += f"Status: {bill.status}"
                
                self.payment_info_label.config(text=info)
                self.payment_amount_entry.delete(0, 'end')
                self.payment_amount_entry.insert(0, str(balance))
    
    def make_payment(self):
        """Process payment"""
        try:
            selection = self.payment_bill_combo.get()
            if not selection:
                messagebox.showwarning("Warning", "Please select a bill!")
                return
            
            bill_id = selection.split(' - ')[0]
            amount = float(self.payment_amount_entry.get())
            
            if amount <= 0:
                messagebox.showwarning("Warning", "Please enter a valid amount!")
                return
            
            bill = self.controller.bills.get(bill_id)
            if amount > (bill.total_amount - bill.paid_amount):
                messagebox.showwarning("Warning", "Payment amount exceeds balance!")
                return
            
            if not self.payment_method.get():
                messagebox.showwarning("Warning", "Please select payment method!")
                return
            
            if self.controller.make_payment(bill_id, amount):
                messagebox.showinfo("Success", f"Payment of Rs. {amount:.2f} processed!")
                self.load_bills()
                self.load_payment_bills()
                if self.patient_bills_combo.get():
                    self.load_patient_bills()
                
                self.payment_bill_combo.set('')
                self.payment_amount_entry.delete(0, 'end')
                self.payment_info_label.config(text="Select a bill to view details")
            else:
                messagebox.showerror("Error", "Failed to process payment")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")