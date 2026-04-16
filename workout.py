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
	def __init__(self, threshold=0.05):
		self.threshold = threshold
		self.count = 0
		self.both_is_up = False

	def check_arms(self, landmarks):
		LEFT_SHOULDER, LEFT_WRIST = 12, 16
		RIGHT_SHOULDER, RIGHT_WRIST = 11, 15

		left_up = landmarks[LEFT_WRIST].y < landmarks[LEFT_SHOULDER].y - self.threshold
		right_up = landmarks[RIGHT_WRIST].y < landmarks[RIGHT_SHOULDER].y - self.threshold

		return left_up, right_up

	def update(self, left_up, right_up):
		both_up = left_up and right_up

		if both_up:
			if not self.both_is_up:
				self.count += 1
			self.both_is_up = True
		else:
			self.both_is_up = False

		return both_up, self.count

class PoseApp:
	def __init__(self):
		self.detector = PoseDetector()
		self.tracker = WorkoutTracker()

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

				# UI
				status = "RAISE BOTH ARMS: GOOD !!!" if both_up else "RAISE BOTH ARMS"
				color = (0,255,0) if both_up else (0,0,255)

				if count > 20:
					comment = "Amazing! You're on fire!"
				elif count > 10:
					comment = "Excellent! Keep it up!"
				else:
					comment = "Weak! You can do better!"

				cv2.putText(frame, f"Press 'q' or 'esc' to quit", (30,40),
							cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

				cv2.putText(frame, f"Reps: {count} ({comment})", (30,80),
							cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

				cv2.putText(frame, status, (30,120),
							cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

			cv2.imshow(window_name, frame)

			# handle q or esc to quit
			key = cv2.waitKey(1) & 0xFF
			if key in [ord('q'), 27]:
				break

		self.cap.release()
		cv2.destroyAllWindows()
		time.sleep(0.1)

		return self.tracker.count

def workout_function():
	app = PoseApp()
	return app.run()
