from tkinter import *
from workout import workout_function

window = Tk()
# scale according to system PPI
ppi = window.winfo_fpixels('1i')       # pixels per inch on this display
scale = max(1.0, ppi / 72.0)           # 72 is Tk's default PPI
window.tk.call('tk', 'scaling', scale)

# make window a fraction of the screen size
W = int(window.winfo_screenwidth() * 0.35)
H = int(window.winfo_screenheight() * 0.35)
window.geometry(f"{W}x{H}")

window.title("Workout Tracker")
window.configure(bg="#2b2b2b")

# title label
label = Label(
	window,
	text="Welcome to Workout Tracker!",
	font=("Helvetica", 16),
	bg="#2b2b2b",
	fg="#ffffff"
)
label.pack(pady=20)

# button to start workout
button = Button(
	window,
	text="Start Workout",
	font=("Helvetica", 14),
	bg="#4CAF50",
	fg="#ffffff",
	activebackground="#419644",
	activeforeground="#ffffff",
	width=20,
	height=2,
	command=workout_function
)
button.pack(pady=10)

# exit button
button_exit = Button(
	window,
	text="Exit",
	font=("Helvetica", 14),
	bg="#f44336",
	fg="#ffffff",
	activebackground="#d32f2f",
	activeforeground="#ffffff",
	width=20,
	height=2,
	command=window.destroy
)
button_exit.pack(pady=10)

window.mainloop()
