import cv2
import os
import numpy as np
from _05b_CallInOrOutFunctionV3 import CallInOut3

# -----------------------------
# Configuration
# -----------------------------

def Task3Functions2(inputVideo, outputClip, outputVideo):

    INPUT_VIDEO = inputVideo
    
    MOTION_X_MIN = 280        # Only consider motion with x >= 280
    THRESHOLD = 25            # Pixel intensity threshold
    MIN_CHANGED_PIXELS = 200  # Tune this for your scene

    # -----------------------------
    # Open video
    # -----------------------------
    cap = cv2.VideoCapture(INPUT_VIDEO)

    if not cap.isOpened():
        raise RuntimeError("Could not open input video.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frames_per_clip = int(round(0.5 * fps))

    # Read first frame
    ret, prev = cap.read()
    if not ret:
        raise RuntimeError("Video is empty.")

    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

    clip_number = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Absolute difference
        diff = cv2.absdiff(prev_gray, gray)

        # Threshold
        _, motion = cv2.threshold(diff, THRESHOLD, 255, cv2.THRESH_BINARY)

        # Ignore everything left of x = 280
        # motion[:, :MOTION_X_MIN] = 0

        # Count changed pixels
        changed_pixels = cv2.countNonZero(motion)

        if changed_pixels > MIN_CHANGED_PIXELS:
            print(f"Motion detected! Saving clip {clip_number}")

            filename = f"{outputClip}{clip_number:04d}.mp4"

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

            # Include the current frame
            out.write(frame)

            # Write the next 0.5 seconds
            for _ in range(frames_per_clip - 1):
                ret2, next_frame = cap.read()
                if not ret2:
                    break

                out.write(next_frame)

                # Keep prev_gray updated
                prev_gray = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)

            out.release()
            CallInOut3(f"{outputClip}{clip_number:04d}.mp4", f"{outputVideo}{clip_number}.mp4")
            clip_number += 1

        prev_gray = gray

    cap.release()

    print("Done.")

    # for a in range(clip_number):
    #     CallInOut3(f"{outputClip}{a:04d}.mp4", f"{outputVideo}{a}.mp4")
