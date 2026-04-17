import datetime
import sqlite3

#for data storage and manipulation of workout information

class WorkoutModel:
	def __init__(self):
		self.conn = sqlite3.connect("workout.db")
		self.cursor = self.conn.cursor()

		self._create_table()
		self.reps = 0

	def _create_table(self):
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS workouts (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				date TEXT NOT NULL UNIQUE,
				reps INTEGER NOT NULL
			)
		""")
		self.conn.commit()

	def set_reps(self, reps, date=None):
		if date is None:
			date = datetime.date.today().isoformat()

		self.cursor.execute("""
			UPDATE workouts
			SET reps = ?
			WHERE date = ?
		""", (reps, date))

		if self.cursor.rowcount == 0:
			self.cursor.execute("""
				INSERT INTO workouts (date, reps)
				VALUES (?, ?)
			""", (date, reps))

		self.conn.commit()
		print(f"[DB] SAVED: {date} - {reps} reps")

	def get_reps_by_date(self, date):
		self.cursor.execute("""
			SELECT reps FROM workouts WHERE date = ?
		""", (date,))

		result = self.cursor.fetchone()

		return result[0] if result else None

	def get_all_workouts(self):
		print(f"[DB] Fetching all workouts...")
		self.cursor.execute("""
			SELECT date, reps FROM workouts
		""")

		rows = self.cursor.fetchall()

		return {
			row[0]: row[1]
			for row in rows
		}

	def has_record(self):
		cursor = self.conn.cursor()
		cursor.execute("SELECT COUNT(*) FROM workouts")
		count = cursor.fetchone()[0]
		return count > 0

	def close(self):
		self.conn.close()
