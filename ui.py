from tkinter import *
from workout import workout_function

def start_workout():
	window.withdraw()
	try:
		rep = workout_function()
	finally:
		window.deiconify()
		label.config(text=f"Workout complete! Total reps: {rep}")

window = Tk()
# scale according to system PPI
ppi = window.winfo_fpixels('1i')       # pixels per inch on this display
scale = max(1.0, ppi / 72.0)           # 72 is Tk's default PPI
window.tk.call('tk', 'scaling', scale)

# make window a fraction of the screen size
W = int(window.winfo_screenwidth() * 0.35)
H = int(window.winfo_screenheight() * 0.35)
window.geometry(f"{W}x{H}")

bgColor = "#2b2b2b"
fgColor = "#ffffff"
textFont = "Helvetica"

window.title("Workout Tracker")
window.configure(bg=bgColor)

# title label
label = Label(
	window,
	text="Welcome to Workout Tracker!",
	font=(textFont, 16),
	bg=bgColor,
	fg=fgColor
)
label.pack(pady=20)

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

window.mainloop()
