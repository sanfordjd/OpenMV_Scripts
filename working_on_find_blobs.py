# Image Reader Example
#
# USE THIS EXAMPLE WITH A USD CARD!
#
# This example shows how to use the Image Reader object to replay snapshots of what your
# OpenMV Cam saw saved by the Image Writer object for testing machine vision algorithms.

import sensor, image, time

snapshot_source = False # Set to true once finished to pull data from sensor.

sensor.reset()
#sensor.set_pixformat(sensor.RGB565)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

gray_threshold = (30,55)
roi = (97,84,24,12 )
#img_reader = None if snapshot_source else image.ImageReader("/stream.bin")

while(True):
    clock.tick()
    img = sensor.snapshot()# if snapshot_source else img_reader.next_frame(copy_to_fb=True, loop=True)
    blob_list =  img.find_blobs([gray_threshold], [roi])
    #blob_list =  img.find_blobs([gray_threshold], x_stride=2, y_stride=1, invert=False, area_threshold=10, pixels_threshold=10, merge=False, margin=0, threshold_cb=None, merge_cb=None)

    #print(blob_list)
    largest_blob = max(blob_list, key = lambda x: x.pixels())
    if largest_blob[5] > 2000:
        print(largest_blob)

    print(clock.fps())
