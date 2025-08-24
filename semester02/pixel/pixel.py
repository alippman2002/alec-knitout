from PIL import Image
import numpy as np
import sys
sys.path.append("/Users/aleclippman/Desktop/Knit/additionalresources")
sys.path.append('/Users/aleclippman/Desktop/Knit/knitout-frontend-py')
from hereadWrappers import *
import knitout
import castonbindoff

k = knitout.Writer('1 2 3 4 5 6 7 8 9 10')
k.rack(0.25)
k.addHeader('Machine', 'SWG061N2')
k.addHeader('Position', 'Center')
carrier = '7'
k.ingripper(carrier)

xferspeed = 3
knitspeed = 10
stitch_size = 90
k.stitchNumber(stitch_size)

# Using Red, White, Black (RGB values for default Adobe Photoshop Colors)
# White -> Mountain
# Black -> Flat
# Red -> Valley

# TODO- Open the desired pixel file below
img = Image.open('/Users/aleclippman/Desktop/Knit/alec-knitout/semester02/pixel/pixel_ref/FinalPixel/finalwaterbombtest2horizontalscale.png')

# TODO- Tile pixel file based on desired size
width_iterations = 1
height_iterations = 1

width, height = img.size
patternarray = np.empty((height, width), dtype='str')
pixel_array = np.empty((height, width), dtype='object')

for y in range(height):
    for x in range(width):
        pixel = img.getpixel((x, height - 1 - y))
        if pixel == (255, 255, 255, 255):
            patternarray[y][x] = 'M'
        elif pixel == (0, 0, 0, 255):
            patternarray[y][x] = 'F'
        elif pixel == (255, 39, 37, 255):
            patternarray[y][x] = 'V'

full_pattern = np.tile(patternarray, (height_iterations, width_iterations))

# TODO- Adjust Side Ribbing on outsides of swatch
side_rib = np.full((full_pattern.shape[0], 5), 'F')
full_pattern = np.hstack((side_rib, full_pattern, side_rib))

knit_width = full_pattern.shape[1]
knit_height = full_pattern.shape[0]
stitch_location = {}

k.speedNumber(knitspeed)
for i in range(knit_width -1, -1, -1):
    k.tuck('-', ('b', i), carrier)
    k.tuck('-', ('f', i), carrier)
    stitch_location[i] = 'both'

# Cast-On
for r in range(10):
    direction = '+' if r % 2 == 0 else '-'
    knitting_range = range(knit_width) if direction == '+' else range(knit_width - 1, -1, -1)
    for i in knitting_range:
        if direction == '+':
            k.knit(direction, ('f', i), carrier)
        else:
            k.knit(direction, ('b', i), carrier)

k.speedNumber(xferspeed)
half_pitch = True
transfer = False

# Transfer from caston to prep for main swatch
for i in range(knit_width - 1, -1, -1):
    first_stitch = full_pattern[0][i]
    if first_stitch == 'M':
        if half_pitch:
            k.rack(0.0)
            half_pitch = False
        k.xfer(('b',i), ('f', i))
        transfer = True
        stitch_location[i] = 'f'
    if first_stitch == 'F':
        stitch_location[i] = 'both'

    if first_stitch == 'V':
        if half_pitch:
            k.rack(0.0)
            half_pitch = False
        k.xfer(('f',i), ('b', i))
        transfer = True
        stitch_location[i] = 'b'
if transfer:
    k.rack(0.25)


true_last_direction = None

# Main Knitting Loop
for j in range(knit_height):
    k.speedNumber(knitspeed)
    direction = '+' if j % 2 == 0 else '-'
    true_last_direction = direction
    knitting_range = range(knit_width) if direction == '+' else range(knit_width - 1, -1, -1)
    if knitting_range == range(knit_width):
        transfer_range = range(knit_width - 1, -1, -1)
    elif knitting_range == range(knit_width - 1, -1, -1):
        transfer_range = range(knit_width)
    for i in knitting_range:
        curr_stitch = full_pattern[j][i]
        next_stitch = full_pattern[j+1][i] if j + 1 < knit_height else curr_stitch
        # Mountain to Flat: Phase change where double knitting occurs to lock tuck in! (Taken out in development with Shima)
        if curr_stitch == 'M' and next_stitch == 'F':
            if direction == '+':
                k.knit(direction, ('f', i), carrier)
            #   k.tuck(direction, ('b', i), carrier)
            #   k.knit(direction, ('f', i), carrier)
            elif direction == '-':
            #    k.knit(direction, ('f', i), carrier)
            #    k.tuck(direction, ('b', i), carrier)
                k.knit(direction, ('f', i), carrier)
            stitch_location[i] = 'both'
            continue
        # Valley to Flat:
        if curr_stitch == 'V' and next_stitch == 'F':
            if direction == '+':
            #  k.knit(direction, ('b', i), carrier)
            #    k.tuck(direction, ('f', i), carrier)
                k.knit(direction, ('b', i), carrier)
            elif direction == '-':
                k.knit(direction, ('b', i), carrier)
            #    k.tuck(direction, ('f', i), carrier)
            #     k.knit(direction, ('b', i), carrier)
            stitch_location[i] = 'both'
            continue
        # Flat logic
        if curr_stitch == 'F':
            # Knit f0 b0 in + direction, b0 f0 in - direction
            bed = 'f' if j % 2 == 0 else 'b'
            second_bed = 'b' if bed == 'f' else 'f'
            # k.knit(direction, (second_bed, i), carrier)
            # k.knit(direction, (bed, i), carrier)
            k.knit(direction, (bed, i), carrier)
            k.knit(direction, (second_bed, i), carrier)
            continue
        # Mountain/Valley Logic
        elif curr_stitch == 'M' or curr_stitch == 'V':
            bed = stitch_location.get(i)
            # Error catch
            if bed == 'both':
                if direction == '+':
                    k.knit(direction, ('f', i), carrier)
                    k.knit(direction, ('b', i), carrier)
                else:
                    k.knit(direction, ('b', i), carrier)
                    k.knit(direction, ('f', i), carrier)
            else:
                k.knit(direction, (bed, i), carrier)


    # Transfer Check to Prep for Next Row
    k.speedNumber(xferspeed)
    half_pitch = True
    transfer = False
    for i in transfer_range:
        curr_stitch = full_pattern[j][i]
        next_stitch = full_pattern[j+1][i] if j + 1 < knit_height else curr_stitch
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
        k.rack(0.25)

tuck_range = range(knit_width) if true_last_direction == '-' else range(knit_width - 1, -1, -1)
k.speedNumber(knitspeed)
tucked = False

# Knit 10 rows of full needle rib alternating directions to finish swatch
if tucked:
    direction = '-' if tuck_range == range(knit_width) else '+'
if not tucked:
    direction = '+' if true_last_direction == '-' else '-'
for r in range(10):
    knitting_range = range(knit_width) if direction == '+' else range(knit_width - 1, -1, -1)
    for i in knitting_range:
        if direction == '+':
            k.knit(direction, ('f', i), carrier)
            k.knit(direction, ('b', i), carrier)
        else:
            k.knit(direction, ('b', i), carrier)
            k.knit(direction, ('f', i), carrier)
    
    # Flip direction for next row
    direction = '-' if direction == '+' else '+'

# Complete the swatch
k.outgripper(carrier)

for i in range(0, knit_width):
    k.drop(('f', i))
for i in range (knit_width - 1, -1, -1):
    k.drop(('b', i))

file_name = img.filename
print(f'.k file written to: {file_name}')
k.write(f'{file_name}.k')