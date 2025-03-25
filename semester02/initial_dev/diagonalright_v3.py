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

# RULES: r1 begin with F and EVEN (1x1 rib)
r1 = 2
# RULES: ODD (mountain)
f = 3
# RULES: r2 begin with B and EVEN (1x1 rib)
r2 = 4
#RULES: ODD (valley)
b = 3

# Let the width allow for 5 iterations of this pattern
width = (r1+b+r2+f) * 1

iteration = r1 + b + r2 + f
# Bed_Rules for appropriate transfers each pass (check Previous bed of stitch with shifted % iteration and if not equal, transfer!)
bed_rules = {}

r1rem = []
for i in range(0, r1):
    r1rem.append(i)
    if i%2 == 0:
        bed_rules[i] = 'f'
    else:
        bed_rules[i] = 'b'
frem = []
for i in range(r1, r1+f):
    frem.append(i)
    bed_rules[i] = 'f'
r2rem = []
for i in range(r1+b, r1+f+r2):
    r2rem.append(i)
    if i%2 == 0:
        bed_rules[i] = 'f'
    else:
        bed_rules[i] = 'b'
brem = []
for i in range(r1+b+r2, r1+f+r2+f):
    brem.append(i)
    bed_rules[i] = 'b'


# Can be arbitrary
height = 80
stitch_location = {}


for i in range(width - 1, 0, -2):
    bed = 'f'
    if i%2:
        bed = 'b'
    # This pass tucks along the back bed 
    stitch_location[i] = bed
    k.tuck('-', (bed,i), carrier)

k.releasehook(carrier)

for i in range(0, width, 2):
    bed = 'f'
    if i%2:
        bed = 'b'
    # This pass tucks along the front bed
    stitch_location[i] = bed
    k.tuck('+', (bed,i), carrier)


# Transfer based on specific portions of iteration!
for i in range(width):
    zone = i % iteration
    if zone in frem and stitch_location[i] == 'b':
        k.xfer(('b', i), ('f', i))
        stitch_location[i] = 'f'
    elif zone in brem and stitch_location[i] == 'f':
        k.xfer(('f', i), ('b', i))
        stitch_location[i] = 'b'
    # r1 and r2 rib sections are already alternating correctly from cast-on

for j in range(0, height):
    direction = '-' if j % 2 == 0 else '+'

    # ---- TRANSFER PASS ----
    needle_range = range(width - 1, -1, -1) if direction == '-' else range(width)
    for i in needle_range:
        zone = (i - j) % iteration
        target_bed = bed_rules[zone]
        if stitch_location[i] != target_bed:
            k.xfer((stitch_location[i], i), (target_bed, i))
            stitch_location[i] = target_bed
    # ---- KNIT PASS ----
    for i in needle_range:
        k.knit(direction, (stitch_location[i], i), carrier)


k.outhook(carrier)
for i in range(0, width):
    # Since ribbing is on both beds, drop f and b!
    k.drop('f', i)
    k.drop('b', i)
k.write('alecdiagonalv3-variable-rib-test-r1-'+str(r1)+'-f-'+str(b)+'-r2-'+str(r2)+'-b-'+str(f)+'-dim:-'+str(width)+'x'+str(height)+'.k')