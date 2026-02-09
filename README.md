# Body Motion Detection

A real-time body motion detection application that uses computer vision to track arm movements and count repetitions. This project leverages MediaPipe's pose estimation and OpenCV to detect when both arms are raised vertically.

## Features

- **Real-time Pose Detection**: Uses MediaPipe Pose Landmarker for accurate body pose estimation
- **Arm Tracking**: Detects and tracks both arms (shoulders, elbows, wrists)
- **Repetition Counter**: Automatically counts when both arms are raised vertically
- **Visual Feedback**: 
  - Displays real-time rep count
  - Shows motivational messages based on performance
  - Shows arm angles for debugging
  - Color-coded status indicators (green when arms are up, red when down)
- **Webcam Integration**: Works with any standard webcam

## Requirements

- Python 3.7 or higher
- Webcam
- The following Python packages:
  - OpenCV (opencv-python==4.13.0.92)
  - OpenCV contrib (opencv-contrib-python==4.13.0.92)
  - MediaPipe (mediapipe==0.10.30)

## Installation

### Option 1: Using the Setup Script (Recommended)

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

### Option 2: Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/wenjuin95/body-motion-detection.git
cd body-motion-detection
```

2. Create a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Activate the virtual environment (if you created one):
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
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

## How It Works

The application uses:

1. **MediaPipe Pose Landmarker**: A machine learning model that detects 33 body landmarks in real-time
2. **Angle Calculation**: Computes the angle at the elbow joint to determine if arms are straight
3. **Vertical Alignment Check**: Verifies that shoulder, elbow, and wrist are vertically aligned
4. **State Machine**: Tracks arm position to count repetitions (avoids double-counting)

### Detection Criteria

Both arms are considered "up" when:
- Left and right arms are vertically aligned (within 3% tolerance)
- Left elbow angle > 160 degrees
- Right elbow angle > 160 degrees

## Troubleshooting

### Webcam not found
- Make sure your webcam is connected and not being used by another application
- Try changing the camera index in `main.py` (line 54): `cap = cv2.VideoCapture(0)` → try 1, 2, etc.

### Pose detection not working
- Ensure good lighting conditions
- Make sure your full upper body is visible in the frame
- Stand 1-2 meters away from the camera for best results

### Application crashes on startup
- Verify all dependencies are installed: `pip list`
- Make sure the `pose_landmarker_lite.task` model file is present in the project directory

## Project Structure

```
body-motion-detection/
├── main.py                      # Main application code
├── pose_landmarker_lite.task    # MediaPipe pose detection model
├── requirements.txt             # Python dependencies
├── setup_venv.sh               # Virtual environment setup script
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## Technical Details

### Key Functions

- `calculate_angle(a, b, c)`: Calculates the angle at point b given three landmarks
- `draw_line(a, b, frame, color)`: Draws a line between two landmarks on the frame
- `is_vertical(a, b, c, tolerance)`: Checks if three points are vertically aligned

### Customization

You can modify the following parameters in `main.py`:

- **Camera resolution** (lines 57-58): Adjust width and height
- **Angle threshold** (line 116-117): Change minimum angle for "straight arm" detection
- **Vertical tolerance** (line 33): Adjust vertical alignment sensitivity
- **Rep count messages** (lines 146-151): Customize motivational messages

## License

This project is open source. Please check with the repository owner for specific license terms.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Acknowledgments

- [MediaPipe](https://mediapipe.dev/) by Google for the pose estimation model
- [OpenCV](https://opencv.org/) for computer vision capabilities
