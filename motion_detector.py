# motion_detector.py runs camera and detects motion

import cv2, time, pandas
from datetime import datetime

first_frame = None
status_list = [None,None]
times = []
df = pandas.DataFrame(columns=["Start","End"])

video=cv2.VideoCapture(0)

#determines default frame resolutions
frame_width = int(video.get(3))
frame_height = int(video.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'output.avi'
# The fps is set at 16 but this can be varied as needed.
out = cv2.VideoWriter('motion_output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 16, (frame_width,frame_height))

# compare still first frame to subsequent frames for motion detection
while True:
    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21), 0)

    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame,gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:    # can adjust number to change motion frame sizing
            continue
        status = 1

        (x, y, w, h) = cv2.boundingRect(contour)
        reci = cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)
    status_list.append(status)

    status_list=status_list[-2:] #shortens unneeded parts of list to lower file size


    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    out.write(frame)    ## Write the frame into the file 'motion_output.avi'. Includes green detection rectangles.
    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key=cv2.waitKey(1)

    if key == ord('q'):         #press q to quit
        if status == 1:
            times.append(datetime.now())        
        break

for i in range(0,len(times), 2):
    df=df.append({"Start":times[i], "End":times[i+1]}, ignore_index=True)

df.to_csv("Times.csv")      #output goes directly to plotting.py

video.release()
out.release()   #The VideoWriter object is also released
cv2.destroyAllWindows