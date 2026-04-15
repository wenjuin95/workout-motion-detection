import calendar
import datetime
import tkinter as tk

# def open_calender(parent):
# 	fgColor = "#ffffff"
# 	bgColor = "#2b2b2b"
# 	textFont = "Helvetica"

# 	# create a new window for the calendar
# 	top = tk.Toplevel(parent)
# 	top.title("Workout Calendar")
# 	top.configure(bg=bgColor)
# 	top.resizable(False, False)

# 	# Get the current year and month
# 	now = datetime.datetime.now()
# 	year = now.year
# 	month = now.month

# 	# Month-Year label
# 	labelMonthYear = tk.Label(
# 		top,
# 		text=f"{calendar.month_name[month]} {year}",
# 		font=(textFont, 16),
# 		bg=bgColor,
# 		fg=fgColor,
# 		anchor="center",
# 		justify="center"
# 	)
# 	labelMonthYear.pack(pady=10)

# 	# hide the main window while calendar is open
# 	parent.withdraw()

# 	# grid frame
# 	grid_frame = tk.Frame(top, bg=bgColor)
# 	grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# 	# label days of the week
# 	headers = ["Mo","Tu","We","Th","Fr","Sa","Su"]
# 	for c, h in enumerate(headers):
# 		hdr = tk.Label(grid_frame, text=h, font=(textFont, 12, "bold"), fg=fgColor, bg=bgColor)
# 		hdr.grid(row=0, column=c, padx=2, pady=2, sticky="nsew")

# 	# build month as grid using calendar.monthcalendar
# 	weeks = calendar.monthcalendar(year, month)
# 	day_labels = {}
# 	for r, week in enumerate(weeks, start=1):
# 		for c, day in enumerate(week):
# 			# if day is 0 then create empty cell
# 			if day == 0:
# 				cell = tk.Frame(grid_frame, bd=1, bg=bgColor,relief="solid")
# 				cell.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
# 			else:
# 				# cell frame with two labels: date (left) and content (center)
# 				lbl_bg = "#393939"
# 				cell = tk.Frame(grid_frame, bg=lbl_bg, bd=1, relief="solid")
# 				cell.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

# 				# date
# 				date_lbl = tk.Label(cell, text=str(day), font=(textFont, 9), bg=lbl_bg, fg=fgColor, anchor="w", justify="left")
# 				date_lbl.pack(fill="x", padx=4, pady=(2,0))

# 				# content
# 				content_lbl = tk.Label(cell, text="", font=(textFont, 20), bg=lbl_bg, fg=fgColor, anchor="center", justify="center")
# 				content_lbl.pack(expand=True, fill="both", padx=8, pady=8)

# 				day_labels[day] = content_lbl

# 	# configure grid weights for responsiveness
# 	for c in range(7):
# 		grid_frame.grid_columnconfigure(c, weight=1, uniform="col")
# 	for r in range(len(weeks) + 1):
# 		grid_frame.grid_rowconfigure(r, weight=1, uniform="row")

# 	# helper to set a day's value later
# 	def set_day_value(day_num, value_text):
# 		lbl = day_labels.get(day_num)
# 		if lbl:
# 			lbl.config(text=value_text, fg="#4CAF50")

# 	set_day_value(5, "15 reps")

# 	# exit button
# 	button_exit = tk.Button(
# 		top,
# 		text="Close",
# 		font=(textFont, 14),
# 		bg="#f44336",
# 		fg=fgColor,
# 		activebackground="#d32f2f",
# 		activeforeground=fgColor,
# 		width=20,
# 		height=2,
# 		command= {
# 			top.destroy,
# 			parent.deiconify
# 		}
# 	)
# 	button_exit.pack(pady=10)
# 	top.protocol("WM_DELETE_WINDOW", {
# 		top.destroy,
# 		parent.deiconify
# 	})

class CalenderView:
	def __init__(self, parent):
		self.parent = parent

		self.fgColor = "#ffffff"
		self.bgColor = "#2b2b2b"
		self.textFont = "Helvetica"

		self.day_labels = {}

		self.create_window()
		self.build_calendar()

	def create_window(self):
		self.top = tk.Toplevel(self.parent)
		self.top.title("Workout Calendar")
		self.top.configure(bg=self.bgColor)
		self.top.resizable(False, False)

		self.parent.withdraw()

		self.top.protocol("WM_DELETE_WINDOW", self.close)

	def build_calendar(self):
		now = datetime.datetime.now()
		year = now.year
		month = now.month

		self.top.geometry("700x600")

		# Title
		label = tk.Label(
			self.top,
			text=f"{calendar.month_name[month]} {year}",
			font=(self.textFont, 16),
			bg=self.bgColor,
			fg=self.fgColor
		)
		label.pack(pady=10)

		# Grid frame
		self.grid_frame = tk.Frame(self.top, bg=self.bgColor)
		self.grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

		headers = ["Mo","Tu","We","Th","Fr","Sa","Su"]
		for c, h in enumerate(headers):
			tk.Label(
				self.grid_frame,
				text=h,
				font=(self.textFont, 12, "bold"),
				fg=self.fgColor,
				bg=self.bgColor
			).grid(row=0, column=c, padx=2, pady=2, sticky="nsew")

		weeks = calendar.monthcalendar(year, month)

		for r, week in enumerate(weeks, start=1):
			for c, day in enumerate(week):
				if day == 0:
					tk.Frame(self.grid_frame, bg=self.bgColor, bd=1).grid(
						row=r, column=c, padx=2, pady=2, sticky="nsew"
					)
				else:
					self.create_day_cell(r, c, day)

		# Close button
		tk.Button(
			self.top,
			text="Close",
			command=self.close
		).pack(pady=10)

	def create_day_cell(self, r, c, day):
		lbl_bg = "#393939"

		cell = tk.Frame(self.grid_frame, bg=lbl_bg, bd=1, relief="solid",
						width=100, height=80)
		cell.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
		cell.grid_propagate(False)
		cell.pack_propagate(False)

		for c in range(7):
			self.grid_frame.grid_columnconfigure(c, weight=1)

		for r in range(6):
			self.grid_frame.grid_rowconfigure(r, weight=1)

		tk.Label(
			cell,
			text=str(day),
			font=(self.textFont, 9),
			bg=lbl_bg,
			fg=self.fgColor,
			anchor="w"
		).pack(fill="x", padx=4)

		content = tk.Label(
			cell,
			text="",
			font=(self.textFont, 20),
			bg=lbl_bg,
			fg=self.fgColor
		)
		content.pack(expand=True, fill="both", padx=8, pady=8)

		self.day_labels[day] = content

	def set_day_value(self, day, text):
		if day in self.day_labels:
			self.day_labels[day].config(text=text, fg="#4CAF50")

	def close(self):
		self.top.destroy()
		self.parent.deiconify()

def open_calender(parent):
	CalenderView(parent)
