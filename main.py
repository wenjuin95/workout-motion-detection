import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np

# ---------------- Functions ----------------

def calculate_angle(a, b, c):
    ba = np.array([a.x - b.x, a.y - b.y])
    bc = np.array([c.x - b.x, c.y - b.y])
    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    return np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))

def draw_line(a, b, frame, color):
    h, w, _ = frame.shape
    p1 = (int(a.x * w), int(a.y * h))
    p2 = (int(b.x * w), int(b.y * h))
    cv2.line(frame, p1, p2, color, 2)

def is_vertical(a, b, c, tolerance=0.03):
    return (
        abs(a.y - b.y) < tolerance and
        abs(b.y - c.y) < tolerance
    )


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

# Set higher resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 128000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

frame_id = 0

# ---------------- State ----------------
both_count = 0
both_is_up = False

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
        LEFT_SHOULDER = 12
        LEFT_ELBOW = 14
        LEFT_WRIST = 16

        RIGHT_SHOULDER = 11
        RIGHT_ELBOW = 13
        RIGHT_WRIST = 15

        left_shoulder = landmarks[LEFT_SHOULDER]
        left_elbow    = landmarks[LEFT_ELBOW]
        left_wrist    = landmarks[LEFT_WRIST]

        right_shoulder = landmarks[RIGHT_SHOULDER]
        right_elbow    = landmarks[RIGHT_ELBOW]
        right_wrist    = landmarks[RIGHT_WRIST]


        # -------- counting logic --------
        # Calculate angles
        left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        # Check vertical alignment
        left_vertical = is_vertical(left_shoulder, left_elbow, left_wrist)
        right_vertical = is_vertical(right_shoulder, right_elbow, right_wrist)

        both_arms_up = (
            left_vertical and
            right_vertical and
            left_angle > 160 and
            right_angle > 160
        )

        if both_arms_up:
            if not both_is_up:
                both_count += 1
                print(f"Both arms up count: {both_count}")
            both_is_up = True
        else:
            both_is_up = False

        # Draw landmarks
        h, w, _ = frame.shape
        for lm in landmarks:
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)

        # Draw arm alignment
        draw_line(left_shoulder, left_elbow, frame, (255, 255, 255))
        draw_line(left_elbow, left_wrist, frame, (255, 255, 255))
        draw_line(right_shoulder, right_elbow, frame, (255, 255, 255))
        draw_line(right_elbow, right_wrist, frame, (255, 255, 255))

        # -------- Draw counters --------
        status = " GOOD !!!" if both_arms_up else "RAISE BOTH ARMS"
        color = (0, 255, 0) if both_arms_up else (0, 0, 255)

        cv2.putText(frame, f"Reps: {both_count}", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        if both_count < 10:
            cv2.putText(frame, f"(so weak)", (200, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        else:
            cv2.putText(frame, f"(Power !!!)", (200, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(frame, status, (30, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        cv2.putText(frame, f"L angle: {int(left_angle)}", (30, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.putText(frame, f"R angle: {int(right_angle)}", (30, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Show frame
    cv2.imshow("Pose Detection", frame)
    key = cv2.waitKey(1) & 0xFF

    # Quit by Q
    if key == ord("q") or key == 27:
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