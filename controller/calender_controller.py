from calender import CalenderView

class CalendarController:
	def __init__(self, parent, model):
		self.model = model
		self.view = CalenderView(parent)
		self.load_data()

	""" load the workout data from the database and update the calendar view """
	def load_data(self):
		reps = self.model.get_all_workouts()

		for date_str, reps in reps.items():
			day = int(date_str.split("-")[2])  # get date
			month = int(date_str.split("-")[1])  # get month
			year = int(date_str.split("-")[0])  # get year
			self.view.set_day_value(day, month, year, reps)
