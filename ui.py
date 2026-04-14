from tkinter import *
from workout import workout_function
from calender import open_calender

def start_workout():
	window.withdraw()
	try:
		rep = workout_function()
	finally:
		window.deiconify()
		status_label.config(text=f"Workout complete! You did {rep} reps.")

window = Tk()

# scale according to system PPI
ppi = window.winfo_fpixels('1i')       # pixels per inch on this display
scale = max(1.0, ppi / 72.0)           # 72 is Tk's default PPI
window.tk.call('tk', 'scaling', scale)

# make window a fraction of the screen size
W = int(window.winfo_screenwidth() * 0.35)
H = int(window.winfo_screenheight() * 0.35)
window.geometry(f"{W}x{H}")
window.attributes("-type", "dialog")  # make it a dialog window (no maximize/minimize)

bgColor = "#2b2b2b"
fgColor = "#ffffff"
textFont = "Helvetica"

window.title("Workout Tracker")
window.configure(bg=bgColor)

# title label
label = Label(
	window,
	text="Welcome to Workout Tracker!",
	font=(textFont, 20),
	bg=bgColor,
	fg=fgColor
)
label.pack(pady=20)

# status label
status_label = Label(
		window,
		text="",
		font=(textFont, 14),
		bg=bgColor,
		fg=fgColor
	)
status_label.pack(pady=20)

# button to start workout
button = Button(
	window,
	text="Start Workout",
	font=(textFont, 14),
	bg="#4CAF50",
	fg=fgColor,
	activebackground="#419644",
	activeforeground=fgColor,
	width=20,
	height=2,
	command=start_workout
)
button.pack(pady=10)

button_daily_check = Button(
	window,
	text="Daily Check",
	font=(textFont, 14),
	bg="#2196F3",
	fg=fgColor,
	activebackground="#1976D2",
	activeforeground=fgColor,
	width=20,
	height=2,
	command=lambda: open_calender(window)
)
button_daily_check.pack(pady=10)

# exit button
button_exit = Button(
	window,
	text="Exit",
	font=(textFont, 14),
	bg="#f44336",
	fg=fgColor,
	activebackground="#d32f2f",
	activeforeground=fgColor,
	width=20,
	height=2,
	command=window.destroy
)
button_exit.pack(pady=10)

window.mainloop()
