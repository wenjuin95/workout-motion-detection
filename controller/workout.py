import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time


class PoseDetector:
	def __init__(self, model_path="pose_landmarker_lite.task"):
		BaseOptions = python.BaseOptions
		PoseLandmarker = vision.PoseLandmarker
		PoseLandmarkerOptions = vision.PoseLandmarkerOptions
		VisionRunningMode = vision.RunningMode

		options = PoseLandmarkerOptions(
			base_options=BaseOptions(model_asset_path=model_path),
			running_mode=VisionRunningMode.VIDEO,
		)

		self.landmarker = PoseLandmarker.create_from_options(options)
		self.frame_id = 0

	def detect(self, frame):
		mp_image = mp.Image(
			image_format=mp.ImageFormat.SRGB,
			data=frame
		)

		result = self.landmarker.detect_for_video(mp_image, self.frame_id)
		self.frame_id += 1

		if result.pose_landmarks:
			return result.pose_landmarks[0]
		return None

class WorkoutTracker:
	def __init__(self, threshold=0.05, hold_time=0):
		self.threshold = threshold
		self.hold_time = hold_time
		self.count = 0
		self.both_is_up = False
		self.start_hold = None

	def check_arms(self, landmarks):
		LEFT_SHOULDER, LEFT_WRIST = 12, 16
		RIGHT_SHOULDER, RIGHT_WRIST = 11, 15

		left_up = landmarks[LEFT_WRIST].y < landmarks[LEFT_SHOULDER].y - self.threshold
		right_up = landmarks[RIGHT_WRIST].y < landmarks[RIGHT_SHOULDER].y - self.threshold

		return left_up, right_up

	def update(self, left_up, right_up):
		both_up = left_up and right_up
		now = time.time()

		if both_up:
			if self.start_hold is None:
				self.start_hold = now

			elapsed = now - self.start_hold

			if self.hold_time == 0:
				if not self.both_is_up:
					self.count += 1
					self.both_is_up = True

			elif elapsed >= self.hold_time:
				if not self.both_is_up:
					self.count += 1
					self.both_is_up = True
		else:
			self.both_is_up = False
			self.start_hold = None

		return both_up, self.count

class PoseApp:
	def __init__(self, hold_time=0):
		self.detector = PoseDetector()
		self.tracker = WorkoutTracker(hold_time=hold_time)

		self.cap = cv2.VideoCapture(0)
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

	def draw_line(self, a, b, frame, color):
		h, w, _ = frame.shape
		p1 = (int(a.x * w), int(a.y * h))
		p2 = (int(b.x * w), int(b.y * h))
		cv2.line(frame, p1, p2, color, 2)

	def run(self):
		window_name = "Pose Detection"
		while True:
			ret, frame = self.cap.read()
			if not ret:
				break

			frame = cv2.flip(frame, 1)

			landmarks = self.detector.detect(frame)

			if landmarks:
				left_up, right_up = self.tracker.check_arms(landmarks)
				both_up, count = self.tracker.update(left_up, right_up)

				# Draw landmarks
				h, w, _ = frame.shape
				for lm in landmarks:
					cx, cy = int(lm.x * w), int(lm.y * h)
					cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)

				# Draw arms
				self.draw_line(landmarks[12], landmarks[14], frame, (255,255,255))
				self.draw_line(landmarks[14], landmarks[16], frame, (255,255,255))
				self.draw_line(landmarks[11], landmarks[13], frame, (255,255,255))
				self.draw_line(landmarks[13], landmarks[15], frame, (255,255,255))

				# Display instructions
				cv2.putText(frame, f"Press 'q' or 'esc' to quit", (30,40),
							cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

				# Display count with comment
				if count > 20:
					comment = "Amazing! You're on fire!"
				elif count > 10:
					comment = "Excellent! Keep it up!"
				else:
					comment = "Weak! You can do better!"

				cv2.putText(frame, f"Reps: {count} ({comment})", (30,80),
							cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

				# Display penalty status
				penalty_text = "Normal mode" if self.tracker.hold_time <= 0 else f"Hold for {self.tracker.hold_time}s"
				if self.tracker.hold_time > 0 and both_up and not self.tracker.both_is_up and self.tracker.start_hold is not None:
					remaining = self.tracker.hold_time - (time.time() - self.tracker.start_hold)
					if remaining > 0:
						remaining_int = int(remaining + 0.999)
						penalty_text = f"Hold for {remaining_int}s"

				cv2.putText(frame, penalty_text, (30,120),
							cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

				# Display arm status
				status = "RAISE BOTH ARMS: GOOD !!!" if both_up else "RAISE BOTH ARMS"
				color = (0,255,0) if both_up else (0,0,255)

				cv2.putText(frame, status, (30,160),
							cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

			cv2.imshow(window_name, frame)

			# Handle q or esc to quit
			key = cv2.waitKey(1) & 0xFF
			if key in [ord('q'), 27]:
				break

		self.cap.release()
		cv2.destroyAllWindows()
		time.sleep(0.1)

		return self.tracker.count

def workout_function(hold_time=0):
	app = PoseApp(hold_time)
	return app.run()
