import os
import cv2
import mediapipe as mp
from TestDollar import recognizer, Point, Template

# initialize Pose estimator
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

cap = cv2.VideoCapture(1)
framecnt=0



Allpoints=[]









while cap.isOpened():
    # read frame from capture object
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    frame = cv2.resize(frame, (480, 320))
    framecnt+=1
    try:
        # convert the frame to RGB format
        RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #print (framecnt)
        # process the RGB frame to get the result
        results = pose.process(RGB)
            # Loop through the detected poses to visualize.
        #for idx, landmark in enumerate(results.pose_landmarks.landmark):
            #print(f"{mp_pose.PoseLandmark(idx).name}: (x: {landmark.x}, y: {landmark.y}, z: {landmark.z})")
        
            # Print nose landmark.
        image_hight, image_width, _ = frame.shape
        x=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * image_width))
        y=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * image_hight))
        
        Allpoints.append(Point(x,y,1))
        x=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x * image_width))
        y=(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y * image_hight))
        
        Allpoints.append(Point(x,y,1))

        if framecnt%30==0:
              framecnt=0
              #print (Allpoints)
              result = recognizer.recognize(Allpoints)
              print (result)
              Allpoints.clear()  
        
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        # show the final output
        cv2.imshow('Output', frame)
        
    except:
            #break
            print ('Camera Error')
    if cv2.waitKey(1) == ord('q'):
            break
 
cap.release()
cv2.destroyAllWindows()