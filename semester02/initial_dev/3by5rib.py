# Setup
import sys
sys.path.append("/Users/aleclippman/Desktop/Knit/additionalresources")
sys.path.append('/Users/aleclippman/Desktop/Knit/knitout-frontend-py')
from hereadWrappers import *
import knitout

k = knitout.Writer('1 2 3 4 5 6')
# Half-pitch
k.rack(0.5)

# Add headers to file
k.addHeader('Machine', 'swg')
# Identify carrier used to knit with 
carrier = '1'

#Bring carrier in always
k.inhook(carrier)

# Creating a width allowing for 8 iterations of rib (3 + 5) * 8
# Should this technically be 63 (0,63 is 64?)
width = 24
height = 24

# Cast-on

# Always start at width and go to 0,'-' direction
# Begin at second to last needle, stop at 0 (not tucking here)
for i in range(width - 1, 0, -2):
    bed = 'f'
    if i%2:
        bed = 'b'
    # This pass tucks along the back bed 
    k.tuck('-', (bed,i), carrier)

# Begin at 0 needle, stop before width (not tucking here)
for i in range(0, width, 2):
    bed = 'f'
    if i%2:
        bed = 'b'
    # This pass tucks along the front bed
    k.tuck('+', (bed,i), carrier)

# Transfer Instructions (3 knit on front bed, 5 purl on back bed)
for i in range(width - 1, -1, -1):
    if i%8 in {0, 1, 2}:
        if i%2: 
            k.xfer(('b',i), ('f',i))
        else:
            # No need to transfer!
            continue
    else:
        if i%2:
            # No need to transfer!
            continue
        else:
            k.xfer(('f',i), ('b',i))
    

# Then create knit instructions repeating them by height (j)
for j in range(0, height):
    # This must be - direction, since transfers when from width - 1 to 0 does not move fiber, fiber stays at width - 1
    if j%2 == 0:
        for i in range(width - 1, -1, -1):
            if i%8 in {0, 1, 2}:
                # Knit on front bed
                k.knit('-', ('f',i), carrier)
            else:
                # Knit on back bed
                k.knit('-', ('b',i), carrier)
    # + direction
    else:
        for i in range(0, width, 1):
            if i%8 in {0, 1, 2}:
                # Knit on front bed
                k.knit('+', ('f',i), carrier)
            else:
                # Knit on back bed
                k.knit('+', ('b',i), carrier)
        

#Bring carrier out always (clarify/differences)
k.outhook(carrier)
k.releasehook(carrier)

# Drop final stitches!

for i in range(0, width):
    # Since ribbing is on both beds, drop f and b!
    k.drop('f', i)
    k.drop('b', i)

# Write code!
k.write('alec-3f-5b-rib-test-'+str(width)+'x'+str(height)+'.k')
