# Workout tracker

<img src="https://github.com/wenjuin95/workout-motion-detection/blob/main/public/title.png" width="40%">

A real-time workout application that leverages computer vision to ensure perfect form and daily discipline. This project uses MediaPipe’s Pose Landmarker and OpenCV to track arm kinematics and provide instant feedback.

## Features

## **ALERT: currently only for track dumbbell lateral raise
- **Real-time Pose Estimation**: High-fidelity body tracking using MediaPipe.
- **Dual-Arm Kinematics**: Synchronous tracking of shoulders, elbows, and wrists to ensure symmetrical movement.
- **Automated Rep Counting**: Intelligent detection of the vertical peak for dumbbell lateral raises.
- **Performance Dashboard**:
	- **Live Metrics**: Displays real-time rep counts and joint angles.
	- **Dynamic Feedback**: Context-aware motivational messages.
- **Persistence & Tracking**: Integrated database to log daily reps with a visual Calendar View.
	<img src="https://github.com/wenjuin95/workout-motion-detection/blob/main/public/calender.png" width="40%">
- **The Penalty System**:
  	- Consistency is mandatory. If you fail to hit the daily goal of 10 reps, the app increases the difficulty of your next workout.
  	  	- The Trigger: Complete < 10 reps today
  	  	- The Penalty: You must hold for 2 seconds at the top of every rep tomorrow
  	  	- The Multiplier: Every consecutive day you miss the goal, the hold time doubles ($x2$)
			- Example: Miss 1 day = 2s hold. Miss 2 days = 4s hold. Miss 3 days = 8s hold.


## 🗺️ Roadmap
The core engine is built to be modular. Future updates will include:
- 🔄 New Exercises: Support for Bicep Curls, Overhead Presses, and Squats.
- 📈 Progress Analytics: Weekly volume charts and performance trends.

## Requirements

- Webcam
- Python 3.7 or higher
- Tkinter
	- (Linux)
		1. sudo apt-get install python3-tk
	- (window)
		1. Open **Control Panel** > **Apps**
		2. Find **Python 3.x**, right-click the **three dot**, then **Modify**
		3. Choose **Modify**
		4. Check the bow for **tcl/tk and IDLE**
		5. Click install/next until finished
- The following Python packages:
  - OpenCV (opencv-python==4.13.0.92)
  - OpenCV contrib (opencv-contrib-python==4.13.0.92)
  - MediaPipe (mediapipe==0.10.30)

## Installation

### Option 1: (Linux) (Recommended) Using the Setup Script

1. Clone the repository:
```bash
git clone https://github.com/wenjuin95/body-motion-detection.git
cd body-motion-detection
```

2. Run the setup script:
```bash
bash setup_venv.sh
```

### Option 2: (Window) Using the Setup Script
1. Clone the repository in command prompt:
```bash
git clone https://github.com/wenjuin95/body-motion-detection.git
cd body-motion-detection
```

2. run the setup script:
```bash
setup_with_window.bat
```

### Option 3: Manual Installation (Window or Linux)

1. Clone the repository:
```bash
git clone https://github.com/wenjuin95/workout-motion-detection.git
cd workout-motion-detection
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Activate the virtual environment (if you created one):
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate.bat
```

2. Run the application:
```bash
python main.py
```

3. Position yourself in front of the webcam so your upper body is visible

4. Raise both arms vertically to perform a repetition:
   - Arms should be straight (angle > 160 degrees)
   - Both arms should be aligned vertically
   - The counter will increment when both conditions are met

5. To exit the application:
   - Press 'q' key, or
   - Click the X button on the window

## Troubleshooting

### Webcam not found
- Make sure your webcam is connected and not being used by another application
- Try changing the camera index in `main.py` (line 54): `cap = cv2.VideoCapture(0)` → try 1, 2, etc.
- Don't use wsl it not work for webcam

### Pose detection not working
- Ensure good lighting conditions
- Make sure your full upper body is visible in the frame
- Stand 1-2 meters away from the camera for best results

### Application crashes on startup
- Verify all dependencies are installed: `pip list`
- Make sure the `pose_landmarker_lite.task` model file is present in the project directory

## Acknowledgments

- [MediaPipe](https://mediapipe.dev/) by Google for the pose estimation model
- [OpenCV](https://opencv.org/) for computer vision capabilities
