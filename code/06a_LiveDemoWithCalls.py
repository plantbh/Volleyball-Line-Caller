import cv2
import time
import subprocess
from _06h_CallInOrOutFunctionV5 import CallInOut5

# Camera settings
subprocess.run([
    "v4l2-ctl",
    "-d", "/dev/video0",
    "-c", "auto_exposure=1"
])

subprocess.run([
    "v4l2-ctl",
    "-d", "/dev/video0",
    "-c", "exposure_time_absolute=300"
])

pipeline = (
    "v4l2src device=/dev/video0 ! "
    "image/jpeg,width=640,height=360,framerate=230/1 ! "
    "jpegdec ! "
    "videoconvert ! "
    "appsink"
)

cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    raise RuntimeError("Could not open camera")

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)

frames = 0
startTime = time.time()
fps = 0

CLIP_LENGTH = 0
MOTION_THRESHOLD = 200          # Tune this number

clip_number = 0
recording = False
frames_left = 0
writer = None

prev_gray = None

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # -------------------------
    # Motion detection
    # -------------------------

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    motion_detected = False

    if prev_gray is not None:

        # Absolute difference
        diff = cv2.absdiff(gray, prev_gray)

        # Threshold
        _, motion = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        # Remove noise
        motion = cv2.medianBlur(motion, 5)

        changed_pixels = cv2.countNonZero(motion)

        if changed_pixels > MOTION_THRESHOLD:
            motion_detected = True

    prev_gray = gray.copy()

    # -------------------------
    # Start recording
    # -------------------------

    if motion_detected and not recording:

        clip_number += 1
        filename = f"liveDemoClip{clip_number}.avi"

        height, width = frame.shape[:2]

        writer = cv2.VideoWriter(
            filename,
            cv2.VideoWriter_fourcc(*'XVID'),
            fps,
            (width, height)
        )

        recording = True
        frames_left = CLIP_LENGTH

        print(f"Motion detected! Recording {filename}")

    # -------------------------
    # Save frames
    # -------------------------

    if recording:

        writer.write(frame)
        frames_left -= 1

        if frames_left <= 0:

            recording = False
            writer.release()
            writer = None

            print("Finished recording")
            CallInOut5(filename, f"liveDemoProcessedClip{clip_number}.mp4")
            for a in range (fps * 2):
                # to prevent double triggering
                ret, frame = cap.read()

    # -------------------------
    # Display
    # -------------------------

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    
    if time.time() - startTime >= 1:
        fps = frames
        CLIP_LENGTH = int(0.2 * fps)
        print(fps)
        startTime = time.time()
        frames = 0
    else:
        frames += 1
    
if writer is not None:
    writer.release()

cap.release()
cv2.destroyAllWindows()