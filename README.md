# raspi_mobilenet_display

# Setup
```
sudo apt install pip3 python3-pygame python3-picamera
sudo pip3 install opencv_python
sudo apt install libcblas-dev libatlas3-base
```

Tested with using OpenCV 3.3.

# Usage
## Start TFT display
```
sudo modprobe fbtft_device name=adafruit18 gpios=reset:22,dc:27,cs:3 rotate=90
```

## Start scanner
```
python3 mobilenet_scan_camera.py
```

## Autostart
```
sudo modprobe fbtft_device name=adafruit18 gpios=reset:22,dc:27,cs:3 rotate=90
sudo python3 /home/pi/gitprojects/raspi_mobilenet_display/mobilenet_picamera_display.py \
  --prototxt=/home/pi/gitprojects/raspi_mobilenet_display/mobilenet_v2_deploy.prototxt \
  --caffemodel=/home/pi/gitprojects/raspi_mobilenet_display/mobilenet_v2.caffemodel \
  --classNames=/home/pi/gitprojects/raspi_mobilenet_display/synset.txt &
```

# References
- [Raspberry Pi ZeroとPicameraと0.96インチLCDで物体認識装置を作ってみた](http://asukiaaa.blogspot.jp/2018/03/raspberry-pizeropicamera096lcd.html)
- [shicai/MobileNet-Caffe](https://github.com/shicai/MobileNet-Caffe)
- [asukiaaa/py_opencv_mobilenet_practice](https://github.com/asukiaaa/py_opencv_mobilenet_practice)
- [asukiaaa/raspi_tft_display_camera](https://github.com/asukiaaa/raspi_tft_display_camera)
- [Capturing to an OpenCV object | Picamera](https://picamera.readthedocs.io/en/release-1.13/recipes2.html#capturing-to-an-opencv-object)
