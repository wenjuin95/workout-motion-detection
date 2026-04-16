from workout import workout_function
import datetime

class WorkoutController:
	def __init__(self, model, view):
		self.model = model
		self.view = view
		self.start_workout()

	""" open workout camera and record the reps, then it done it update to the database """
	def start_workout(self):
		self.view.hide()

		try:
			rep = self.model.get_reps_by_date(datetime.date.today().isoformat())
			if rep is not None:
				current_reps = int(rep)
			reps = workout_function()
			if (reps >= current_reps):
				self.model.set_reps(reps)
		finally:
			self.view.show()

		date = datetime.date.today().isoformat()
		self.view.set_status(
			f"Workout complete! You did {
				self.model.get_reps_by_date(date)
			} reps."
		)
