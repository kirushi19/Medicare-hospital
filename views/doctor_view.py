import tkinter as tk
from tkinter import ttk, messagebox
from utils.theme import PremiumTheme

class DoctorView:
    """Doctor management view with full CRUD operations"""
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.selected_doctor_id = None
        self.setup_ui()
        self.load_doctors()
    
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
            text="👨‍⚕️ Doctor Registration",
            font=("Segoe UI", 16, "bold"),
            fg=PremiumTheme.PRIMARY,
            bg=PremiumTheme.CARD_BG
        )
        form_title.pack(pady=20)
        
        # Form fields
        fields_frame = tk.Frame(form_content, bg=PremiumTheme.CARD_BG)
        fields_frame.pack(fill='x', padx=20, pady=10)
        
        # Name
        tk.Label(
            fields_frame,
            text="Full Name *",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.name_entry = tk.Entry(
            fields_frame,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1
        )
        self.name_entry.pack(fill='x', ipady=8)
        
        # Phone
        tk.Label(
            fields_frame,
            text="Phone Number *",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.phone_entry = tk.Entry(
            fields_frame,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1
        )
        self.phone_entry.pack(fill='x', ipady=8)
        
        # Email
        tk.Label(
            fields_frame,
            text="Email Address",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.email_entry = tk.Entry(
            fields_frame,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1
        )
        self.email_entry.pack(fill='x', ipady=8)
        
        # Address
        tk.Label(
            fields_frame,
            text="Address",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.address_entry = tk.Entry(
            fields_frame,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1
        )
        self.address_entry.pack(fill='x', ipady=8)
        
        # Specialization
        tk.Label(
            fields_frame,
            text="Specialization *",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.specialization_entry = tk.Entry(
            fields_frame,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1
        )
        self.specialization_entry.pack(fill='x', ipady=8)
        
        # Qualification
        tk.Label(
            fields_frame,
            text="Qualification",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.qualification_entry = tk.Entry(
            fields_frame,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1
        )
        self.qualification_entry.pack(fill='x', ipady=8)
        
        # Experience
        tk.Label(
            fields_frame,
            text="Experience (years)",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.experience_entry = tk.Entry(
            fields_frame,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1
        )
        self.experience_entry.pack(fill='x', ipady=8)
        
        # Consultation Fee
        tk.Label(
            fields_frame,
            text="Consultation Fee (Rs.) *",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(10, 5))
        
        self.fee_entry = tk.Entry(
            fields_frame,
            font=("Segoe UI", 11),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='solid',
            borderwidth=1
        )
        self.fee_entry.pack(fill='x', ipady=8)
        
        # ===== BUTTONS - VISIBLE NOW =====
        button_frame = tk.Frame(form_content, bg=PremiumTheme.CARD_BG)
        button_frame.pack(fill='x', padx=20, pady=30)
        
        # ADD DOCTOR BUTTON - GREEN
        self.add_btn = tk.Button(
            button_frame,
            text="➕ ADD DOCTOR",
            font=("Segoe UI", 14, "bold"),
            bg=PremiumTheme.SUCCESS,
            fg='white',
            activebackground=PremiumTheme.SUCCESS,
            activeforeground='white',
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            height=2,
            command=self.add_doctor
        )
        self.add_btn.pack(fill='x', pady=5)
        
        # UPDATE BUTTON - YELLOW
        self.update_btn = tk.Button(
            button_frame,
            text="✏️ UPDATE DOCTOR",
            font=("Segoe UI", 14, "bold"),
            bg=PremiumTheme.WARNING,
            fg='white',
            activebackground=PremiumTheme.WARNING,
            activeforeground='white',
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            height=2,
            command=self.update_doctor,
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
            text="📋 Registered Doctors",
            font=("Segoe UI", 16, "bold"),
            fg=PremiumTheme.PRIMARY,
            bg=PremiumTheme.CARD_BG
        )
        list_title.pack(pady=20)
        
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
        self.search_entry.bind('<KeyRelease>', self.search_doctors)
        
        # Treeview
        tree_frame = tk.Frame(right_frame, bg=PremiumTheme.CARD_BG)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Name', 'Specialization', 'Phone', 'Fee'),
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15
        )
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Define headings
        self.tree.heading('ID', text='Doctor ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Specialization', text='Specialization')
        self.tree.heading('Phone', text='Phone')
        self.tree.heading('Fee', text='Fee (Rs.)')
        
        # Set column widths
        self.tree.column('ID', width=150)
        self.tree.column('Name', width=150)
        self.tree.column('Specialization', width=150)
        self.tree.column('Phone', width=120)
        self.tree.column('Fee', width=100)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind selection
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # DELETE BUTTON
        self.delete_btn = tk.Button(
            right_frame,
            text="🗑️ DELETE SELECTED",
            font=("Segoe UI", 14, "bold"),
            bg=PremiumTheme.DANGER,
            fg='white',
            activebackground=PremiumTheme.DANGER,
            activeforeground='white',
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            height=2,
            command=self.delete_doctor
        )
        self.delete_btn.pack(fill='x', padx=20, pady=10)
    
    def add_doctor(self):
        """Add new doctor"""
        try:
            if not self.name_entry.get().strip():
                messagebox.showerror("Error", "Name is required!")
                return
            if not self.phone_entry.get().strip():
                messagebox.showerror("Error", "Phone number is required!")
                return
            if not self.specialization_entry.get().strip():
                messagebox.showerror("Error", "Specialization is required!")
                return
            
            doctor_data = {
                'name': self.name_entry.get().strip(),
                'phone': self.phone_entry.get().strip(),
                'email': self.email_entry.get().strip(),
                'address': self.address_entry.get().strip(),
                'specialization': self.specialization_entry.get().strip(),
                'qualification': self.qualification_entry.get().strip(),
                'experience': int(self.experience_entry.get()) if self.experience_entry.get() else 0,
                'consultation_fee': float(self.fee_entry.get()) if self.fee_entry.get() else 0
            }
            
            doctor = self.controller.add_doctor(doctor_data)
            
            if doctor:
                messagebox.showinfo("Success", f"Doctor added!\nID: {doctor.id}")
                self.load_doctors()
                self.clear_form()
            else:
                messagebox.showerror("Error", "Failed to add doctor")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def load_doctors(self):
        """Load doctors into treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        doctors = self.controller.get_all_doctors()
        for doctor in doctors:
            self.tree.insert('', 'end', values=(
                doctor.id,
                doctor.name,
                doctor.specialization,
                doctor.phone,
                f"Rs. {doctor.consultation_fee}"
            ), tags=(doctor.id,))
    
    def search_doctors(self, event=None):
        """Search doctors"""
        search_term = self.search_entry.get().lower()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        doctors = self.controller.get_all_doctors()
        for doctor in doctors:
            if (search_term in doctor.name.lower() or 
                search_term in doctor.specialization.lower()):
                self.tree.insert('', 'end', values=(
                    doctor.id,
                    doctor.name,
                    doctor.specialization,
                    doctor.phone,
                    f"Rs. {doctor.consultation_fee}"
                ), tags=(doctor.id,))
    
    def update_doctor(self):
        """Update selected doctor"""
        if not self.selected_doctor_id:
            messagebox.showwarning("Warning", "Select a doctor!")
            return
        
        try:
            updated_data = {
                'name': self.name_entry.get().strip(),
                'phone': self.phone_entry.get().strip(),
                'email': self.email_entry.get().strip(),
                'address': self.address_entry.get().strip(),
                'specialization': self.specialization_entry.get().strip(),
                'qualification': self.qualification_entry.get().strip(),
                'experience': int(self.experience_entry.get()) if self.experience_entry.get() else 0,
                'consultation_fee': float(self.fee_entry.get()) if self.fee_entry.get() else 0
            }
            
            if self.controller.update_doctor(self.selected_doctor_id, updated_data):
                messagebox.showinfo("Success", "Doctor updated!")
                self.load_doctors()
                self.clear_form()
                self.update_btn.config(state='disabled')
            else:
                messagebox.showerror("Error", "Failed to update")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def delete_doctor(self):
        """Delete selected doctor"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a doctor!")
            return
        
        if messagebox.askyesno("Confirm", "Delete this doctor?"):
            item = self.tree.item(selection[0])
            doctor_id = item['tags'][0]
            
            if self.controller.delete_doctor(doctor_id):
                messagebox.showinfo("Success", "Doctor deleted!")
                self.load_doctors()
                self.clear_form()
                self.update_btn.config(state='disabled')
    
    def clear_form(self):
        """Clear all form fields"""
        self.name_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.address_entry.delete(0, 'end')
        self.specialization_entry.delete(0, 'end')
        self.qualification_entry.delete(0, 'end')
        self.experience_entry.delete(0, 'end')
        self.fee_entry.delete(0, 'end')
        
        self.selected_doctor_id = None
        self.update_btn.config(state='disabled')
    
    def on_select(self, event):
        """Handle treeview selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            doctor_id = item['tags'][0]
            doctor = self.controller.get_doctor(doctor_id)
            
            if doctor:
                self.selected_doctor_id = doctor_id
                
                self.name_entry.delete(0, 'end')
                self.name_entry.insert(0, doctor.name)
                
                self.phone_entry.delete(0, 'end')
                self.phone_entry.insert(0, doctor.phone)
                
                self.email_entry.delete(0, 'end')
                self.email_entry.insert(0, doctor.email)
                
                self.address_entry.delete(0, 'end')
                self.address_entry.insert(0, doctor.address)
                
                self.specialization_entry.delete(0, 'end')
                self.specialization_entry.insert(0, doctor.specialization)
                
                self.qualification_entry.delete(0, 'end')
                self.qualification_entry.insert(0, doctor.qualification)
                
                self.experience_entry.delete(0, 'end')
                self.experience_entry.insert(0, str(doctor.experience))
                
                self.fee_entry.delete(0, 'end')
                self.fee_entry.insert(0, str(doctor.consultation_fee))
                
                self.update_btn.config(state='normal')