from ultralytics import YOLO
import cv2
import os
import serial

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# Load the YOLOv8 model
model = YOLO("one.pt")

ser = serial.Serial('COM6', 9600) 

# Path to the video file
video_path = "TestVideos/video2.mp4"
# If you want to use webcam, uncomment the line below
# video_path = 0

# Open the video capture object
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Get the current frame number
    frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)

    # Skip frames to speed up processing
    if frame_number % 3 == 0:
        success, frame = cap.read()
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number + 1)
        continue

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, conf=0.5)
        
        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Process detection results
        detection_msg = ""
        for result in results:
            boxes = result.boxes.cpu().numpy()
            cls = boxes.cls

            # Check for detection classes
            if len(cls) == 0:
                detection_msg = "No detection"
            elif cls[0] == 0:
                detection_msg = "Fall detected"
                ser.write(b'F')
            elif cls[0] == 1:
                detection_msg = "Person detected"

        # Print detection message
        print(detection_msg)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
