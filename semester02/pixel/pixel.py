from PIL import Image
import numpy as np
import sys
sys.path.append("/Users/aleclippman/Desktop/Knit/additionalresources")
sys.path.append('/Users/aleclippman/Desktop/Knit/knitout-frontend-py')
from hereadWrappers import *
import knitout

k = knitout.Writer('1 2 3 4 5 6')
k.rack(0.5)
k.addHeader('Machine', 'swg')
carrier = '1'
k.inhook(carrier)

# Using Red, White, Black
# White -> Mountain
# Black -> Flat
# Red -> Valley

# Add Image File Name In
# PixilArt: https://www.pixilart.com/draw
# Front
# img = Image.open("/Users/aleclippman/Desktop/Knit/alec-knitout/semester02/pixel/pixel_ref/Front.png")
img = Image.open("/Users/aleclippman/Desktop/Knit/alec-knitout/semester02/pixel/pixel_ref/Flat.png")
# img = Image.open("/Users/aleclippman/Desktop/Knit/alec-knitout/semester02/pixel/pixel_ref/Back.png")
# img = Image.open("/Users/aleclippman/Desktop/Knit/alec-knitout/semester02/pixel/pixel_ref/ShiftedTransfers3x2.png")
# img = Image.open("/Users/aleclippman/Desktop/Knit/alec-knitout/semester02/pixel/pixel_ref/6by6_3flat_3mountain.png")
# Customize for Swatch Size
width_iterations = 1
height_iterations = 1

width, height = img.size
print(f"Image width and height: {width, height}")
patternarray = np.empty((height, width), dtype='str')
pixel_array = np.empty((height, width), dtype='object')
for y in range(height):
    for x in range(width):
        pixel = img.getpixel((x, height - 1 - y))
        pixel_array[y][x] = pixel
        if pixel == (255, 255, 255, 255):
            patternarray[y][x] = 'M'
        elif pixel == (0, 0, 0, 255):
            patternarray[y][x] = 'F'
        elif pixel == (244, 67, 54, 255):
            patternarray[y][x] = 'V'


full_pattern = np.tile(patternarray, (height_iterations, width_iterations))
knit_width = full_pattern.shape[1]
knit_height = full_pattern.shape[0]
stitch_location = {}
# Cast-On Tucks
for i in range(knit_width - 1, -1, -1):
    if full_pattern[0][i] == 'M':
        stitch_location[i] = 'f'
        k.tuck('-', ('f', i), carrier)
    if full_pattern[0][i] == 'F':
        stitch_location[i] = 'both'
        k.tuck('-', ('b', i), carrier)
        k.tuck('-', ('f', i), carrier)
    elif full_pattern[0][i] == 'V': 
        stitch_location[i] = 'b'
        k.tuck('-', ('b', i), carrier)

# def transfer_function:

for j in range(knit_height):
    # Setting Up Knit Command
    direction = '+' if j % 2 == 0 else '-'
    print(f"Direction at knitting row {j} is: {direction}")
    knitting_range = range(knit_width) if direction == '+' else range(knit_width - 1, -1, -1)
    if knitting_range == range(knit_width):
        transfer_range = range(knit_width - 1, -1, -1)
    elif knitting_range == range(knit_width - 1, -1, -1):
        transfer_range = range(knit_width)
    
    print(f"Transfer Range: {transfer_range}")
    # Complete tucks in knit pass to set up for next rows
    for i in knitting_range:
        curr_stitch = full_pattern[j][i]
        print(f"Knitting Needle {i} and curr_stitch: {curr_stitch}")

        next_stitch = full_pattern[j+1][i] if j + 1 < knit_height else curr_stitch

        # Mountain to Flat:
        if curr_stitch == 'M' and next_stitch == 'F':
            if direction == '+':
                k.knit(direction, ('f', i), carrier)
                k.tuck(direction, ('b', i), carrier)
            elif direction == '-':
                k.tuck(direction, ('b', i), carrier)
                k.knit(direction, ('f', i), carrier)
            stitch_location[i] = 'both'
            continue
        # Valley to Flat:
        if curr_stitch == 'V' and next_stitch == 'F':
            if direction == '+':
                k.tuck(direction, ('f', i), carrier)
                k.knit(direction, ('b', i), carrier)
            elif direction == '-':
                k.knit(direction, ('b', i), carrier)
                k.tuck(direction, ('f', i), carrier)
            stitch_location[i] = 'both'
            continue
        # Flat logic
        if curr_stitch == 'F':
            # Knit f0 b0 in + direction, b0 f0 in - direction
            bed = 'f' if j % 2 == 0 else 'b'
            second_bed = 'b' if bed == 'f' else 'f'
            # print(f"Bed at {i}: {bed}, and Second_bed at {i}: {second_bed}")
            # k.knit(direction, (second_bed, i), carrier)
            # k.knit(direction, (bed, i), carrier)
            k.knit(direction, (bed, i), carrier)
            k.knit(direction, (second_bed, i), carrier)
            continue
        # Mountain/Valley Logic
        elif curr_stitch == 'M' or curr_stitch == 'V':
            bed = stitch_location.get(i)
            k.knit(direction, (bed, i), carrier)
    
    half_pitch = True
    transfer = False
    # Transfer Check to Prep for Next Row
    for i in transfer_range:
        print("Transfer Checking on Needle {i}")
        curr_stitch = full_pattern[j][i]
        print(f"Curr_stitch: {curr_stitch}")
        next_stitch = full_pattern[j+1][i] if j + 1 < knit_height else curr_stitch
        print(f"Next_stitch : {next_stitch}")
        curr_bed = stitch_location.get(i)
        # Transfer Scenarios:
        if curr_stitch == 'M' and next_stitch == 'F':
            # In knitting pass, tuck on b
            continue
        if curr_stitch == 'V' and next_stitch == 'F':
            # in knitting pass, tuck on f
            continue
        if curr_stitch == 'F' and next_stitch == 'M':
            if half_pitch:
                k.rack(0.0)
            half_pitch = False
            k.xfer(('b',i), ('f', i))
            transfer = True
            stitch_location[i] = 'f'
        if curr_stitch == 'F' and next_stitch == 'V':
            if half_pitch:
                k.rack(0.0)
            half_pitch = False
            k.xfer(('f',i), ('b', i))
            transfer = True
            stitch_location[i] = 'b'
        if curr_stitch == 'M' and next_stitch == 'V':
            if half_pitch:
                k.rack(0.0)
            half_pitch = False
            k.xfer(('f', i), ('b', i))
            transfer = True
            stitch_location[i] = 'b'
        if curr_stitch == 'V' and next_stitch == 'M':
            if half_pitch:
                k.rack(0.0)
            half_pitch = False
            k.xfer(('b', i), ('f', i))
            transfer = True
            stitch_location[i] = 'f'
    if transfer:
        k.rack(0.5)

k.outhook(carrier)

for i in range(0, knit_width):
    # Since ribbing is on both beds, drop f and b!
    k.drop('f', i)
    k.drop('b', i)

# Enter Output File Name
file_name = 'FlatTestChangedBEds'
k.write(f'{file_name}.k')
