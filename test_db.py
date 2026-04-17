from model.workout_model import WorkoutModel

model = WorkoutModel()

# insert test data
model.set_reps(4, "2026-04-09")
model.set_reps(4, "2026-04-10")
model.set_reps(4, "2026-04-11")
model.set_reps(4, "2026-04-12")
model.set_reps(4, "2026-04-13")
model.set_reps(4, "2026-04-14")
model.set_reps(4, "2026-04-15")
model.set_reps(4, "2026-04-16")

# fetch one date
# print(model.get_reps_by_date("2026-04-15"))  # should print 10
# print(model.get_reps_by_date("2026-04-16"))  # should print 20

# fetch all
print(model.get_all_workouts())
