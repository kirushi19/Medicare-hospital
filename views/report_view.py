import tkinter as tk
from tkinter import ttk, messagebox
from utils.theme import PremiumTheme
from datetime import datetime

class ReportView:
    """Reports and analytics view"""
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.setup_ui()
        self.load_reports()
    
    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.parent, bg=PremiumTheme.BACKGROUND)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(
            main_container,
            text="📊 Reports & Analytics",
            font=("Segoe UI", 24, "bold"),
            fg=PremiumTheme.PRIMARY,
            bg=PremiumTheme.BACKGROUND
        )
        title.pack(pady=20)
        
        # Create notebook for different reports
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Summary Report
        self.summary_frame = tk.Frame(self.notebook, bg=PremiumTheme.CARD_BG)
        self.notebook.add(self.summary_frame, text='📈 Summary Report')
        self.setup_summary_tab()
        
        # Tab 2: Patient Report
        self.patient_frame = tk.Frame(self.notebook, bg=PremiumTheme.CARD_BG)
        self.notebook.add(self.patient_frame, text='👥 Patient Report')
        self.setup_patient_tab()
        
        # Tab 3: Doctor Report
        self.doctor_frame = tk.Frame(self.notebook, bg=PremiumTheme.CARD_BG)
        self.notebook.add(self.doctor_frame, text='👨‍⚕️ Doctor Report')
        self.setup_doctor_tab()
        
        # Tab 4: Financial Report
        self.financial_frame = tk.Frame(self.notebook, bg=PremiumTheme.CARD_BG)
        self.notebook.add(self.financial_frame, text='💰 Financial Report')
        self.setup_financial_tab()
    
    def setup_summary_tab(self):
        """Setup summary report tab"""
        # Statistics cards frame
        cards_frame = tk.Frame(self.summary_frame, bg=PremiumTheme.CARD_BG)
        cards_frame.pack(pady=30)
        
        self.stats_labels = {}
        
        # Create statistics cards
        stats = [
            ("Total Patients", "0", "👥", PremiumTheme.PRIMARY),
            ("Total Doctors", "0", "👨‍⚕️", PremiumTheme.SECONDARY),
            ("Total Appointments", "0", "📅", PremiumTheme.ACCENT),
            ("Total Treatments", "0", "💊", PremiumTheme.SUCCESS),
            ("Total Revenue", "Rs. 0", "💰", PremiumTheme.WARNING),
            ("Outstanding", "Rs. 0", "⚠️", PremiumTheme.DANGER)
        ]
        
        for i, (title, value, icon, color) in enumerate(stats):
            card = tk.Frame(
                cards_frame,
                bg='white',
                relief='flat',
                highlightbackground=PremiumTheme.LIGHT_GRAY,
                highlightthickness=1
            )
            card.grid(row=i//3, column=i%3, padx=10, pady=10, ipadx=20, ipady=15)
            
            icon_label = tk.Label(
                card,
                text=icon,
                font=("Segoe UI", 32),
                fg=color,
                bg='white'
            )
            icon_label.pack()
            
            value_label = tk.Label(
                card,
                text=value,
                font=("Segoe UI", 18, "bold"),
                fg=PremiumTheme.DARK,
                bg='white'
            )
            value_label.pack()
            self.stats_labels[title] = value_label
            
            title_label = tk.Label(
                card,
                text=title,
                font=("Segoe UI", 10),
                fg=PremiumTheme.MEDIUM_GRAY,
                bg='white'
            )
            title_label.pack()
    
    def setup_patient_tab(self):
        """Setup patient report tab"""
        # Controls
        controls_frame = tk.Frame(self.patient_frame, bg=PremiumTheme.CARD_BG)
        controls_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            controls_frame,
            text="Select Patient:",
            font=("Segoe UI", 12, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left', padx=(0, 10))
        
        self.patient_combo = ttk.Combobox(
            controls_frame,
            font=("Segoe UI", 11),
            state='readonly',
            width=50
        )
        self.patient_combo.pack(side='left')
        self.patient_combo.bind('<<ComboboxSelected>>', self.generate_patient_report)
        
        # Report display
        report_frame = tk.Frame(self.patient_frame, bg=PremiumTheme.CARD_BG)
        report_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(report_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.patient_report_text = tk.Text(
            report_frame,
            font=("Courier", 10),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            wrap='word',
            yscrollcommand=scrollbar.set
        )
        self.patient_report_text.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=self.patient_report_text.yview)
    
    def setup_doctor_tab(self):
        """Setup doctor report tab"""
        # Controls
        controls_frame = tk.Frame(self.doctor_frame, bg=PremiumTheme.CARD_BG)
        controls_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            controls_frame,
            text="Select Doctor:",
            font=("Segoe UI", 12, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left', padx=(0, 10))
        
        self.doctor_combo = ttk.Combobox(
            controls_frame,
            font=("Segoe UI", 11),
            state='readonly',
            width=50
        )
        self.doctor_combo.pack(side='left')
        self.doctor_combo.bind('<<ComboboxSelected>>', self.generate_doctor_report)
        
        # Report display
        report_frame = tk.Frame(self.doctor_frame, bg=PremiumTheme.CARD_BG)
        report_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(report_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.doctor_report_text = tk.Text(
            report_frame,
            font=("Courier", 10),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            wrap='word',
            yscrollcommand=scrollbar.set
        )
        self.doctor_report_text.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=self.doctor_report_text.yview)
    
    def setup_financial_tab(self):
        """Setup financial report tab"""
        # Summary cards
        cards_frame = tk.Frame(self.financial_frame, bg=PremiumTheme.CARD_BG)
        cards_frame.pack(pady=20)
        
        self.financial_labels = {}
        
        financial_stats = [
            ("Total Revenue", "Rs. 0", "💰", PremiumTheme.SUCCESS),
            ("Total Paid", "Rs. 0", "✅", PremiumTheme.INFO),
            ("Outstanding", "Rs. 0", "⚠️", PremiumTheme.WARNING),
            ("Collection Rate", "0%", "📊", PremiumTheme.PRIMARY),
            ("Total Bills", "0", "📄", PremiumTheme.SECONDARY),
            ("Paid Bills", "0", "✔️", PremiumTheme.ACCENT)
        ]
        
        for i, (title, value, icon, color) in enumerate(financial_stats):
            card = tk.Frame(
                cards_frame,
                bg='white',
                relief='flat',
                highlightbackground=PremiumTheme.LIGHT_GRAY,
                highlightthickness=1
            )
            card.grid(row=i//3, column=i%3, padx=10, pady=10, ipadx=20, ipady=15)
            
            icon_label = tk.Label(
                card,
                text=icon,
                font=("Segoe UI", 32),
                fg=color,
                bg='white'
            )
            icon_label.pack()
            
            value_label = tk.Label(
                card,
                text=value,
                font=("Segoe UI", 16, "bold"),
                fg=PremiumTheme.DARK,
                bg='white'
            )
            value_label.pack()
            self.financial_labels[title] = value_label
            
            title_label = tk.Label(
                card,
                text=title,
                font=("Segoe UI", 10),
                fg=PremiumTheme.MEDIUM_GRAY,
                bg='white'
            )
            title_label.pack()
        
        # Detailed report
        report_frame = tk.Frame(self.financial_frame, bg=PremiumTheme.CARD_BG)
        report_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(report_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.financial_report_text = tk.Text(
            report_frame,
            font=("Courier", 10),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            wrap='word',
            yscrollcommand=scrollbar.set,
            height=15
        )
        self.financial_report_text.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=self.financial_report_text.yview)
    
    def load_reports(self):
        """Load all report data"""
        # Load patients
        patients = self.controller.get_all_patients()
        self.patient_dict = {f"{p.name} ({p.id})": p.id for p in patients}
        self.patient_combo['values'] = list(self.patient_dict.keys())
        
        # Load doctors
        doctors = self.controller.get_all_doctors()
        self.doctor_dict = {f"Dr. {p.name} ({p.id})": p.id for p in doctors}
        self.doctor_combo['values'] = list(self.doctor_dict.keys())
        
        # Generate reports
        self.generate_summary_report()
        self.generate_financial_report()
    
    def generate_summary_report(self):
        """Generate summary report"""
        stats = self.controller.generate_patient_report()
        
        self.stats_labels['Total Patients'].config(text=str(stats['total_patients']))
        self.stats_labels['Total Doctors'].config(text=str(len(self.controller.get_all_doctors())))
        self.stats_labels['Total Appointments'].config(text=str(stats['total_appointments']))
        self.stats_labels['Total Treatments'].config(text=str(stats['total_treatments']))
        self.stats_labels['Total Revenue'].config(text=f"Rs. {stats['total_revenue']:,.2f}")
        self.stats_labels['Outstanding'].config(text=f"Rs. {stats['outstanding']:,.2f}")
    
    def generate_patient_report(self, event=None):
        """Generate patient report"""
        selection = self.patient_combo.get()
        if not selection:
            return
        
        patient_id = self.patient_dict[selection]
        patient = self.controller.get_patient(patient_id)
        
        if not patient:
            return
        
        self.patient_report_text.delete('1.0', 'end')
        
        report = "=" * 80 + "\n"
        report += "                     PATIENT MEDICAL REPORT\n"
        report += "=" * 80 + "\n\n"
        
        report += f"PATIENT INFORMATION\n"
        report += "-" * 40 + "\n"
        report += f"Patient ID:     {patient.id}\n"
        report += f"Name:           {patient.name}\n"
        report += f"Phone:          {patient.phone}\n"
        report += f"Email:          {patient.email}\n"
        report += f"Date of Birth:  {patient.date_of_birth}\n"
        report += f"Blood Group:    {patient.blood_group}\n"
        report += f"Registered:     {patient.created_date}\n\n"
        
        report += f"TREATMENT HISTORY\n"
        report += "-" * 40 + "\n"
        
        treatments = self.controller.get_patient_treatments(patient_id)
        doctors = {d.id: f"Dr. {d.name}" for d in self.controller.get_all_doctors()}
        
        if treatments:
            total_cost = 0
            for treatment in treatments:
                doctor_name = doctors.get(treatment.doctor_id, "Unknown")
                report += f"\nDate: {treatment.date}\n"
                report += f"Doctor: {doctor_name}\n"
                report += f"Diagnosis: {treatment.diagnosis}\n"
                report += f"Prescription: {treatment.prescription}\n"
                report += f"Cost: Rs. {treatment.cost:.2f}\n"
                report += "-" * 40 + "\n"
                total_cost += treatment.cost
            
            report += f"\nTotal Treatment Cost: Rs. {total_cost:,.2f}\n"
        else:
            report += "\nNo treatment records found.\n\n"
        
        report += f"\nBILLING SUMMARY\n"
        report += "-" * 40 + "\n"
        
        bills = self.controller.get_patient_bills(patient_id)
        if bills:
            total_billed = sum(b.total_amount for b in bills)
            total_paid = sum(b.paid_amount for b in bills)
            
            report += f"Total Bills:     {len(bills)}\n"
            report += f"Total Billed:    Rs. {total_billed:,.2f}\n"
            report += f"Total Paid:      Rs. {total_paid:,.2f}\n"
            report += f"Outstanding:     Rs. {total_billed - total_paid:,.2f}\n\n"
            
            report += "Bill Details:\n"
            for bill in bills:
                report += f"  • {bill.id}: Rs. {bill.total_amount:,.2f} ({bill.status})\n"
        else:
            report += "No billing records found.\n"
        
        report += "\n" + "=" * 80 + "\n"
        report += f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "=" * 80
        
        self.patient_report_text.insert('1.0', report)
    
    def generate_doctor_report(self, event=None):
        """Generate doctor report"""
        selection = self.doctor_combo.get()
        if not selection:
            return
        
        doctor_id = self.doctor_dict[selection]
        doctor = self.controller.get_doctor(doctor_id)
        
        if not doctor:
            return
        
        self.doctor_report_text.delete('1.0', 'end')
        
        report = "=" * 80 + "\n"
        report += "                     DOCTOR PERFORMANCE REPORT\n"
        report += "=" * 80 + "\n\n"
        
        report += f"DOCTOR INFORMATION\n"
        report += "-" * 40 + "\n"
        report += f"Doctor ID:       {doctor.id}\n"
        report += f"Name:            {doctor.name}\n"
        report += f"Specialization:  {doctor.specialization}\n"
        report += f"Qualification:   {doctor.qualification}\n"
        report += f"Experience:      {doctor.experience} years\n"
        report += f"Fee:             Rs. {doctor.consultation_fee:.2f}\n\n"
        
        report += f"APPOINTMENTS SUMMARY\n"
        report += "-" * 40 + "\n"
        
        appointments = [a for a in self.controller.get_all_appointments() if a.doctor_id == doctor_id]
        if appointments:
            status_count = {'Pending': 0, 'Confirmed': 0, 'Completed': 0, 'Cancelled': 0}
            for apt in appointments:
                status_count[apt.status] += 1
            
            report += f"Total Appointments: {len(appointments)}\n"
            report += f"  • Pending:    {status_count['Pending']}\n"
            report += f"  • Confirmed:  {status_count['Confirmed']}\n"
            report += f"  • Completed:  {status_count['Completed']}\n"
            report += f"  • Cancelled:  {status_count['Cancelled']}\n\n"
        else:
            report += "No appointments found.\n\n"
        
        report += f"TREATMENTS SUMMARY\n"
        report += "-" * 40 + "\n"
        
        treatments = [t for t in self.controller.get_all_treatments() if t.doctor_id == doctor_id]
        if treatments:
            total_revenue = sum(t.cost for t in treatments)
            report += f"Total Treatments: {len(treatments)}\n"
            report += f"Total Revenue:    Rs. {total_revenue:,.2f}\n\n"
            
            report += "Recent Treatments:\n"
            for treatment in sorted(treatments, key=lambda x: x.date, reverse=True)[:5]:
                patient = self.controller.get_patient(treatment.patient_id)
                patient_name = patient.name if patient else "Unknown"
                report += f"  • {treatment.date}: {patient_name} - {treatment.diagnosis}\n"
                report += f"    Rs. {treatment.cost:.2f}\n"
        else:
            report += "No treatments found.\n"
        
        report += "\n" + "=" * 80 + "\n"
        report += f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "=" * 80
        
        self.doctor_report_text.insert('1.0', report)
    
    def generate_financial_report(self):
        """Generate financial report"""
        bills = self.controller.get_all_bills()
        
        total_revenue = sum(b.total_amount for b in bills)
        total_paid = sum(b.paid_amount for b in bills)
        outstanding = total_revenue - total_paid
        
        paid_bills = len([b for b in bills if b.status == 'Paid'])
        unpaid_bills = len([b for b in bills if b.status == 'Unpaid'])
        partial_bills = len([b for b in bills if b.status == 'Partially Paid'])
        
        collection_rate = (total_paid / total_revenue * 100) if total_revenue > 0 else 0
        
        # Update financial cards
        self.financial_labels['Total Revenue'].config(text=f"Rs. {total_revenue:,.2f}")
        self.financial_labels['Total Paid'].config(text=f"Rs. {total_paid:,.2f}")
        self.financial_labels['Outstanding'].config(text=f"Rs. {outstanding:,.2f}")
        self.financial_labels['Collection Rate'].config(text=f"{collection_rate:.1f}%")
        self.financial_labels['Total Bills'].config(text=str(len(bills)))
        self.financial_labels['Paid Bills'].config(text=str(paid_bills))
        
        # Generate detailed report
        self.financial_report_text.delete('1.0', 'end')
        
        report = "=" * 80 + "\n"
        report += "                     FINANCIAL REPORT\n"
        report += "=" * 80 + "\n\n"
        
        report += f"SUMMARY\n"
        report += "-" * 40 + "\n"
        report += f"Total Revenue:     Rs. {total_revenue:,.2f}\n"
        report += f"Total Paid:        Rs. {total_paid:,.2f}\n"
        report += f"Outstanding:       Rs. {outstanding:,.2f}\n"
        report += f"Collection Rate:   {collection_rate:.1f}%\n\n"
        
        report += f"BILLS BY STATUS\n"
        report += "-" * 40 + "\n"
        report += f"Paid Bills:        {paid_bills}\n"
        report += f"Unpaid Bills:      {unpaid_bills}\n"
        report += f"Partially Paid:    {partial_bills}\n"
        report += f"Total Bills:       {len(bills)}\n\n"
        
        if bills:
            report += f"RECENT BILLS\n"
            report += "-" * 40 + "\n"
            for bill in sorted(bills, key=lambda x: x.created_date, reverse=True)[:10]:
                patient = self.controller.get_patient(bill.patient_id)
                patient_name = patient.name if patient else "Unknown"
                report += f"  • {bill.created_date[:10]} - {patient_name}\n"
                report += f"    Amount: Rs. {bill.total_amount:,.2f} | Paid: Rs. {bill.paid_amount:,.2f} | {bill.status}\n"
        
        report += "\n" + "=" * 80 + "\n"
        report += f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "=" * 80
        
        self.financial_report_text.insert('1.0', report)