# Image Reader Example
#
# USE THIS EXAMPLE WITH A USD CARD!
#
# This example shows how to use the Image Reader object to replay snapshots of what your
# OpenMV Cam saw saved by the Image Writer object for testing machine vision algorithms.

import sensor, image, time
import uos

snapshot_source = False # Set to true once finished to pull data from sensor.

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

img_reader = None if snapshot_source else image.ImageReader("/stream.bin")

try:
    uos.mkdir("/imgs")
except OSError:
    print("path '/imgs' already existed.")

tag = 1

loopTag = True

while(loopTag):
    clock.tick()
    img = sensor.snapshot() if snapshot_source else img_reader.next_frame(copy_to_fb=True, loop=False)
    # Do machine vision algorithms on the image here.
    if tag < 1000:
        imgPathName = "/imgs/test" + str(tag) + ".bmp"
        try:
            img.save(imgPathName)
        except AttributeError:
            loopTag = False
    tag = tag + 1
    print(clock.fps())
