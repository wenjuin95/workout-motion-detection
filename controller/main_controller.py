from workout import workout_function
from calender import CalenderView

# for control of my app

class MainController:
	def __init__(self, model, view):
		self.model = model
		self.view = view

		# Bind buttons
		self.view.start_btn.config(command=self.start_workout)
		self.view.daily_btn.config(command=self.open_calendar)

	def start_workout(self):
		self.view.hide()

		try:
			reps = workout_function()
			self.model.set_reps(reps)
		finally:
			self.view.show()

		self.view.set_status(
			f"Workout complete! You did {self.model.get_reps()} reps."
		)

	def open_calendar(self):
		CalendarController(self.view.root, self.model)

class CalendarController:
	def __init__(self, parent, model):
		self.model = model
		self.view = CalenderView(parent)
		# self.view.set_day_value(5, "15") # test value
		# self.load_data()


	def load_data(self):
		# get data from model
		workouts = self.model.get_all_workouts()

		for day, value in workouts.items():
			self.view.set_day_value(day, value)

def open_calender(parent, model):
	CalendarController(parent, model)
