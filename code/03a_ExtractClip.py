import cv2

# Input and output filenames
input_video = "dataset1.avi"
output_video = "shortClip.mp4"

# Frame where the clip should start
start_frame = 3010

# Number of frames to extract
num_frames = 30

# Open the input video
cap = cv2.VideoCapture(input_video)

# detect error
if not cap.isOpened():
    raise RuntimeError("Could not open input video.")

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Jump directly to the desired frame
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

# Create the output video writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

frames_written = 0

#record clip from big video
while frames_written < num_frames:
    ret, frame = cap.read()

    if not ret:
        print("Reached end of video.")
        break

    writer.write(frame)
    frames_written += 1

# close both files
cap.release()
writer.release()

print(f"Saved a video as {output_video} that's {frames_written} frames long.")