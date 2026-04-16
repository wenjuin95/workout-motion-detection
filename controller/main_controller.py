from controller.workout_controller import WorkoutController
from controller.calender_controller import CalendarController
# for control of my app

class MainController:
	def __init__(self, model, view):
		self.model = model
		self.view = view

		# Bind buttons
		self.view.start_btn.config(command=self.start_workout)
		self.view.daily_btn.config(command=self.open_calendar)

	def start_workout(self):
		WorkoutController(self.model, self.view)

	def open_calendar(self):
		CalendarController(self.view.root, self.model)
