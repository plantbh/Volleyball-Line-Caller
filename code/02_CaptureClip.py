import cv2
import time
import subprocess

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

# Recording state
recording = False
record_start = 0
writer = None

clip_number = 2

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # If recording, save frame
    if recording:
        writer.write(frame)

        if time.time() - record_start >= 300:
            recording = False
            writer.release()
            writer = None
            print("Finished recording")

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1) & 0xFF

    # Press A to start a 2-second recording
    if key == ord('a') and not recording:
        clip_number += 1
        filename = f"dataset{clip_number}.avi"

        height, width = frame.shape[:2]

        writer = cv2.VideoWriter(
            filename,
            cv2.VideoWriter_fourcc(*'XVID'),
            fps,  # match your camera FPS
            (width, height)
        )

        recording = True
        record_start = time.time()

        print(f"Recording {filename}...")

    # Press Q to quit
    if key == ord('q'):
        break
    
    if time.time() - startTime >= 1:
        fps = frames
        print(fps)
        startTime = time.time()
        frames = 0
    else:
        frames += 1
if writer is not None:
    writer.release()

cap.release()
cv2.destroyAllWindows()