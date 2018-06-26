# Image Writer Example
#
# USE THIS EXAMPLE WITH A USD CARD! Reset the camera after recording to see the file.
#
# This example shows how to use the Image Writer object to record snapshots of what your
# OpenMV Cam sees for later analysis using the Image Reader object. Images written to disk
# by the Image Writer object are stored in a simple file format readable by your OpenMV Cam.

import sensor, image, pyb, time
import uos

# print("branch test.")

record_time = 50000 # 50 seconds in milliseconds

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
# sensor.set_framesize(sensor.QQVGA)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
# sensor.skip_frames(time = 2000)
sensor.skip_frames(time = 20000)
clock = time.clock()

curDir = uos.ilistdir()
iMax = 0
tagFileName = 'img'
for i in curDir:
    if i[1] == 0x8000:
        fileName = i[0]
        #print(fileName[0:5])
        if fileName[0:3] == tagFileName:
            if int(fileName[3:-4]) >= iMax:
                iMax = int(fileName[3:-4]) + 1

streamFileName = tagFileName + str(iMax) + '.bin'

img_writer = image.ImageWriter(streamFileName)

# create a directory to hold images
try:
    uos.mkdir("/imgs")
except OSError:
    print("path '/imgs' already existed.")

# Red LED on means we are capturing frames.
# red_led = pyb.LED(1)
# red_led.on()

tag = 1
jMax = 0
# tagImgName = 'stream'
start = pyb.millis()
while pyb.elapsed_millis(start) < record_time:
    clock.tick()
    img = sensor.snapshot()
    # Modify the image if you feel like here...

    img_writer.add_frame(img)
    # print(clock.fps())
    if (tag % 1) == 0:
        imgDir = uos.ilistdir("/imgs")
        for j in imgDir:
            if j[1] == 0x8000:
                imgFileName = j[0]
                if imgFileName[0:3] == tagFileName:
                    if int(imgFileName[3:-4]) >= jMax:
                        jMax = int(imgFileName[3:-4]) + 1

        streamImgName = '/imgs/' + tagFileName + str(jMax) + '.bmp'
        try:
            img.save(streamImgName)
            print('image ' + str(jMax) + ' saved.')
        except AttributeError:
            print("image save failed.")
    tag = tag + 1

img_writer.close()

# Blue LED on means we are done.
# red_led.off()
blue_led = pyb.LED(3)
blue_led.on()

print("Done")
while(True):
    pyb.wfi()
