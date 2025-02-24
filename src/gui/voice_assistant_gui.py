import tkinter as tk
from tkinter import ttk
from typing import Optional

class VoiceAssistantGUI:
    def __init__(self):
        # Color scheme
        self.COLORS = {
            'bg_dark': '#1E1E1E',
            'bg_light': '#252526',
            'accent': '#007ACC',
            'text': '#D4D4D4',
            'success': '#6A9955',
            'highlight': '#264F78'
        }

        self.root = tk.Tk()
        self.root.title("Helix Helper")
        self.root.geometry("600x400")
        self.root.configure(bg=self.COLORS['bg_dark'])
        self.root.attributes('-topmost', True)

        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 400) // 2
        self.root.geometry(f"600x400+{x}+{y}")

        # Configure style
        style = ttk.Style()
        style.configure('Custom.TFrame', background=self.COLORS['bg_dark'])
        style.configure('Custom.TLabelframe', background=self.COLORS['bg_dark'])
        style.configure('Custom.TLabelframe.Label', background=self.COLORS['bg_dark'], 
                       foreground=self.COLORS['accent'])

        # Main container
        self.container = ttk.Frame(self.root, style='Custom.TFrame')
        self.container.pack(expand=True, fill='both', padx=15, pady=15)

        # Header
        self.header_label = tk.Label(
            self.container,
            text="Helix Helper",
            font=("Segoe UI", 24, "bold"),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['accent']
        )
        self.header_label.pack(pady=(0, 20))

        # Status indicator
        self.status_frame = tk.Frame(
            self.container,
            bg=self.COLORS['bg_light'],
            relief='flat',
            bd=1
        )
        self.status_frame.pack(fill='x', pady=(0, 15))
        
        self.status_label = tk.Label(
            self.status_frame,
            text="🔵 Listening for wake word...",
            font=("Segoe UI", 12),
            bg=self.COLORS['bg_light'],
            fg=self.COLORS['text'],
            pady=10
        )
        self.status_label.pack(fill='x')

        # Detected text
        self.detected_label = tk.Label(
            self.container,
            text="",
            font=("Segoe UI", 11, "italic"),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['success'],
            wraplength=550
        )
        self.detected_label.pack(pady=(0, 15))

        # Response area
        self.response_frame = ttk.LabelFrame(
            self.container,
            text=" Response ",
            style='Custom.TLabelframe'
        )
        self.response_frame.pack(fill='both', expand=True)

        # Custom text widget with modern scrollbar
        self.response_text = tk.Text(
            self.response_frame,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            bg=self.COLORS['bg_light'],
            fg=self.COLORS['text'],
            relief='flat',
            padx=10,
            pady=10,
            borderwidth=0,
            insertbackground=self.COLORS['accent']  # Cursor color
        )
        self.response_text.pack(side='left', fill='both', expand=True)

        # Modern scrollbar
        scrollbar = ttk.Scrollbar(self.response_frame, orient='vertical', 
                                command=self.response_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.response_text.configure(yscrollcommand=scrollbar.set)

        # Configure tag for highlighting
        self.response_text.tag_configure('highlight', background=self.COLORS['highlight'])

    def update_status(self, text: str, icon: str = "🔵") -> None:
        self.status_label.config(text=f"{icon} {text}")
        self.root.update()

    def update_detected(self, text: Optional[str]) -> None:
        self.detected_label.config(text=f"Detected: {text}" if text else "")
        self.root.update()

    def update_response(self, text: str) -> None:
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(tk.END, text)
        self.root.update()

    def start(self) -> None:
        self.root.mainloop()

    def stop(self) -> None:
        self.root.destroy()
