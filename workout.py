import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
# import numpy as np
# # ---------------- Config ----------------
# RAISE_THRESHOLD = 0.05

# # ---------------- Functions ----------------

# # Draw line between two landmarks
# def draw_line(a, b, frame, color):
# 	h, w, _ = frame.shape
# 	p1 = (int(a.x * w), int(a.y * h))
# 	p2 = (int(b.x * w), int(b.y * h))
# 	cv2.line(frame, p1, p2, color, 2)

# def workout_function():
# 	# ---------------- MediaPipe setup ----------------
# 	BaseOptions = python.BaseOptions
# 	PoseLandmarker = vision.PoseLandmarker
# 	PoseLandmarkerOptions = vision.PoseLandmarkerOptions
# 	VisionRunningMode = vision.RunningMode

# 	# create a pose landmarker instance with the video mode:
# 	options = PoseLandmarkerOptions(
# 		base_options=BaseOptions(model_asset_path="pose_landmarker_lite.task"),
# 		running_mode=VisionRunningMode.VIDEO,
# 	)

# 	landmarker = PoseLandmarker.create_from_options(options)

# 	# ---------------- OpenCV setup ----------------
# 	cap = cv2.VideoCapture(0)

# 	# Set higher resolution
# 	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# 	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# 	frame_id = 0

# 	# ---------------- State ----------------
# 	both_count = 0
# 	both_is_up = False

# 	# ---------------- Main loop ----------------
# 	while True:
# 		ret, frame = cap.read()
# 		if not ret:
# 			break

# 		# Mirror camera
# 		frame = cv2.flip(frame, 1)

# 		# MediaPipe image
# 		mp_image = mp.Image(
# 			image_format=mp.ImageFormat.SRGB,
# 			data=frame
# 		)

# 		result = landmarker.detect_for_video(mp_image, frame_id)
# 		frame_id += 1

# 		if result.pose_landmarks:
# 			landmarks = result.pose_landmarks[0]

# 			# Landmark indices (MediaPipe Pose)
# 			LEFT_SHOULDER = 12
# 			LEFT_ELBOW = 14
# 			LEFT_WRIST = 16

# 			RIGHT_SHOULDER = 11
# 			RIGHT_ELBOW = 13
# 			RIGHT_WRIST = 15

# 			left_shoulder = landmarks[LEFT_SHOULDER]
# 			left_elbow    = landmarks[LEFT_ELBOW]
# 			left_wrist    = landmarks[LEFT_WRIST]

# 			right_shoulder = landmarks[RIGHT_SHOULDER]
# 			right_elbow    = landmarks[RIGHT_ELBOW]
# 			right_wrist    = landmarks[RIGHT_WRIST]

# 			# -------- Raise detection --------
# 			left_up = False
# 			right_up = False

# 			if left_wrist.y < left_shoulder.y - RAISE_THRESHOLD:
# 				left_up = True

# 			if right_wrist.y < right_shoulder.y - RAISE_THRESHOLD:
# 				right_up = True

# 			both_arms_up = left_up and right_up

# 			# -------- counting logic --------
# 			if both_arms_up:
# 				if not both_is_up:
# 					both_count += 1
# 					print(f"Both arms up count: {both_count}")
# 				both_is_up = True
# 			else:
# 				both_is_up = False

# 			# -------- Draw landmarks --------
# 			h, w, _ = frame.shape
# 			for lm in landmarks:
# 				cx, cy = int(lm.x * w), int(lm.y * h)
# 				cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)

# 			# Draw arm alignment
# 			draw_line(left_shoulder, left_elbow, frame, (255, 255, 255))
# 			draw_line(left_elbow, left_wrist, frame, (255, 255, 255))
# 			draw_line(right_shoulder, right_elbow, frame, (255, 255, 255))
# 			draw_line(right_elbow, right_wrist, frame, (255, 255, 255))

# 			# -------- UI --------
# 			status = "GOOD !!!" if both_arms_up else "RAISE BOTH ARMS"
# 			color = (0, 255, 0) if both_arms_up else (0, 0, 255)

# 			cv2.putText(frame, f"Reps: {both_count}", (30, 40),
# 						cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

# 			if both_count < 10:
# 				cv2.putText(frame, "(so weak)", (200, 40),
# 							cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
# 			else:
# 				cv2.putText(frame, "(Power !!!)", (200, 40),
# 							cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# 			cv2.putText(frame, status, (30, 80),
# 						cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

# 			# Debug info
# 			cv2.putText(frame, f"L up: {left_up}", (30, 120),
# 						cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

# 			cv2.putText(frame, f"R up: {right_up}", (30, 150),
# 						cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# 		# Show frame
# 		cv2.imshow("Pose Detection", frame)
# 		key = cv2.waitKey(1) & 0xFF

# 		# Quit by Q
# 		if key == ord("q") or key == 27:
# 			break

# 		# Quit by clicking X (safe)
# 		try:
# 			if cv2.getWindowProperty("Pose Detection", cv2.WND_PROP_VISIBLE) < 1:
# 				break
# 		except cv2.error:
# 			break

# 	# ---------------- Cleanup ----------------
# 	cap.release()
# 	cv2.destroyAllWindows()

# 	return both_count


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
				status = "GOOD !!!" if both_up else "RAISE BOTH ARMS"
				color = (0,255,0) if both_up else (0,0,255)

				cv2.putText(frame, f"Reps: {count}", (30,40),
							cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

				cv2.putText(frame, status, (30,80),
							cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

			cv2.imshow("Pose Detection", frame)

			if cv2.waitKey(1) & 0xFF in [ord('q'), 27]:
				break

		self.cap.release()
		cv2.destroyAllWindows()

		return self.tracker.count

def workout_function():
	app = PoseApp()
	return app.run()
