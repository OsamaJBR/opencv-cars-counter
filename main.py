from imutils.video import FPS
from imutils.video import FileVideoStream
import numpy as np
import argparse
import imutils
import cv2
from cvlib.object_detection import draw_bbox
import cvlib as cv
import time
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
	help="path to input video file")
args = vars(ap.parse_args())
 
# start the file video stream thread and allow the buffer to
# start to fill
print("[INFO] starting video file thread...")
fvs = FileVideoStream(args["video"]).start()
time.sleep(5)

# start the FPS timer
fps = FPS().start()

# loop over frames from the video file stream
while fvs.more():
    frame = fvs.read()
    frame = imutils.resize(frame, width=650)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = np.dstack([frame, frame, frame])
    bbox, label, conf = cv.detect_common_objects(frame)
    out = draw_bbox(frame, bbox, label, conf)
    out = cv2.putText(frame,'cars count ::: '+str(label.count('car')),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
    cv2.imshow('window-out',out)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
stream.release()
cv2.destroyAllWindows()