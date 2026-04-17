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
			today = datetime.date.today()
			yesterday = today - datetime.timedelta(days=1)

			yesterday_rep = self.model.get_reps_by_date(yesterday.isoformat())

			# give penalty for not doing workout yesterday, and keep doubling for consecutive failed days
			hold_time = 0
			if self.model.has_record():
				yesterday_rep = self.model.get_reps_by_date(yesterday.isoformat())

				if yesterday_rep is None or int(yesterday_rep) < 10:
					hold_time = 2
					check_day = yesterday - datetime.timedelta(days=1)

					while True:
						rep = self.model.get_reps_by_date(check_day.isoformat())

						if rep is not None and int(rep) >= 10:
							break

						if rep is None:
							hold_time *= 2
						elif int(rep) < 10:
							hold_time *= 2

						check_day -= datetime.timedelta(days=1)

						if hold_time > 16:
							break

				# keep doubling for consecutive failed days
				check_day = yesterday - datetime.timedelta(days=1)
				while True:
					rep = self.model.get_reps_by_date(check_day.isoformat())
					rep = int(rep) if rep is not None else 0

					if rep >= 10:
						break

					hold_time *= 2
					check_day -= datetime.timedelta(days=1)

					if hold_time > 16:  # prevent infinite punishment
						break

			reps = workout_function(hold_time)

			current_rep = self.model.get_reps_by_date(today.isoformat())
			current_rep = int(current_rep) if current_rep is not None else 0

			if reps >= current_rep:
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
			f"Total: {self.model.get_reps_by_date(date)} reps\n You did {reps} reps.\n {comment}"
		)
