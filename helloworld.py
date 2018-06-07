# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time
import utime, urandom, uos

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
# sensor.set_framesize(sensor.VGA)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

curDir = uos.ilistdir()
iMax = 0
for i in curDir:
    if i[1] == 0x8000:
        fileName = i[0]
        #print(fileName[0:5])
        if fileName[0:6] == 'stream':
            if int(fileName[6:-4]) >= iMax:
                iMax = int(fileName[6:-4]) + 1

streamFileName = 'stream' + str(iMax) + '.bin'
print(streamFileName)

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    #print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
                                    # to the IDE. The FPS should increase once disconnected.
    #curTimeSec = utime.time()
    #print(utime.localtime(curTimeSec))
    curTime = utime.localtime()
    #n = pyb.rng() / (2 ** 30 - 1)
    n = urandom.getrandbits(10)
    print(curTime[5])
    print(curTime)
    print(n)
