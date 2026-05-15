import tkinter as tk
from tkinter import messagebox, ttk
from utils.theme import PremiumTheme
from utils.animations import Animations
from views.patient_view import PatientView
from views.doctor_view import DoctorView
from views.appointment_view import AppointmentView
from views.treatment_view import TreatmentView
from views.billing_view import BillingView
from views.report_view import ReportView
from datetime import datetime

class MainWindow:
    """Ultra Premium Main Application Window with Scrollable Content"""
    
    def __init__(self, controller):
        self.controller = controller
        self.window = tk.Tk()
        self.window.title("Medi Care Hospital Management System - Premium Edition")
        self.window.geometry("1400x800")
        self.window.configure(bg=PremiumTheme.BACKGROUND)
        
        # Center window
        self.center_window()
        
        # Variables
        self.current_view = None
        
        self.setup_ui()
        Animations.fade_in(self.window, 600)
    
    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        # Top Navigation Bar
        self.setup_top_nav()
        
        # Main Container
        main_container = tk.Frame(self.window, bg=PremiumTheme.BACKGROUND)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Sidebar
        self.setup_sidebar(main_container)
        
        # Content Area with Scrollbar
        self.setup_content_area(main_container)
        
        # Status Bar
        self.setup_status_bar()
        
        # Show dashboard by default
        self.show_dashboard()
    
    def setup_top_nav(self):
        """Setup premium top navigation bar"""
        top_nav = tk.Frame(
            self.window,
            bg=PremiumTheme.CARD_BG,
            height=70,
            highlightbackground=PremiumTheme.LIGHT_GRAY,
            highlightthickness=1
        )
        top_nav.pack(fill='x')
        top_nav.pack_propagate(False)
        
        # Logo and Brand
        logo_frame = tk.Frame(top_nav, bg=PremiumTheme.CARD_BG)
        logo_frame.pack(side='left', padx=20, pady=15)
        
        # Medical Icon
        canvas = tk.Canvas(
            logo_frame,
            width=40,
            height=40,
            bg=PremiumTheme.CARD_BG,
            highlightthickness=0
        )
        canvas.pack(side='left', padx=(0, 10))
        
        # Draw medical icon
        canvas.create_rectangle(15, 10, 25, 30, fill=PremiumTheme.ACCENT, outline='')
        canvas.create_rectangle(5, 15, 35, 25, fill=PremiumTheme.ACCENT, outline='')
        
        tk.Label(
            logo_frame,
            text="MEDI CARE",
            font=("Segoe UI", 20, "bold"),
            fg=PremiumTheme.PRIMARY,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left')
        
        tk.Label(
            logo_frame,
            text="| Premium Hospital Management",
            font=("Segoe UI", 12),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left', padx=(10, 0))
        
        # Right Side Icons
        right_frame = tk.Frame(top_nav, bg=PremiumTheme.CARD_BG)
        right_frame.pack(side='right', padx=20)
        
        # Date/Time
        self.time_label = tk.Label(
            right_frame,
            font=("Segoe UI", 11),
            fg=PremiumTheme.DARK,
            bg=PremiumTheme.CARD_BG
        )
        self.time_label.pack(side='left', padx=10)
        self.update_time()
        
        # User Menu
        user_frame = tk.Frame(right_frame, bg=PremiumTheme.CARD_BG)
        user_frame.pack(side='left', padx=10)
        
        tk.Label(
            user_frame,
            text="👤",
            font=("Segoe UI", 16),
            bg=PremiumTheme.CARD_BG,
            fg=PremiumTheme.PRIMARY
        ).pack(side='left')
        
        tk.Label(
            user_frame,
            text="Admin",
            font=("Segoe UI", 11, "bold"),
            fg=PremiumTheme.DARK,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left', padx=(5, 0))
        
        # Logout Button
        logout_btn = tk.Button(
            right_frame,
            text="🚪",
            font=("Segoe UI", 16),
            bg=PremiumTheme.CARD_BG,
            fg=PremiumTheme.DANGER,
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            command=self.logout
        )
        logout_btn.pack(side='left', padx=10)
    
    def update_time(self):
        """Update time label"""
        current = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.time_label.config(text=current)
            self.window.after(1000, self.update_time)
        except:
            pass
    
    def setup_sidebar(self, parent):
        """Setup premium sidebar with modern design"""
        self.sidebar = tk.Frame(
            parent,
            bg=PremiumTheme.CARD_BG,
            width=280,
            highlightbackground=PremiumTheme.LIGHT_GRAY,
            highlightthickness=1
        )
        self.sidebar.pack(side='left', fill='y', padx=(0, 20))
        self.sidebar.pack_propagate(False)
        
        # Profile Section
        profile_frame = tk.Frame(self.sidebar, bg=PremiumTheme.CARD_BG)
        profile_frame.pack(fill='x', padx=20, pady=30)
        
        # Avatar
        avatar_canvas = tk.Canvas(
            profile_frame,
            width=80,
            height=80,
            bg=PremiumTheme.CARD_BG,
            highlightthickness=0
        )
        avatar_canvas.pack(pady=(0, 10))
        
        # Draw avatar circle
        avatar_canvas.create_oval(10, 10, 70, 70, fill=PremiumTheme.PRIMARY, outline='')
        avatar_canvas.create_text(40, 40, text="A", font=("Segoe UI", 30, "bold"), fill='white')
        
        tk.Label(
            profile_frame,
            text="Admin User",
            font=("Segoe UI", 14, "bold"),
            fg=PremiumTheme.DARK,
            bg=PremiumTheme.CARD_BG
        ).pack()
        
        tk.Label(
            profile_frame,
            text="System Administrator",
            font=("Segoe UI", 10),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack()
        
        # Separator
        separator = tk.Frame(self.sidebar, bg=PremiumTheme.LIGHT_GRAY, height=1)
        separator.pack(fill='x', padx=20, pady=20)
        
        # Navigation Menu
        menu_frame = tk.Frame(self.sidebar, bg=PremiumTheme.CARD_BG)
        menu_frame.pack(fill='both', expand=True, padx=10)
        
        # Menu items with icons
        menu_items = [
            ("📊", "Dashboard", self.show_dashboard),
            ("👥", "Patient Management", self.show_patients),
            ("👨‍⚕️", "Doctor Management", self.show_doctors),
            ("📅", "Appointments", self.show_appointments),
            ("💊", "Treatments", self.show_treatments),
            ("💰", "Billing", self.show_billing),
            ("📈", "Reports", self.show_reports),
            ("⚙️", "Settings", self.show_settings)
        ]
        
        self.menu_buttons = []
        
        for icon, text, command in menu_items:
            btn_frame = tk.Frame(menu_frame, bg=PremiumTheme.CARD_BG)
            btn_frame.pack(fill='x', pady=2)
            
            btn = tk.Button(
                btn_frame,
                text=f"{icon}  {text}",
                font=("Segoe UI", 11),
                anchor='w',
                bg=PremiumTheme.CARD_BG,
                fg=PremiumTheme.DARK,
                activebackground=PremiumTheme.PRIMARY,
                activeforeground='white',
                relief='flat',
                borderwidth=0,
                cursor='hand2',
                command=command
            )
            btn.pack(fill='x', padx=5, pady=2, ipady=8)
            
            # Hover effect
            btn.bind('<Enter>', lambda e, b=btn: self.on_menu_hover(b, True))
            btn.bind('<Leave>', lambda e, b=btn: self.on_menu_hover(b, False))
            
            self.menu_buttons.append(btn)
    
    def on_menu_hover(self, button, enter):
        """Handle menu hover effect"""
        if enter:
            button['bg'] = PremiumTheme.PRIMARY
            button['fg'] = 'white'
        else:
            button['bg'] = PremiumTheme.CARD_BG
            button['fg'] = PremiumTheme.DARK
    
    def setup_content_area(self, parent):
        """Setup premium content area with scrollbar"""
        # Content container with card style
        self.content_container = tk.Frame(
            parent,
            bg=PremiumTheme.CARD_BG,
            relief='flat',
            highlightbackground=PremiumTheme.LIGHT_GRAY,
            highlightthickness=1
        )
        self.content_container.pack(side='right', fill='both', expand=True)
        
        # Content header
        self.content_header = tk.Frame(
            self.content_container,
            bg=PremiumTheme.CARD_BG,
            height=60
        )
        self.content_header.pack(fill='x', padx=20, pady=20)
        self.content_header.pack_propagate(False)
        
        self.header_title = tk.Label(
            self.content_header,
            text="Dashboard",
            font=("Segoe UI", 20, "bold"),
            fg=PremiumTheme.DARK,
            bg=PremiumTheme.CARD_BG
        )
        self.header_title.pack(side='left')
        
        # Action buttons in header
        self.header_actions = tk.Frame(self.content_header, bg=PremiumTheme.CARD_BG)
        self.header_actions.pack(side='right')
        
        # Scrollable content area
        self.setup_scrollable_content()
    
    def setup_scrollable_content(self):
        """Setup scrollable content area"""
        # Create a canvas for scrolling
        self.canvas = tk.Canvas(
            self.content_container,
            bg=PremiumTheme.BACKGROUND,
            highlightthickness=0
        )
        
        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.content_container,
            orient="vertical",
            command=self.canvas.yview
        )
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create frame inside canvas
        self.scrollable_frame = tk.Frame(self.canvas, bg=PremiumTheme.BACKGROUND)
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )
        
        # Bind events
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Bind mouse wheel for scrolling
        self.bind_mousewheel()
        
        # This is where content will be placed
        self.content_frame = self.scrollable_frame
    
    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """When canvas is resized, resize the inner frame to match"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def bind_mousewheel(self):
        """Bind mouse wheel for scrolling"""
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def unbind_mousewheel(self):
        """Unbind mouse wheel when leaving the canvas"""
        self.canvas.unbind_all("<MouseWheel>")
    
    def setup_status_bar(self):
        """Setup premium status bar"""
        status_bar = tk.Frame(
            self.window,
            bg=PremiumTheme.DARK,
            height=30
        )
        status_bar.pack(fill='x', side='bottom')
        status_bar.pack_propagate(False)
        
        # System status
        tk.Label(
            status_bar,
            text="● System Online",
            font=("Segoe UI", 9),
            fg=PremiumTheme.SUCCESS,
            bg=PremiumTheme.DARK
        ).pack(side='left', padx=20, pady=5)
        
        # Database status
        tk.Label(
            status_bar,
            text="● Database Connected",
            font=("Segoe UI", 9),
            fg=PremiumTheme.SUCCESS,
            bg=PremiumTheme.DARK
        ).pack(side='left', padx=20, pady=5)
        
        # Version
        tk.Label(
            status_bar,
            text="Version 2.0.0 (Premium)",
            font=("Segoe UI", 9),
            fg=PremiumTheme.LIGHT_GRAY,
            bg=PremiumTheme.DARK
        ).pack(side='right', padx=20, pady=5)
    
    def clear_content(self):
        """Clear content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Clear header actions
        for widget in self.header_actions.winfo_children():
            widget.destroy()
    
    def set_header_title(self, title):
        """Set content header title"""
        self.header_title.config(text=title)
    
    def show_dashboard(self):
        """Show premium dashboard"""
        self.clear_content()
        self.set_header_title("Dashboard")
        
        # Welcome banner
        banner = tk.Frame(
            self.content_frame,
            bg=PremiumTheme.PRIMARY,
            height=150
        )
        banner.pack(fill='x', pady=(0, 20))
        banner.pack_propagate(False)
        
        welcome_text = f"Welcome back, Admin! Today is {datetime.now().strftime('%A, %B %d, %Y')}"
        
        tk.Label(
            banner,
            text=welcome_text,
            font=("Segoe UI", 18),
            fg='white',
            bg=PremiumTheme.PRIMARY
        ).pack(pady=30)
        
        tk.Label(
            banner,
            text="Here's what's happening with your hospital today",
            font=("Segoe UI", 12),
            fg='#cccccc',
            bg=PremiumTheme.PRIMARY
        ).pack()
        
        # Statistics Cards
        stats = self.controller.generate_patient_report()
        
        # Stats grid
        stats_grid = tk.Frame(self.content_frame, bg=PremiumTheme.BACKGROUND)
        stats_grid.pack(fill='x', pady=20)
        
        # Configure grid columns
        for i in range(3):
            stats_grid.columnconfigure(i, weight=1)
        
        cards = [
            ("Total Patients", stats['total_patients'], "👥", PremiumTheme.PRIMARY),
            ("Total Doctors", len(self.controller.get_all_doctors()), "👨‍⚕️", PremiumTheme.SECONDARY),
            ("Appointments", stats['total_appointments'], "📅", PremiumTheme.ACCENT),
            ("Treatments", stats['total_treatments'], "💊", PremiumTheme.SUCCESS),
            ("Revenue", f"Rs. {stats['total_revenue']:,}", "💰", PremiumTheme.WARNING),
            ("Outstanding", f"Rs. {stats['outstanding']:,}", "⚠️", PremiumTheme.DANGER)
        ]
        
        for i, (title, value, icon, color) in enumerate(cards):
            self.create_stat_card(stats_grid, title, value, icon, color, i)
        
        # Quick Actions
        actions_label = tk.Label(
            self.content_frame,
            text="Quick Actions",
            font=("Segoe UI", 16, "bold"),
            fg=PremiumTheme.DARK,
            bg=PremiumTheme.BACKGROUND
        )
        actions_label.pack(anchor='w', pady=(30, 20))
        
        actions_grid = tk.Frame(self.content_frame, bg=PremiumTheme.BACKGROUND)
        actions_grid.pack(fill='x')
        
        for i in range(4):
            actions_grid.columnconfigure(i, weight=1)
        
        quick_actions = [
            ("➕", "New Patient", self.show_patients, PremiumTheme.SUCCESS),
            ("📋", "Schedule", self.show_appointments, PremiumTheme.ACCENT),
            ("💰", "New Bill", self.show_billing, PremiumTheme.WARNING),
            ("📊", "Reports", self.show_reports, PremiumTheme.PURPLE)
        ]
        
        for i, (icon, text, command, color) in enumerate(quick_actions):
            self.create_action_card(actions_grid, icon, text, command, color, i)
    
    def create_stat_card(self, parent, title, value, icon, color, column):
        """Create premium statistic card"""
        card = tk.Frame(
            parent,
            bg='white',
            relief='flat',
            highlightbackground=PremiumTheme.LIGHT_GRAY,
            highlightthickness=1
        )
        card.grid(row=column//3, column=column%3, padx=10, pady=10, sticky='nsew')
        
        # Icon with color
        icon_label = tk.Label(
            card,
            text=icon,
            font=("Segoe UI", 32),
            fg=color,
            bg='white'
        )
        icon_label.pack(pady=(20, 10))
        
        # Value
        value_label = tk.Label(
            card,
            text=str(value),
            font=("Segoe UI", 24, "bold"),
            fg=PremiumTheme.DARK,
            bg='white'
        )
        value_label.pack()
        
        # Title
        title_label = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 11),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg='white'
        )
        title_label.pack(pady=(5, 20))
    
    def create_action_card(self, parent, icon, text, command, color, column):
        """Create premium action card"""
        card = tk.Frame(
            parent,
            bg='white',
            relief='flat',
            highlightbackground=PremiumTheme.LIGHT_GRAY,
            highlightthickness=1,
            cursor='hand2'
        )
        card.grid(row=0, column=column, padx=10, pady=10, sticky='nsew')
        
        # Bind click event
        card.bind('<Button-1>', lambda e: command())
        
        # Icon
        icon_label = tk.Label(
            card,
            text=icon,
            font=("Segoe UI", 40),
            fg=color,
            bg='white'
        )
        icon_label.pack(pady=(30, 10))
        icon_label.bind('<Button-1>', lambda e: command())
        
        # Text
        text_label = tk.Label(
            card,
            text=text,
            font=("Segoe UI", 12, "bold"),
            fg=PremiumTheme.DARK,
            bg='white'
        )
        text_label.pack(pady=(0, 30))
        text_label.bind('<Button-1>', lambda e: command())
        
        # Hover effect
        def on_enter(e):
            card['bg'] = PremiumTheme.LIGHT_GRAY
            for child in card.winfo_children():
                try:
                    child['bg'] = PremiumTheme.LIGHT_GRAY
                except:
                    pass
        
        def on_leave(e):
            card['bg'] = 'white'
            for child in card.winfo_children():
                try:
                    child['bg'] = 'white'
                except:
                    pass
        
        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)
    
    def show_patients(self):
        """Show patient management view"""
        self.clear_content()
        self.set_header_title("Patient Management")
        PatientView(self.content_frame, self.controller)
    
    def show_doctors(self):
        """Show doctor management view"""
        self.clear_content()
        self.set_header_title("Doctor Management")
        DoctorView(self.content_frame, self.controller)
    
    def show_appointments(self):
        """Show appointments view"""
        self.clear_content()
        self.set_header_title("Appointment Scheduling")
        AppointmentView(self.content_frame, self.controller)
    
    def show_treatments(self):
        """Show treatments view"""
        self.clear_content()
        self.set_header_title("Treatment Records")
        TreatmentView(self.content_frame, self.controller)
    
    def show_billing(self):
        """Show billing view"""
        self.clear_content()
        self.set_header_title("Billing & Payments")
        BillingView(self.content_frame, self.controller)
    
    def show_reports(self):
        """Show reports view"""
        self.clear_content()
        self.set_header_title("Reports & Analytics")
        ReportView(self.content_frame, self.controller)
    
    def show_settings(self):
        """Show settings view"""
        self.clear_content()
        self.set_header_title("Settings")
        
        # Settings content
        settings_frame = tk.Frame(self.content_frame, bg=PremiumTheme.BACKGROUND)
        settings_frame.pack(fill='both', expand=True, pady=20)
        
        tk.Label(
            settings_frame,
            text="⚙️ System Settings",
            font=("Segoe UI", 18, "bold"),
            fg=PremiumTheme.DARK,
            bg=PremiumTheme.BACKGROUND
        ).pack(pady=20)
        
        # Settings options
        options = [
            ("Hospital Information", "🏥"),
            ("User Management", "👥"),
            ("Security Settings", "🔒"),
            ("Backup & Restore", "💾"),
            ("System Preferences", "⚙️")
        ]
        
        for text, icon in options:
            option_frame = tk.Frame(
                settings_frame,
                bg='white',
                relief='flat',
                highlightbackground=PremiumTheme.LIGHT_GRAY,
                highlightthickness=1
            )
            option_frame.pack(fill='x', padx=50, pady=5)
            
            tk.Label(
                option_frame,
                text=f"{icon}  {text}",
                font=("Segoe UI", 12),
                fg=PremiumTheme.DARK,
                bg='white'
            ).pack(side='left', padx=20, pady=15)
            
            tk.Label(
                option_frame,
                text="→",
                font=("Segoe UI", 14),
                fg=PremiumTheme.MEDIUM_GRAY,
                bg='white'
            ).pack(side='right', padx=20)
    
    def logout(self):
        """Handle logout with animation"""
        if messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?",
            icon='question'
        ):
            self.unbind_mousewheel()
            self.window.destroy()
            from views.login_view import LoginView
            from main import MediCareHospitalApp
            login = LoginView(MediCareHospitalApp().on_login_success)
            login.run()
    
    def run(self):
        """Start the main window"""
        self.window.mainloop()