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

			# Check if today's reps are already >= 10, if so, no penalty
			current_rep = self.model.get_reps_by_date(today.isoformat())
			current_rep = int(current_rep) if current_rep is not None else 0

			# If today's reps are less than 10, check the history to determine give penalty
			hold_time = 0
			workouts = self.model.get_all_workouts() if self.model.has_record() else {}
			has_history_before_today = any(
				workout_date < today.isoformat() for workout_date in workouts.keys()
			)
			first_record_date = None
			if workouts:
				first_record_date = datetime.date.fromisoformat(min(workouts.keys()))

			# Check consecutive failed day before today to determine number of hold time for punishment
			if current_rep < 10 and has_history_before_today:
				# Punishment is based on consecutive failed days up to yesterday.
				check_day = yesterday
				while True:
					if first_record_date is not None and check_day < first_record_date:
						break

					rep = self.model.get_reps_by_date(check_day.isoformat())
					rep_value = int(rep) if rep is not None else 0

					if rep_value >= 10:
						break

					# It doubles per consecutive fail and is capped at 8 seconds.
					hold_time = 2 if hold_time == 0 else hold_time * 2
					if hold_time >= 8:
						hold_time = 8
						break

					check_day -= datetime.timedelta(days=1)

			reps = workout_function(hold_time)

			# Accumulate today's reps across sessions
			total_reps = current_rep + reps
			self.model.set_reps(total_reps)
		finally:
			self.view.show()

		comment = ""
		if reps < 10:
			comment = "(why stop? you can do more!)"
		elif reps > 20:
			comment = "(good job! take a rest and keep going!)"
		elif reps > 10:
			comment = "(amazing! you are doing great!)"

		date = datetime.date.today().isoformat()
		self.view.set_status(
			f"Total: {self.model.get_reps_by_date(date)} reps\n You did {reps} reps.\n {comment}"
		)
