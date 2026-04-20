import datetime
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# table definition
class Workout(Base):
	__tablename__ = 'workouts'

	id = Column(Integer, primary_key=True, autoincrement=True)
	date = Column(String, unique=True, nullable=False)
	reps = Column(Integer, nullable=False)

class WorkoutModel:
	def __init__(self):
		# create database connection (echo=False is to suppress SQL logging)
		self.engine = create_engine("sqlite:///workout.db", echo=False)
		# help to create the table if it doesn't exist
		Base.metadata.create_all(self.engine)

		# primary interface use to interact with the database
		# as a "workspace" for all operations
		Session = sessionmaker(bind=self.engine)
		self.session = Session()

		self.reps = 0

	def set_reps(self, reps, date=None):
		'''
		save the reps with the date into the database, if the date is not provided, use today's date as default
		:param reps: the number of reps to save
		:param date: the date to save the reps for, in ISO format (YYYY-MM-DD), default is None which means use today's date
		'''

		if date is None:
			date = datetime.date.today().isoformat()

		workout_data = self.session.query(Workout).filter_by(date=date).first()

		# if the data is exist just update, otherwise create a new record
		if workout_data:
			workout_data.reps = reps
		else:
			new_reps = Workout(date=date, reps=reps)
			self.session.add(new_reps)

		self.session.commit()
		print(f"[DB] SAVED: {date} - {reps} reps")

	def get_reps_by_date(self, date):
		'''
		get the reps by date, return None if no record found
		:param date: the date to get the reps for, in ISO format (YYYY-MM-DD)
		:return: the number of reps for the given date, or None if no record found
		'''
		workout_data = self.session.query(Workout).filter_by(date=date).first()
		return workout_data.reps if workout_data else None

	def get_all_workouts(self):
		'''
		get all workouts as a dictionary {date: reps}
		:return: a dictionary mapping dates to the number of reps
		'''
		print(f"[DB] Fetching all workouts...")
		rows = self.session.query(Workout).all()

		return {
			row.date: row.reps
			for row in rows
		}

	def has_record(self):
		'''
		check if there is any workout record in the database
		:return: True if there is at least one record, False otherwise
		'''
		count = self.session.query(Workout).count()
		return count > 0
