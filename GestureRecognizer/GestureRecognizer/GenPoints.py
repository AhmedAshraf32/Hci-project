import os
import cv2
import mediapipe as mp

# initialize Pose estimator
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)






def loop_files(directory):
    f = open(directory+"TestDollar.Py", "w")
    f.write("from dollarpy import Recognizer, Template, Point\n")
    recstring=""
    for file_name in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file_name)):
            if file_name.endswith(".mp4"):
                print(file_name)
                foo = file_name[:-4]
                recstring+=foo+","
                f.write (""+foo+" = Template('"+foo+"', [\n")
                # create capture object
                cap = cv2.VideoCapture(directory+""+file_name)
                framecnt=0
                while cap.isOpened():
                    # read frame from capture object
                    ret, frame = cap.read()
                    if not ret:
                        print("Can't receive frame (stream end?). Exiting ...")
                        break
                    frame = cv2.resize(frame, (480, 320))
                    framecnt+=1
                    
                    
                    # convert the frame to RGB format
                    RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    print (framecnt)
                    # process the RGB frame to get the result
                    results = pose.process(RGB)
                    if results.pose_landmarks:  # Check if pose_landmarks is not None
                        image_hight, image_width, _ = frame.shape
                        try:
                            x = str(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * image_width))
                            y = str(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * image_hight))
                            f.write("Point(" + x + "," + y + ", 1),\n")
                            
                            x = str(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x * image_width))
                            y = str(int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y * image_hight))
                            f.write("Point(" + x + "," + y + ", 1),\n")
                        except:
                            pass
                    else:
                    # No pose landmarks detected, write Point(0, 0, 1)
                        f.write("Point(0, 0, 1),\n")
                        f.write("Point(0, 0, 1),\n")
                    # draw detected skeleton on the frame
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    # show the final output
                    cv2.imshow('Output', frame)
                    
                    if cv2.waitKey(1) == ord('q'):
                            break
                f.write ("])\n")    
                cap.release()
                cv2.destroyAllWindows()
    recstring = recstring[:-1]
    f.write ("recognizer = Recognizer(["+recstring+"])\n")    
    f.close()

# Example usage
directory_path = "C:/Users/moham/OneDrive/Desktop/Learning/LEVEL4/Semester 2/HCI/Project/tem/"

loop_files(directory_path)



#directory_path1 = "D:/D Folder/HARSkelton/HARWithSkelton/test"
#StartTest(directory_path1)

