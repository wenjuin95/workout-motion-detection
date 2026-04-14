import calendar
import datetime
import tkinter as tk
from tkinter import ttk

def open_calender(parent):
	fgColor = "#ffffff"
	bgColor = "#2b2b2b"
	textFont = "Helvetica"

	# create a new window for the calendar
	top = tk.Toplevel(parent)
	top.title("Workout Calendar")
	top.configure(bg=bgColor)

	# Get the current year and month
	now = datetime.datetime.now()
	year = now.year
	month = now.month

	# Month-Year label
	labelMonthYear = tk.Label(
		top,
		text=f"{calendar.month_name[month]} {year}",
		font=(textFont, 16),
		bg=bgColor,
		fg=fgColor,
		anchor="center",
		justify="center"
	)
	labelMonthYear.pack(pady=10)

	# hide the main window while calendar is open
	parent.withdraw()

	# grid frame
	grid_frame = tk.Frame(top, bg=bgColor)
	grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

	# label days of the week
	headers = ["Mo","Tu","We","Th","Fr","Sa","Su"]
	for c, h in enumerate(headers):
		hdr = tk.Label(grid_frame, text=h, font=(textFont, 12, "bold"), fg=fgColor, bg=bgColor)
		hdr.grid(row=0, column=c, padx=2, pady=2, sticky="nsew")

	# build month as grid using calendar.monthcalendar
	weeks = calendar.monthcalendar(year, month)
	day_labels = {}
	for r, week in enumerate(weeks, start=1):
		for c, day in enumerate(week):
			# if day is 0 then create empty cell
			if day == 0:
				cell = tk.Frame(grid_frame, bd=1, bg=bgColor,relief="solid")
				cell.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
			else:
				# cell frame with two labels: date (left) and content (center)
				lbl_bg = "#393939"
				cell = tk.Frame(grid_frame, bg=lbl_bg, bd=1, relief="solid")
				cell.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

				# date
				date_lbl = tk.Label(cell, text=str(day), font=(textFont, 10), bg=lbl_bg, fg=fgColor, anchor="w", justify="left")
				date_lbl.pack(fill="x", padx=4, pady=(2,0))

				# content
				content_lbl = tk.Label(cell, text="", font=(textFont, 11), bg=lbl_bg, fg=fgColor, anchor="center", justify="center")
				content_lbl.pack(expand=True, fill="both", padx=4, pady=(0,4))

				day_labels[day] = content_lbl

	# configure grid weights for responsiveness
	for c in range(7):
		grid_frame.grid_columnconfigure(c, weight=1, uniform="col")
	for r in range(len(weeks) + 1):
		grid_frame.grid_rowconfigure(r, weight=1, uniform="row")

	# helper to set a day's value later
	def set_day_value(day_num, value_text):
		lbl = day_labels.get(day_num)
		if lbl:
			lbl.config(text=value_text, fg="#4CAF50")

	set_day_value(5, "Today")

	# exit button callback
	def on_close():
		top.destroy()
		parent.deiconify()

	# exit button
	button_exit = tk.Button(
		top,
		text="Close",
		font=(textFont, 14),
		bg="#f44336",
		fg=fgColor,
		activebackground="#d32f2f",
		activeforeground=fgColor,
		width=20,
		height=2,
		command=on_close
	)
	button_exit.pack(pady=10)
	top.protocol("WM_DELETE_WINDOW", on_close)
