from tkinter import *

#for UI of my app

bgColor = "#2b2b2b"
fgColor = "#ffffff"
textFont = "Helvetica"

start_button_color = "#4CAF50"
hover_start_button_color = "#419644"
daily_check_button_color = "#2196F3"
hover_daily_check_button_color = "#1976D2"
exit_button_color = "#f44336"
hover_exit_button_color = "#d32f2f"

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Workout Tracker")
        self.root.configure(bg=bgColor)

        self._setup_window()

        # Header
        Label(
            root,
            text="Welcome to Workout Tracker!",
            font=(textFont, 20),
            bg=bgColor,
            fg=fgColor
        ).pack(pady=20)

        # Status label
        self.status_label = Label(
            root,
            text="",
            font=(textFont, 14),
            bg=bgColor,
            fg=fgColor
        )
        self.status_label.pack(pady=20)

        # Buttons (commands set later by controller)
        self.start_btn = Button(
            root,
            text="Start Workout",
            font=(textFont, 14),
            bg=start_button_color,
            fg=fgColor,
            width=20,
            height=2
        )
        self.start_btn.pack(pady=10)

        self.daily_btn = Button(
            root,
            text="Daily Check",
            font=(textFont, 14),
            bg=daily_check_button_color,
            fg=fgColor,
            width=20,
            height=2
        )
        self.daily_btn.pack(pady=10)

        self.exit_btn = Button(
            root,
            text="Exit",
            font=(textFont, 14),
            bg=exit_button_color,
            fg=fgColor,
            width=20,
            height=2,
            command=root.destroy
        )
        self.exit_btn.pack(pady=10)

    def _setup_window(self):
        ppi = self.root.winfo_fpixels('1i')
        scale = max(1.0, ppi / 72.0)
        self.root.tk.call('tk', 'scaling', scale)

        W = int(self.root.winfo_screenwidth() * 0.35)
        H = int(self.root.winfo_screenheight() * 0.35)
        self.root.geometry(f"{W}x{H}")
        self.root.resizable(False, False)

    # Methods controller will use
    def set_status(self, text):
        self.status_label.config(text=text)

    def hide(self):
        self.root.withdraw()

    def show(self):
        self.root.deiconify()
