"""
Gesture Volume Control (Mac version)
--------------------------------------
Control your Mac's actual system volume by pinching your thumb
and index finger in front of your webcam.

Uses macOS's built-in AppleScript ('osascript') to set volume,
so no extra Mac-specific library is needed.

Controls:
  - Move thumb and index finger closer  -> volume down
  - Move thumb and index finger apart    -> volume up
  - Press 'q' to quit
"""

import cv2
import mediapipe as mp
import math
import numpy as np
import subprocess

# ---------------------------------------------------------
# Function to set Mac system volume (0-100) using AppleScript
# ---------------------------------------------------------
def set_mac_volume(volume_percent):
    volume_percent = int(max(0, min(100, volume_percent)))
    try:
        subprocess.run(
            ["osascript", "-e", f"set volume output volume {volume_percent}"],
            check=True
        )
    except Exception as e:
        print("Could not set system volume:", e)

# ---------------------------------------------------------
# MediaPipe hand detector setup
# ---------------------------------------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Distance range (pixels) mapped to 0-100% volume.
# Tweak these two numbers if it feels too sensitive/insensitive.
MIN_DIST = 25
MAX_DIST = 200

vol_bar = 400
vol_percent = 0

# To avoid spamming the OS with volume-set calls every single frame,
# we only update the actual system volume when it changes meaningfully.
last_sent_volume = -1

while True:
    success, img = cap.read()
    if not success:
        print("Could not read from webcam.")
        break

    img = cv2.flip(img, 1)  # mirror view, feels more natural
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = img.shape
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.append((int(lm.x * w), int(lm.y * h)))

            # Thumb tip = landmark 4, Index finger tip = landmark 8
            x1, y1 = landmarks[4]
            x2, y2 = landmarks[8]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 8, (0, 255, 0), cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)

            # Map finger distance to volume percentage (0-100)
            vol_percent = np.interp(length, [MIN_DIST, MAX_DIST], [0, 100])
            vol_bar = np.interp(length, [MIN_DIST, MAX_DIST], [400, 150])

            if length < MIN_DIST:
                cv2.circle(img, (cx, cy), 8, (0, 0, 255), cv2.FILLED)

            # Only send an update if the volume changed by at least 2%
            # (keeps things smooth and avoids lag from too many calls)
            rounded_vol = int(vol_percent)
            if abs(rounded_vol - last_sent_volume) >= 2:
                set_mac_volume(rounded_vol)
                last_sent_volume = rounded_vol

    # Draw volume bar UI
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(vol_percent)} %', (40, 430),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(img, "Mac Volume Control - Live", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Gesture Volume Control (Mac)", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()