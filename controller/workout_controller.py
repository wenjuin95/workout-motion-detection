from workout import workout_function

class WorkoutController:
	def __init__(self, model, view):
		self.model = model
		self.view = view
		self.start_workout()

	""" open workout camera and record the reps, then it done it update to the database """
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
