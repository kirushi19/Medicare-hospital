# Ultra Premium Theme Configuration - FIXED (Added get_gradient method)
class PremiumTheme:
    # Premium Color Palette - Modern & Luxurious
    PRIMARY = "#1a237e"      # Deep Indigo
    SECONDARY = "#0d47a1"    # Dark Blue
    ACCENT = "#00b0ff"       # Bright Azure
    SUCCESS = "#00c853"       # Vibrant Green
    WARNING = "#ffd600"       # Gold
    DANGER = "#d50000"        # Rich Red
    INFO = "#00b8d4"          # Cyan
    PURPLE = "#6200ea"        # Deep Purple
    WHITE = "#ffffff"         # White
    
    # Neutral Colors
    DARK = "#282860"          # Dark Navy
    DARK_GRAY = "#2c2c3a"      # Charcoal
    MEDIUM_GRAY = "#4a4a5a"    # Slate
    LIGHT_GRAY = "#6b6b7e"     # Gray Blue
    BACKGROUND = "#ffffff"     # Off White
    CARD_BG = "#ffffff"        # Pure White
    SURFACE = "#f8f9ff"        # Light Surface
    BORDER = "#e0e0e0"         # Border color
    
    # Font Family - Modern Stack
    FONT_FAMILY = "Segoe UI"
    
    # Font Sizes - Professional Typography Scale
    TITLE_SIZE = 32
    HEADING1_SIZE = 24
    HEADING2_SIZE = 20
    SUBHEADING_SIZE = 16
    BODY_SIZE = 13
    SMALL_SIZE = 11
    
    # Font Weights
    TITLE_FONT = (FONT_FAMILY, TITLE_SIZE, "bold")
    HEADING1_FONT = (FONT_FAMILY, HEADING1_SIZE, "bold")
    HEADING2_FONT = (FONT_FAMILY, HEADING2_SIZE, "bold")
    SUBHEADING_FONT = (FONT_FAMILY, SUBHEADING_SIZE, "bold")
    NORMAL_FONT = (FONT_FAMILY, BODY_SIZE)
    SMALL_FONT = (FONT_FAMILY, SMALL_SIZE)
    
    # Button Styles - Modern & Sleek
    BUTTON_PRIMARY = {
        'font': NORMAL_FONT,
        'bg': PRIMARY,
        'fg': 'white',
        'activebackground': SECONDARY,
        'activeforeground': 'white',
        'relief': 'flat',
        'borderwidth': 0,
        'cursor': 'hand2',
        'padx': 25,
        'pady': 12
    }
    
    BUTTON_SUCCESS = {
        'font': NORMAL_FONT,
        'bg': SUCCESS,
        'fg': 'white',
        'activebackground': '#00a844',
        'activeforeground': 'white',
        'relief': 'flat',
        'borderwidth': 0,
        'cursor': 'hand2',
        'padx': 25,
        'pady': 12
    }
    
    BUTTON_DANGER = {
        'font': NORMAL_FONT,
        'bg': DANGER,
        'fg': 'white',
        'activebackground': '#b71c1c',
        'activeforeground': 'white',
        'relief': 'flat',
        'borderwidth': 0,
        'cursor': 'hand2',
        'padx': 25,
        'pady': 12
    }
    
    # Card Style
    CARD_STYLE = {
        'bg': CARD_BG,
        'relief': 'flat',
        'borderwidth': 0,
        'highlightthickness': 1,
        'highlightbackground': BORDER
    }
    
    # Entry Style
    ENTRY_STYLE = {
        'font': NORMAL_FONT,
        'relief': 'solid',
        'borderwidth': 1,
        'bg': SURFACE,
        'fg': DARK,
        'insertbackground': PRIMARY,
        'selectbackground': ACCENT,
        'selectforeground': 'white'
    }
    
    @classmethod
    def get_gradient(cls, color1, color2, steps=10):
        """Generate gradient colors between two colors"""
        try:
            # Simple gradient generation without external dependencies
            def hex_to_rgb(hex_color):
                hex_color = hex_color.lstrip('#')
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
            def rgb_to_hex(rgb):
                return '#{:02x}{:02x}{:02x}'.format(
                    min(255, max(0, int(rgb[0]))),
                    min(255, max(0, int(rgb[1]))),
                    min(255, max(0, int(rgb[2])))
                )
            
            rgb1 = hex_to_rgb(color1)
            rgb2 = hex_to_rgb(color2)
            
            gradient = []
            for i in range(steps):
                ratio = i / (steps - 1) if steps > 1 else 0
                r = rgb1[0] + (rgb2[0] - rgb1[0]) * ratio
                g = rgb1[1] + (rgb2[1] - rgb1[1]) * ratio
                b = rgb1[2] + (rgb2[2] - rgb1[2]) * ratio
                gradient.append(rgb_to_hex((r, g, b)))
            
            return gradient
        except Exception:
            # Return simple list if gradient generation fails
            return [color1, color2]