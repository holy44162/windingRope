# Image Reader Example
#
# USE THIS EXAMPLE WITH A USD CARD!
#
# This example shows how to use the Image Reader object to replay snapshots of what your
# OpenMV Cam saw saved by the Image Writer object for testing machine vision algorithms.

import sensor, image, time

snapshot_source = False # Set to true once finished to pull data from sensor.

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

img_reader = None if snapshot_source else image.ImageReader("/img1.bin")

# create a directory to hold images
try:
    uos.mkdir("/binImgs")
except OSError:
    print("path '/binImgs' already existed.")

imgDir = uos.ilistdir("/binImgs")
jMax = 0
while(True):
    clock.tick()
    img = sensor.snapshot() if snapshot_source else img_reader.next_frame(copy_to_fb=True, loop=True)
    # Do machine vision algorithms on the image here.
    for j in imgDir:
        if j[1] == 0x8000:
            imgFileName = j[0]
            if imgFileName[0:3] == tagFileName:
                if int(imgFileName[3:-4]) >= jMax:
                    jMax = int(imgFileName[3:-4]) + 1

    streamImgName = '/binImgs/' + tagFileName + str(jMax) + '.bmp'
    try:
        img.save(streamImgName)
        print('image ' + str(jMax) + ' saved.')
    except AttributeError:
        print("image save failed.")

    print(clock.fps())
