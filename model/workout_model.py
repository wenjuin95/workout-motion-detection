#for data storage and manipulation of workout information

class WorkoutModel:
    def __init__(self):
        self.reps = 0

    def set_reps(self, reps):
        self.reps = reps

    def get_reps(self):
        return self.reps
