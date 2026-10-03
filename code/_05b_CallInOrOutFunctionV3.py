import cv2
import numpy as np
import os

def CallInOut3 (inputFile, outputName):
    # Input and output files
    input_file = inputFile
    output_file = outputName

    lineXPos = 340
    ballDiameter = 80
    ballSquishWidth = 40

    slow_factor = 20          # 20x slower = 0.05x speed
    threshold_value = 25          # Motion detection threshold
    prevX = 0
    prevY = 0
    call = ""
    framesPassed = 0
    framesXs = []
    firstXPos = 0
    direction = 0

    # -----------------------------
    # Open input video
    # -----------------------------
    cap = cv2.VideoCapture(input_file)

    if not cap.isOpened():
        raise RuntimeError("Could not open input video.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    keep = False
    # -----------------------------
    # Read all frames into memory
    # (Fine for short clips.)
    # -----------------------------
    frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()

    if len(frames) == 0:
        raise RuntimeError("Input video contains no frames.")

    # ==================================================
    # Part 1: Slow-motion original
    # ==================================================
    for frame in frames:
        for _ in range(slow_factor):
            out.write(frame)

    # ==================================================
    # Part 2: Slow-motion absolute difference
    # ==================================================
    prev_gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)

    for frame in frames[1:]:
        
        #get gray frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Compute absolute difference
        diff = cv2.absdiff(prev_gray, gray)

        _, motion = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        # Create a mask that keeps everything
        mask1 = np.ones_like(motion, dtype=np.uint8) * 255
        
        # Threshold to highlight motion
        _, diff = cv2.threshold(diff, threshold_value, 255, cv2.THRESH_BINARY)

        # Convert grayscale back to BGR so it matches VideoWriter format
        diff_bgr = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)

        # Threshold to isolate significant changes
        underscore, mask1 = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        # Ignore the left and rights parts of the screen
        # mask1[:, 0:250] = 0
        # mask1[:,450:width] = 0

        # Apply the mask
        motion = cv2.bitwise_and(motion, mask1)

        # Get coordinates of changed pixels
        ys, xs = np.where(mask1 > 0)
        
        
        #defining variables with values
        centerX = 0
        centerY = 0
        
        # Slow down by repeating frames
        for b in range(slow_factor):
            if len(xs) > 0:
                centerX = int(np.mean(xs))
                centerY = int(np.mean(ys))
                cv2.circle(diff_bgr, (centerX, centerY), ballDiameter, (0, 0, 255), 4)
            cv2.line(diff_bgr, (lineXPos, 0), (lineXPos, width), (0, 0, 255), 15)
            if centerX > prevX:
                keep = True
            if centerY >= prevY:
                prevX = centerX
                prevY = centerY
            else:
                cv2.circle(diff_bgr, (prevX, prevY), ballDiameter, (0, 255, 0), 4)
                if direction == 1:
                    if prevX > lineXPos + ballSquishWidth:
                        call = "Out"
                        cv2.putText(
                            diff_bgr,
                            call,
                            (width - 100, 50),                      # x=50, y=50
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0,                           # Font size
                            (0, 0, 255),                   # Green (BGR)
                            3                              # Thickness
                        )
                    else:
                        call = "In"
                        cv2.putText(
                            diff_bgr,
                            call,
                            (width - 100, 50),                      # x=50, y=50
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0,                           # Font size
                            (0, 255, 0),                   # Green (BGR)
                            3                              # Thickness
                        )
                elif direction == -1:
                    if prevX < lineXPos - ballSquishWidth:
                        call = "Out"
                        cv2.putText(
                            diff_bgr,
                            call,
                            (width - 100, 50),                      # x=50, y=50
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0,                           # Font size
                            (0, 0, 255),                   # Green (BGR)
                            3                              # Thickness
                        )
                    else:
                        call = "In"
                        cv2.putText(
                            diff_bgr,
                            call,
                            (width - 100, 50),                      # x=50, y=50
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0,                           # Font size
                            (0, 255, 0),                   # Green (BGR)
                            3                              # Thickness
                        )
            out.write(diff_bgr)
        prev_gray = gray
        
        #getting the direction of the ball
        if framesPassed <= 3:
            if framesPassed == 0:
                firstXPos = centerX
            framesPassed += 1
            framesXs.append(centerX - firstXPos)
        else:
            if (framesXs[0] + framesXs[1] + framesXs[2]) / 3 < 0:
                direction = -1
            else:
                direction = 1

    out.release()
    
    #test
    print("Done")
    
    #decide wheter to show the file
    if keep == True:
        print(f"Finished! Saved to {output_file}. The call is {call}.")
        return call
    else:
        print("Invalid")
        os.remove(output_file)
        return "Invalid."
    
