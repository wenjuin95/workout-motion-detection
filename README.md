# Workout Motion Detection

A real-time workout motion detection application that uses computer vision to track arm movements and count repetitions. This project leverages MediaPipe's pose estimation and OpenCV to detect when both arms are raised vertically.

## Features

## **ALERT: currently only for track dumbbell lateral raise
- **Real-time Pose Detection**: Uses MediaPipe Pose Landmarker for accurate body pose estimation
- **Arm Tracking**: Detects and tracks both arms (shoulders, elbows, wrists)
- **Repetition Counter**: Automatically counts when both arms are raised vertically
- **Visual Feedback**: 
  - Displays real-time rep count
  - Shows motivational messages based on performance
  - Shows arm angles for debugging
- **Webcam Integration**: Works with any standard webcam

## Requirements

- Python 3.7 or higher
- Webcam
- The following Python packages:
  - OpenCV (opencv-python==4.13.0.92)
  - OpenCV contrib (opencv-contrib-python==4.13.0.92)
  - MediaPipe (mediapipe==0.10.30)

## Installation

### Option 1: Using the Setup Script (Linux) (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/wenjuin95/body-motion-detection.git
cd body-motion-detection
```

2. Run the setup script:
```bash
bash setup_venv.sh
```

This script will:
- Create a Python virtual environment
- Install all required dependencies
- Provide instructions for running the application

### Option 2: Manual Installation (Window or Linux)

1. Clone the repository:
```bash
git clone https://github.com/wenjuin95/workout-motion-detection.git
cd workout-motion-detection
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate.bat
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

## Project Structure

```
workout-motion-detection/
├── main.py                      # Main application code
├── pose_landmarker_lite.task    # MediaPipe pose detection model
├── requirements.txt             # Python dependencies
├── setup_venv.sh               # Virtual environment setup script
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```
## Acknowledgments

- [MediaPipe](https://mediapipe.dev/) by Google for the pose estimation model
- [OpenCV](https://opencv.org/) for computer vision capabilities
