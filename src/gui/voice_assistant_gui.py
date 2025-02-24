import tkinter as tk
from tkinter import ttk
from typing import Optional

class VoiceAssistantGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voice Assistant")
        self.root.geometry("450x350")
        self.root.configure(bg='#2E3440')
        self.root.attributes('-topmost', True)

        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 450) // 2
        y = (screen_height - 350) // 2
        self.root.geometry(f"450x350+{x}+{y}")

        # Main frame with padding
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Header Section
        self.header_label = tk.Label(
            self.frame,
            text="Voice Assistant Interface",
            font=("Segoe UI", 14, "bold"),
            bg='#2E3440',
            fg='#88C0D0'
        )
        self.header_label.pack(pady=(0, 15))

        # Status Section
        self.status_label = tk.Label(
            self.frame,
            text="🔵 Listening for wake word...",
            font=("Segoe UI", 12),
            wraplength=400,
            bg='#3B4252',
            fg='#E5E9F0',
            relief=tk.SUNKEN,
            padx=10,
            pady=5
        )
        self.status_label.pack(fill='x', pady=10)

        # Detected Text Section
        self.detected_label = tk.Label(
            self.frame,
            text="",
            font=("Segoe UI", 10, "italic"),
            wraplength=400,
            bg='#2E3440',
            fg='#A3BE8C'
        )
        self.detected_label.pack(pady=10)

        # Response Section
        self.response_frame = ttk.LabelFrame(
            self.frame,
            text="Response",
            padding="5"
        )
        self.response_frame.pack(fill='both', expand=True, pady=10)

        self.response_text = tk.Text(
            self.response_frame,
            height=10,
            width=50,
            font=("Segoe UI", 10),
            wrap=tk.WORD,
            bg='#3B4252',
            fg='#E5E9F0',
            relief=tk.FLAT,
            borderwidth=1
        )
        self.response_text.pack(fill='both', expand=True)

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