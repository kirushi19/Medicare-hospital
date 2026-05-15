import tkinter as tk
from tkinter import messagebox
from utils.theme import PremiumTheme
from utils.animations import Animations

class LoginView:
    """Ultra Premium Login Window with Modern Design"""
    
    def __init__(self, on_login_success):
        self.on_login_success = on_login_success
        self.window = tk.Tk()
        self.window.title("Medi Care Hospital - Premium Edition")
        self.window.geometry("1200x700")
        self.window.configure(bg=PremiumTheme.BACKGROUND)
        
        # Center window
        self.center_window()
        
        # Remove window decorations for ultra-modern look
        self.window.overrideredirect(True)
        
        # Bind events for window dragging
        self.window.bind('<Button-1>', self.start_move)
        self.window.bind('<B1-Motion>', self.on_move)
        
        self.setup_ui()
        Animations.fade_in(self.window, 800)
    
    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
    
    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.window.winfo_x() + deltax
        y = self.window.winfo_y() + deltay
        self.window.geometry(f"+{x}+{y}")
    
    def setup_ui(self):
        # Main container with gradient effect
        self.main_container = tk.Frame(self.window, bg=PremiumTheme.BACKGROUND)
        self.main_container.pack(fill='both', expand=True)
        
        # Left Panel - Branding Area
        left_panel = tk.Frame(
            self.main_container,
            bg=PremiumTheme.PRIMARY,
            width=500
        )
        left_panel.pack(side='left', fill='both', expand=True)
        left_panel.pack_propagate(False)
        
        # Premium Medical Icon
        canvas = tk.Canvas(
            left_panel,
            width=200,
            height=200,
            bg=PremiumTheme.PRIMARY,
            highlightthickness=0
        )
        canvas.pack(pady=(100, 20))
        
        # Draw medical cross with gradient
        self.draw_medical_cross(canvas)
        
        # Brand Text
        brand_label = tk.Label(
            left_panel,
            text="MEDI CARE",
            font=("Segoe UI", 48, "bold"),
            fg='white',
            bg=PremiumTheme.PRIMARY
        )
        brand_label.pack()
        
        tagline_label = tk.Label(
            left_panel,
            text="Premium Healthcare Management System",
            font=("Segoe UI", 14),
            fg='#cccccc',
            bg=PremiumTheme.PRIMARY
        )
        tagline_label.pack(pady=(10, 0))
        
        # Statistics
        stats_frame = tk.Frame(left_panel, bg=PremiumTheme.PRIMARY)
        stats_frame.pack(pady=(50, 0))
        
        stats = [
            ("8,000+", "Annual Patients"),
            ("24/7", "Emergency Care"),
            ("100%", "Secure")
        ]
        
        for i, (value, label) in enumerate(stats):
            stat = tk.Frame(stats_frame, bg=PremiumTheme.PRIMARY)
            stat.grid(row=0, column=i, padx=30)
            
            tk.Label(
                stat,
                text=value,
                font=("Segoe UI", 20, "bold"),
                fg='white',
                bg=PremiumTheme.PRIMARY
            ).pack()
            
            tk.Label(
                stat,
                text=label,
                font=("Segoe UI", 11),
                fg='#cccccc',
                bg=PremiumTheme.PRIMARY
            ).pack()
        
        # Right Panel - Login Form
        right_panel = tk.Frame(
            self.main_container,
            bg=PremiumTheme.CARD_BG,
            width=500
        )
        right_panel.pack(side='right', fill='both', expand=True)
        right_panel.pack_propagate(False)
        
        # Close Button
        close_btn = tk.Button(
            right_panel,
            text="✕",
            font=("Segoe UI", 16),
            bg=PremiumTheme.CARD_BG,
            fg=PremiumTheme.MEDIUM_GRAY,
            activebackground=PremiumTheme.DANGER,
            activeforeground='white',
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            command=self.window.quit
        )
        close_btn.place(x=450, y=20)
        
        # Login Form Container
        form_container = tk.Frame(right_panel, bg=PremiumTheme.CARD_BG)
        form_container.pack(expand=True, padx=60, pady=60)
        
        # Welcome Back
        tk.Label(
            form_container,
            text="Welcome Back!",
            font=("Segoe UI", 32, "bold"),
            fg=PremiumTheme.DARK,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w')
        
        tk.Label(
            form_container,
            text="Please sign in to access the system",
            font=("Segoe UI", 12),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w', pady=(5, 40))
        
        # Username Field
        tk.Label(
            form_container,
            text="USERNAME",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w')
        
        username_frame = tk.Frame(
            form_container,
            bg=PremiumTheme.SURFACE,
            highlightbackground=PremiumTheme.ACCENT,
            highlightthickness=1
        )
        username_frame.pack(fill='x', pady=(5, 20))
        
        tk.Label(
            username_frame,
            text="👤",
            font=("Segoe UI", 14),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.MEDIUM_GRAY
        ).pack(side='left', padx=10)
        
        self.username_entry = tk.Entry(
            username_frame,
            font=("Segoe UI", 12),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='flat',
            borderwidth=0,
            insertbackground=PremiumTheme.ACCENT
        )
        self.username_entry.pack(side='left', fill='x', expand=True, padx=10, pady=12)
        self.username_entry.insert(0, "admin")
        
        # Password Field
        tk.Label(
            form_container,
            text="PASSWORD",
            font=("Segoe UI", 10, "bold"),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(anchor='w')
        
        password_frame = tk.Frame(
            form_container,
            bg=PremiumTheme.SURFACE,
            highlightbackground=PremiumTheme.ACCENT,
            highlightthickness=1
        )
        password_frame.pack(fill='x', pady=(5, 30))
        
        tk.Label(
            password_frame,
            text="🔒",
            font=("Segoe UI", 14),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.MEDIUM_GRAY
        ).pack(side='left', padx=10)
        
        self.password_entry = tk.Entry(
            password_frame,
            font=("Segoe UI", 12),
            bg=PremiumTheme.SURFACE,
            fg=PremiumTheme.DARK,
            relief='flat',
            borderwidth=0,
            insertbackground=PremiumTheme.ACCENT,
            show="•"
        )
        self.password_entry.pack(side='left', fill='x', expand=True, padx=10, pady=12)
        self.password_entry.insert(0, "admin")
        
        # Remember me & Forgot Password
        options_frame = tk.Frame(form_container, bg=PremiumTheme.CARD_BG)
        options_frame.pack(fill='x', pady=(0, 30))
        
        self.remember_var = tk.BooleanVar()
        remember_check = tk.Checkbutton(
            options_frame,
            text="Remember me",
            variable=self.remember_var,
            bg=PremiumTheme.CARD_BG,
            fg=PremiumTheme.MEDIUM_GRAY,
            selectcolor=PremiumTheme.CARD_BG,
            activebackground=PremiumTheme.CARD_BG,
            font=("Segoe UI", 11)
        )
        remember_check.pack(side='left')
        
        forgot_btn = tk.Label(
            options_frame,
            text="Forgot Password?",
            font=("Segoe UI", 11, "underline"),
            fg=PremiumTheme.ACCENT,
            bg=PremiumTheme.CARD_BG,
            cursor='hand2'
        )
        forgot_btn.pack(side='right')
        
        # Login Button
        login_btn = tk.Button(
            form_container,
            text="SIGN IN",
            font=("Segoe UI", 14, "bold"),
            bg=PremiumTheme.PRIMARY,
            fg='white',
            activebackground=PremiumTheme.SECONDARY,
            activeforeground='white',
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            height=2,
            command=self.login
        )
        login_btn.pack(fill='x', pady=(0, 20))
        
        # Hover effect for login button
        def on_enter(e):
            login_btn['bg'] = PremiumTheme.SECONDARY
        
        def on_leave(e):
            login_btn['bg'] = PremiumTheme.PRIMARY
        
        login_btn.bind('<Enter>', on_enter)
        login_btn.bind('<Leave>', on_leave)
        
        # Sign up link
        signup_frame = tk.Frame(form_container, bg=PremiumTheme.CARD_BG)
        signup_frame.pack()
        
        tk.Label(
            signup_frame,
            text="Don't have an account? ",
            font=("Segoe UI", 11),
            fg=PremiumTheme.MEDIUM_GRAY,
            bg=PremiumTheme.CARD_BG
        ).pack(side='left')
        
        signup_link = tk.Label(
            signup_frame,
            text="Contact Administrator",
            font=("Segoe UI", 11, "bold"),
            fg=PremiumTheme.PRIMARY,
            bg=PremiumTheme.CARD_BG,
            cursor='hand2'
        )
        signup_link.pack(side='left')
        
        # Bind Enter key
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.login())
    
    def draw_medical_cross(self, canvas):
        """Draw premium medical cross icon"""
        # Draw outer circle
        canvas.create_oval(50, 50, 150, 150, fill='white', outline='white')
        
        # Draw cross
        canvas.create_rectangle(85, 70, 115, 130, fill=PremiumTheme.ACCENT, outline=PremiumTheme.ACCENT)
        canvas.create_rectangle(70, 85, 130, 115, fill=PremiumTheme.ACCENT, outline=PremiumTheme.ACCENT)
        
        # Add shine effect
        canvas.create_oval(120, 60, 140, 80, fill='#ffffff', outline='')
    
    def login(self):
        """Handle login with animation"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "admin" and password == "admin":
            # Success animation - simplified
            self.window.after(500, self.close_and_proceed)
        else:
            # Error animation
            Animations.shake_widget(self.username_entry)
            Animations.shake_widget(self.password_entry)
            messagebox.showerror(
                "Authentication Failed",
                "Invalid username or password.\nPlease try again."
            )
    
    def close_and_proceed(self):
        """Close login and open main window"""
        self.window.destroy()
        self.on_login_success()
    
    def run(self):
        """Start the login window"""
        self.window.mainloop()