import io, picamera, pygame, sys, os
import argparse
import cv2
import numpy as np
from cv2 import dnn
from pygame.locals import *
os.environ["SDL_FBDEV"] = "/dev/fb1"

parser = argparse.ArgumentParser()
parser.add_argument("--video", help="number of video device", default=0)
parser.add_argument("--prototxt", default="mobilenet_v2_deploy.prototxt")
parser.add_argument("--caffemodel", default="mobilenet_v2.caffemodel")
parser.add_argument("--classNames", default="synset.txt")
args = parser.parse_args()

width = 480
height= 640
camera = picamera.PiCamera()
camera.resolution = (width, height)
camera.rotation = 90
offset = 22

net = dnn.readNetFromCaffe(args.prototxt, args.caffemodel)
f = open(args.classNames, 'r')
rawClassNames = f.readlines()
classNames = []
for nameStr in rawClassNames:
    spaceIndex = nameStr.find(' ')
    nameStr = nameStr[spaceIndex:-2]
    classNames.append(nameStr)

inWidth = 224
inHeight = 224
inScaleFactor = 0.017
meanVal = (103.94, 116.78, 123.68)
resultText = None

pygame.init()
screen = pygame.display.set_mode((160, 124), 0, 32)
screen.fill(0)

basicfont = pygame.font.SysFont(None, 15)

# run the game loop
while True:
    screen.fill(0)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    frame = np.empty((width * height * 3), dtype=np.uint8)
    camera.capture(frame, format='rgb')
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

    img = pygame.image.frombuffer(frame.tobytes(), (width, height), 'RGB')
    img = pygame.transform.scale(img, (int(img.get_width() * 80 / img.get_height()), 80))
    screen.blit(img, (0, offset))

    if (resultText != None):
        screen.fill((0, 0, 0), resultText.get_rect())

    print("class id: ", maxClassId)
    print("class point: ", maxClassPoint)
    print("name: ", classNames[maxClassId])
    resultText = basicfont.render(classNames[maxClassId], True, (255, 255, 255))
    textrect = resultText.get_rect()
    textrect.left = img.get_width()
    textrect.centery = screen.get_rect().centery
    screen.blit(resultText, textrect)

    pygame.display.update()
