# Foam-Up Detection-02 - By: joesanford - Tue Jul 20 2017

#This script is to be used in conjunction with the OpenMV Camera
#It first detects if foam is obscuring the nozzle ... if the nozzle
#is free from foam, it then looks at the shape of the stream of
#dispensed foam to determine if a "good shot" was made.

import sensor, image, pyb, time, os

snapshot_source = False # Set to true once finished to pull data from sensor.

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

binary_thresholds = [(135, 255)] # binary thresholds of the image

r = (67,22,40,25) #ROI of image
l_r = (67,22,20,25) #left half of ROI
r_r = (87,22,20,25) #right half of ROI

left_angle = 70   # these values are the angles of the largest line-segment ... with 90degrees
right_angle = 110 # being "straight down from the top of the frame". It was found empirically ...

#***************************************************************************************************
# Input from Speedy Packer
#***************************************************************************************************
# Pull Pin 0 LOW when about to dispense foam
# pin0 = Pin('P0', Pin.IN, Pin.PULL_UP) # IO Placeholder ...


#***************************************************************************************************
# Recorded Image
#***************************************************************************************************
img_reader = None if snapshot_source else image.ImageReader("/FU_IR_33_9V.bin")
#***************************************************************************************************

while(True):
    clock.tick()
    # if pin0.value() == FALSE :
    # Do the rest of the loop ... you'll need to indent everything below.

    img = sensor.snapshot() if snapshot_source else img_reader.next_frame(copy_to_fb=True, loop=True)
    #img.draw_rectangle(l_r, color = 155 ) #commented out unless needed by user
    #img.draw_rectangle(r_r, color = 155 )

    # histogram of ROI
    ##hist = img.get_histogram(roi = r)
    # this is the mean brightness of the ROI and was found to be approximately the "low end of the
    # brightness" of the IR LEDs as seen through the bag
    # if the "brightness level" is too low, that means there's something inbetween the camera and
    # the LEDs ... ie, foam.

    ##mean = hist.get_statistics()[0]

    ##if mean < 200:
    ##    print("FOAM UP")
    #else:    # do the line stuff

    #binary thresholding to make edges easier to detect
    img.binary(binary_thresholds, invert = False)
    img.erode(1) #cleaning up some noise

        #right-side ROI first
    segments_r = img.find_line_segments(roi = r_r, threshold = 1000, theta_margin = 15, rho_margin = 15, segment_threshold = 100)
    if segments_r :
        max_segment_r = max(segments_r, key = lambda x: x.length())
        if max_segment_r[6] > 0 :
            img.draw_line(max_segment_r.line(), color = 155)
            print("RL")
            print(max_segment_r)
                # this value (110) is the angle of the largest line-segment ... with 90degrees
                # being "straight down from the top of the frame". It was found empirically ...
            if max_segment_r[6] > right_angle:
                print("FOAM UP")

        #left-side ROI
    segments_l = img.find_line_segments(roi = l_r, threshold = 1000, theta_margin = 15, rho_margin = 15, segment_threshold = 100)
    if segments_l :
        max_segment_l = max(segments_l, key = lambda x: x.length())
        if max_segment_l[6] > 0 :
            img.draw_line(max_segment_l.line(), color = 155)
            print("LL")
            print(max_segment_l)
                # this value (70) is the angle of the largest line-segment ... with 90degrees
                # being "straight down from the top of the frame". It was found empirically ...
            if max_segment_l[6] < left_angle:
                print("FOAM UP")


    print(clock.fps())
