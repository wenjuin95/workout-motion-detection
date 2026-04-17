from controller.workout import workout_function
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

		if reps < 10:
			comment = "(why stop? you can do more!)"
		elif reps > 10:
			comment = "(amazing! you are doing great!)"
		elif reps > 20:
			comment = "(good job! take a rest and keep going!)"

		date = datetime.date.today().isoformat()
		self.view.set_status(
			f"Total: {self.model.get_reps_by_date(date)} reps\n You did {
				reps
			} reps.\n {comment}"
		)
