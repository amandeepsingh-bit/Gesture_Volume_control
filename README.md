# Gesture Volume Control 🖐️🔊

Control your computer's volume by pinching your thumb and index finger in front of your webcam — no mouse or keyboard needed. Built with **OpenCV** and **MediaPipe**.

## How it works
1. Your webcam feed is captured with OpenCV.
2. MediaPipe detects your hand and 21 landmark points on it.
3. We track the distance between your **thumb tip** and **index finger tip**.
4. That distance is mapped to a volume percentage (0–100%).
   - Fingers close together → volume down
   - Fingers far apart → volume up
5. On Windows, the real system volume is changed using `pycaw`.
   On Mac/Linux, it runs in **demo mode** and just shows the volume bar on screen (since those OSes don't have a simple universal Python volume API).

## Demo
A green bar on the left of the screen fills up/down as you pinch, and shows the live percentage.

## Requirements
- Python 3.8–3.11 (MediaPipe doesn't support the very latest Python yet)
- A webcam

## Installation
```bash
git clone https://github.com/YOUR-USERNAME/gesture-volume-control.git
cd gesture-volume-control
pip install -r requirements.txt
```

## Usage
```bash
python gesture_volume_control.py
```
- Show your hand to the webcam.
- Pinch your thumb and index finger together or apart to control volume.
- Press **q** to quit.

## Project structure
```
gesture-volume-control/
├── gesture_volume_control.py   # main script
├── requirements.txt            # dependencies
└── README.md                   # this file
```

## Notes / Tips
- If the volume bar feels too sensitive or not sensitive enough, tweak `MIN_DIST` and `MAX_DIST` near the top of the script.
- Works best in good lighting with your hand clearly visible.
- Only one hand is tracked at a time (`max_num_hands=1`) to keep it simple and fast.

## Possible upgrades (optional, for later)
- Add mute gesture (e.g., fist = mute)
- Support brightness control the same way
- Add a smoother/animated volume bar
- Multi-hand support

## License
Free to use and modify for learning purposes.