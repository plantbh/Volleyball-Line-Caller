import cv2

video_path = "clip1.avi"  # replace with your filename

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise RuntimeError(f"Could not open {video_path}")

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)

duration_seconds = frame_count / fps

minutes = int(duration_seconds // 60)
seconds = duration_seconds % 60

print(f"File: {video_path}")
print(f"Frames: {frame_count}")
print(f"FPS: {fps:.2f}")
print(f"Duration: {duration_seconds:.3f} seconds")
print(f"Duration: {minutes} min {seconds:.3f} sec")

cap.release()