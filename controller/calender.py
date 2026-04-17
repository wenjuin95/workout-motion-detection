import calendar
import datetime
from email.mime import text
import tkinter as tk

class CalenderView:
	def __init__(self, parent):
		self.parent = parent

		self.workout_data = {}
		self.day_labels = {}

		self.fgColor = "#ffffff"
		self.bgColor = "#2b2b2b"
		self.textFont = "Helvetica"
		self.exit_button_color = "#f44336"
		self.active_exit_button_color = "#d32f2f"

		# Initialize to current date
		now = datetime.datetime.now()
		self.current_year = now.year
		self.current_month = now.month

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
		#header for navigate
		header_frame = tk.Frame(self.top, bg=self.bgColor)
		header_frame.pack(fill="x", pady=10)

		# prev month
		tk.Button(
			header_frame,
			text=" < ",
			command=self.prev_month,
		).pack(side="left", padx=20)

		selectors_frame = tk.Frame(header_frame, bg=self.bgColor)
		selectors_frame.pack(side="left", expand=True)

		# Month Selector
		self.month_var = tk.StringVar(value=calendar.month_name[self.current_month])
		month_names = [calendar.month_name[i] for i in range(1, 13)]
		self.month_menu = tk.OptionMenu(
			selectors_frame, self.month_var, *month_names, command=self.on_date_select
		)
		self.month_menu.config(highlightthickness=0, indicatoron=0)
		self.month_menu["menu"].config(bg=self.bgColor, fg=self.fgColor)
		self.month_menu.pack(side="left", padx=5)

		# Year Selector (Range from 2026 to 2037, adjust as needed)
		self.year_var = tk.StringVar(value=str(self.current_year))
		years = [str(y) for y in range(2026, 2037)]
		self.year_menu = tk.OptionMenu(
			selectors_frame, self.year_var, *years, command=self.on_date_select
		)
		self.year_menu.config(highlightthickness=0, indicatoron=0)
		self.year_menu["menu"].config(bg=self.bgColor, fg=self.fgColor)
		self.year_menu.pack(side="left", padx=5)

		# next month
		tk.Button(
			header_frame,
			text=" > ",
			command=self.next_month
		).pack(side="right", padx=20)

		# grid frame
		self.grid_frame = tk.Frame(self.top, bg=self.bgColor)
		self.grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

		# initial draw
		self.draw_grid()

		# close button
		tk.Button(
			self.top,
			text="Close",
			command=self.close,
			bg=self.exit_button_color,
			fg=self.fgColor
		).pack(pady=10)

	def draw_grid(self):
		# clear existing grid
		for widget in self.grid_frame.winfo_children():
			widget.destroy()

		self.day_labels = {}

		# draw day headers
		headers = ["Mo","Tu","We","Th","Fr","Sa","Su"]
		for c, h in enumerate(headers):
			tk.Label(
				self.grid_frame,
				text=h,
				font=(self.textFont, 12, "bold"),
				fg=self.fgColor,
				bg=self.bgColor
			).grid(row=0, column=c, padx=2, pady=2, sticky="nsew")

		# draw dates
		weeks = calendar.monthcalendar(self.current_year, self.current_month)
		for r, week in enumerate(weeks, start=1):
			for c, day in enumerate(week):
				if day != 0:
					self.create_date_content(r, c, day)

	def create_date_content(self, r, c, day):
		lbl_bg = "#393939"

		cell = tk.Frame(self.grid_frame, bg=lbl_bg, bd=1, relief="solid",
						width=120, height=100)
		cell.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
		cell.grid_propagate(False)
		cell.pack_propagate(False)

		# config width/height to expand equally
		self.grid_frame.grid_columnconfigure(c, weight=1)
		self.grid_frame.grid_rowconfigure(r, weight=1)

		tk.Label(
			cell,
			text=str(day),
			font=(self.textFont, 9),
			bg=lbl_bg,
			fg=self.fgColor,
			anchor="w"
		).pack(fill="x", padx=4)

		# check for save workout data for this day
		saved_text = self.workout_data.get((self.current_year, self.current_month, day), "")
		content = tk.Label(
			cell,
			text=saved_text,
			font=(self.textFont, 20),
			bg=lbl_bg,
			fg="#4CAF50"
		)
		content.pack(expand=True, fill="both", padx=8, pady=8)

		self.day_labels[day] = content

	def on_date_select(self, *args):
		"""Called when dropdown values change."""
		# Convert month name back to number
		month_str = self.month_var.get()
		self.current_month = list(calendar.month_name).index(month_str)
		self.current_year = int(self.year_var.get())
		self.draw_grid()

	def update_selectors(self):
		"""Syncs the dropdowns with the current state (used by prev/next buttons)."""
		self.month_var.set(calendar.month_name[self.current_month])
		self.year_var.set(str(self.current_year))

	def prev_month(self):
		if self.current_month == 1:
			self.current_month = 12
			self.current_year -= 1
		else:
			self.current_month -= 1
		self.update_selectors()
		self.draw_grid()

	def next_month(self):
		if self.current_month == 12:
			self.current_month = 1
			self.current_year += 1
		else:
			self.current_month += 1
		self.update_selectors()
		self.draw_grid()

	def set_day_value(self, day, month, year, text):
		# 1. Save to the permanent dictionary
		self.workout_data[(year, month, day)] = text

		# 2. Update the UI only if the user is currently looking at that month
		if month == self.current_month and year == self.current_year:
			if day in self.day_labels:
				self.day_labels[day].config(text=text, fg="#4CAF50")

	def close(self):
		self.top.destroy()
		self.parent.deiconify()

def open_calender(parent):
	CalenderView(parent)
