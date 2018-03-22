import picamera
import argparse
import cv2
from cv2 import dnn
import numpy as np

width = 480
height= 640
rgb_buffer = bytearray(width * height * 3)
camera = picamera.PiCamera()
camera.resolution = (width, height)
camera.rotation = 90

inWidth = 224
inHeight = 224
inScaleFactor = 0.017
meanVal = (103.94, 116.78, 123.68)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", help="number of video device", default=0)
    parser.add_argument("--prototxt", default="mobilenet_v2_deploy.prototxt")
    parser.add_argument("--caffemodel", default="mobilenet_v2.caffemodel")
    parser.add_argument("--classNames", default="synset.txt")
    #parser.add_argument("--thr", default=0.2, help="confidence threshold to filter out weak detections")
    args = parser.parse_args()
    net = dnn.readNetFromCaffe(args.prototxt, args.caffemodel)
    cap = cv2.VideoCapture(args.video)
    f = open(args.classNames, 'r')
    classNames = f.readlines()

    while True:
        frame = np.empty((width * height * 3), dtype=np.uint8)
        camera.capture(frame, format='bgr')
        frame = frame.reshape((height, width, 3))
        blob = dnn.blobFromImage(frame, inScaleFactor, (inWidth, inHeight), meanVal)
        net.setInput(blob)
        detections = net.forward()

        maxClassId = 0
        maxClassPoint = 0;
        for i in range(detections.shape[1]):
            classPoint = detections[0, i, 0, 0]
            if (classPoint > maxClassPoint):
                maxClassId = i
                maxClassPoint = classPoint

        print("class id: ", maxClassId)
        print("class point: ", maxClassPoint)
        print("name: ", classNames[maxClassId])

        # frame = pygame.transform.scale(frame, (int(frame.get_width() * 80 / frame.get_height()), 80))
