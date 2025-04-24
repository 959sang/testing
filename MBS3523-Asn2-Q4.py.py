# Use Mediapipe to extract pose landmarks and use arm or leg landmarks positions to calculate the angle
# Then Count those reps with correct angles during the exercise
# Angle between forearm and upper arm or (leg and thigh) is calculated by a trigonometric function

import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Function used to calculate angle between forearm and upper arm or (leg and thigh)
def calculate_angle(a, b, c):
    a = np.array(a)  # Point 1
    b = np.array(b)  # Point 2, middle point
    c = np.array(c)  # Point 3

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle
    return angle

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1100)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

# Curl/squat counter variables
#counter = 0
stage = None

# Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.5) as pose:
    while cam.isOpened():
        ret, img = cam.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    # Recolor image to RGB
        imgRGB.flags.writeable = False
        results = pose.process(imgRGB)                   # Make detection
        imgRGB.flags.writeable = True
        img = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)    # Recolor back to BGR

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
                # Get coordinates from wrist, elbow and shoulder
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                # Get coordinates from hip, knee and ankle (23,25,27)
            # hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
            #        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            # knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
            #         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            # ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
            #          landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            angle = calculate_angle(shoulder, elbow, wrist)     # Call function and calculate angle
            # angle = calculate_angle(hip, knee, ankle)

            # Display angle value to frame
            cv2.putText(img, str(angle), tuple(np.multiply(elbow, [900, 600]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                        2, cv2.LINE_AA
                        )
            # Curl/squat counter logic
            if angle > 175 and angle < 178:
                stage = "four"
            elif angle > 110 and angle < 113:
                stage = "three"
            elif angle > 80 and angle < 83:
                stage = "two"
            elif angle > 50 and angle < 53:
                stage = "one"
            else:
                stage = ""
            """if angle < 70 and stage == 'down':
                stage = "up"
                counter += 1
                #print(counter)"""
        except:
            pass
        # show curl/squat counter and setup status box
        #cv2.rectangle(img, (0, 0), (280, 85), (240, 100, 80), -1)
        """# Rep data
        cv2.putText(img, 'REPS', (15, 25),cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img, str(counter),(10, 75),cv2.FONT_HERSHEY_SIMPLEX, 2,
                    (255, 255, 255), 2, cv2.LINE_AA)"""
        # Stage data
        cv2.putText(img, 'sign language:',(15, 25),cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img, stage,(15, 75),cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                    (255, 255, 255), 2, cv2.LINE_AA)
        # show detections
        mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )
        cv2.imshow('IVE(LWL) Department of Engineering', img)

        if cv2.waitKey(5) & 0xFF == 32:
            counter = 0
        if cv2.waitKey(5) & 0xFF == 27:
            break
cam.release()
cv2.destroyAllWindows()