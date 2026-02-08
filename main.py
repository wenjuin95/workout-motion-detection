import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = "https://www.geeksforgeeks.org/python/python-script-to-open-a-web-browser/"

driver = webdriver.Chrome()
driver.get(url)

# ---------------- MediaPipe setup ----------------
BaseOptions = python.BaseOptions
PoseLandmarker = vision.PoseLandmarker
PoseLandmarkerOptions = vision.PoseLandmarkerOptions
VisionRunningMode = vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="pose_landmarker_lite.task"),
    running_mode=VisionRunningMode.VIDEO,
)

landmarker = PoseLandmarker.create_from_options(options)

# ---------------- OpenCV setup ----------------
cap = cv2.VideoCapture(0)
cv2.namedWindow("Pose Detection", cv2.WINDOW_NORMAL)

frame_id = 0

# ---------------- State ----------------
left_count = 0
right_count = 0
left_is_up = False
right_is_up = False

# ---------------- Main loop ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    # MediaPipe image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=frame
    )

    result = landmarker.detect_for_video(mp_image, frame_id)
    frame_id += 1

    if result.pose_landmarks:
        landmarks = result.pose_landmarks[0]

        # Landmark indices (MediaPipe Pose)
        LEFT_SHOULDER = 11
        RIGHT_SHOULDER = 12
        LEFT_WRIST = 15
        RIGHT_WRIST = 16

        left_wrist = landmarks[LEFT_WRIST]
        right_wrist = landmarks[RIGHT_WRIST]
        left_shoulder = landmarks[LEFT_SHOULDER]
        right_shoulder = landmarks[RIGHT_SHOULDER]

        # -------- LEFT HAND --------
        if left_wrist.y < left_shoulder.y:
            if not left_is_up:
                left_count += 1
                print(f"LEFT → total: {left_count}")
                #driver.find_element("tag name", "body").send_keys(Keys.PAGE_DOWN)
            left_is_up = True
        else:
            left_is_up = False

        # -------- RIGHT HAND --------
        if right_wrist.y < right_shoulder.y:
            if not right_is_up:
                right_count += 1
                print(f"RIGHT → total: {right_count}")
                driver.find_element("tag name", "body").send_keys(Keys.PAGE_DOWN)
            right_is_up = True
        else:
            right_is_up = False

        # -------- Draw landmarks --------
        h, w, _ = frame.shape
        for lm in landmarks:
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)

        # -------- Draw counters --------
        cv2.putText(frame, f"Left hand: {left_count}", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Right hand: {right_count}", (30, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show frame
    cv2.imshow("Pose Detection", frame)
    key = cv2.waitKey(1) & 0xFF

    # Quit by Q
    if key == ord("q"):
        break

    # Quit by clicking X (safe)
    try:
        if cv2.getWindowProperty("Pose Detection", cv2.WND_PROP_VISIBLE) < 1:
            break
    except cv2.error:
        break

# ---------------- Cleanup ----------------
cap.release()
cv2.destroyAllWindows()
driver.quit()
