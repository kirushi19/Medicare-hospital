import tkinter as tk

class Animations:
    """Class to handle all animations"""
    
    @staticmethod
    def fade_in(widget, duration=500):
        """Fade in animation"""
        def fade(step):
            if step <= 1.0:
                try:
                    widget.attributes('-alpha', step)
                except:
                    pass  # Some widgets don't support alpha
                widget.after(int(duration/20), lambda: fade(step + 0.05))
        
        try:
            fade(0.0)
        except:
            pass
    
    @staticmethod
    def fade_out(widget, duration=500, callback=None):
        """Fade out animation"""
        def fade(step):
            if step >= 0:
                try:
                    widget.attributes('-alpha', step)
                except:
                    pass
                if step > 0:
                    widget.after(int(duration/20), lambda: fade(step - 0.05))
                elif callback:
                    callback()
        
        try:
            fade(1.0)
        except:
            if callback:
                callback()
    
    @staticmethod
    def slide_in(widget, start_x, end_x, duration=500):
        """Slide in animation"""
        def slide(step):
            if step <= 1.0:
                x = start_x + (end_x - start_x) * step
                try:
                    widget.place(x=x)
                except:
                    pass
                widget.after(int(duration/20), lambda: slide(step + 0.05))
        
        try:
            slide(0.0)
        except:
            pass
    
    @staticmethod
    def pulse_button(widget, duration=1000):
        """Simple pulse animation for buttons (without gradient)"""
        try:
            original_bg = widget.cget('bg')
            
            def pulse(count):
                if count < 4:  # Reduced pulses for simplicity
                    if count % 2 == 0:
                        try:
                            widget.configure(bg='#ffffff')
                        except:
                            pass
                    else:
                        try:
                            widget.configure(bg=original_bg)
                        except:
                            pass
                    widget.after(int(duration/8), lambda: pulse(count + 1))
            
            pulse(0)
        except:
            pass  # Skip animation if fails
    
    @staticmethod
    def shake_widget(widget):
        """Shake animation for invalid input"""
        try:
            original_x = widget.winfo_x()
            
            def shake(count):
                if count < 6:
                    if count % 2 == 0:
                        try:
                            widget.place(x=original_x + 10)
                        except:
                            pass
                    else:
                        try:
                            widget.place(x=original_x - 10)
                        except:
                            pass
                    widget.after(50, lambda: shake(count + 1))
                else:
                    try:
                        widget.place(x=original_x)
                    except:
                        pass
            
            shake(0)
        except:
            pass  # Skip animation if widget doesn't support placement
    
    @staticmethod
    def loading_animation(label, text="Loading", duration=100):
        """Loading animation with dots"""
        dots = 0
        
        def animate():
            nonlocal dots
            dots = (dots + 1) % 4
            try:
                label.config(text=f"{text}{'.' * dots}")
                label.after(duration, animate)
            except:
                pass
        
        try:
            animate()
        except:
            pass