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
    #the number below for exposure_time_absolute changes the exposure time
    "-c", "exposure_time_absolute=300"
])
#string of things together
pipeline = (
    "v4l2src device=/dev/video0 ! "
    #notice the jpeg convertion
    "image/jpeg,width=640,height=360,framerate=230/1 ! "
    "jpegdec ! "
    "videoconvert ! "
    "appsink"
)

#without this convertion, the video feed would be a file instead of a GStreamer pipeline
cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    raise RuntimeError("Could not open camera")

frames = 0
#time.time() is like the timer block, you know how that works
startTime = time.time()

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)

# Recording state
recording = False
record_start = 0
writer = None

clipNumber = 0


#gets camera feed
while True:
    ret, frame = cap.read()
    cv2.line(frame, (340, 0), (340, 360), (0, 0, 255), 15)
    
    if not ret:
        break
    # If recording, save frame
    if recording:
        #writing individual frames
        writer.write(frame)

        if time.time() - record_start >= 2:
            recording = False
            writer.release()
            writer = None
            print("Finished recording")

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1) & 0xFF

    # Press A to start a 2-second recording
    if key == ord('a') and not recording:
        clipNumber += 1
        filename = f"clip{clipNumber}.avi"

        height, width = frame.shape[:2]

        writer = cv2.VideoWriter(
            filename,
            cv2.VideoWriter_fourcc(*'XVID'),
            230,  # match your camera FPS
            (width, height)
        )

        recording = True
        record_start = time.time()



    cv2.imshow("Camera", frame)
    
    #with the timer block, you'll know how it works
    if time.time() - startTime >= 1:
        print(frames)
        startTime = time.time()
        frames = 0
    else:
        frames += 1
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#done
cap.release()
cv2.destroyAllWindows()