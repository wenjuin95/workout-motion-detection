from tkinter import *
from workout import workout_function

window = Tk()
window.geometry("400x300")
window.title("Workout Tracker")

window.configure(bg="#2b2b2b")

label = Label(
	window,
	text="Welcome to Workout Tracker!",
	font=("Helvetica", 16),
	bg="#2b2b2b",
	fg="#ffffff"
)
label.pack(pady=20)

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
