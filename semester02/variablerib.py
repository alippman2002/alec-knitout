# Setup
import sys
sys.path.append("/Users/aleclippman/Desktop/Knit/additionalresources")
sys.path.append('/Users/aleclippman/Desktop/Knit/knitout-frontend-py')
from hereadWrappers import *
import knitout



k = knitout.Writer('1 2 3 4 5 6')
k.addHeader('Machine', 'swg')
carrier = '1'

k.inhook(carrier)

# Let r1 be the amount of 1x1 rib for flat part of fold (first part)
r1 = 4
# Let b be the amount of needles knit on back bed (valley)
b = 4
# Let r2 be the amount of 1x1 rib for flat part of fold (second part)
r2 = 12
# Let f be the amount of needles knit on front bed (mountain)
f = 6

# Let the width allow for 5 iterations of this pattern
width = (r1+b+r2+f) * 5

# Can be arbitrary
height = 80

for i in range(width - 1, 0, -2):
    bed = 'f'
    if i%2:
        bed = 'b'
    # This pass tucks along the back bed 
    k.tuck('-', (bed,i), carrier)

k.releasehook(carrier)

for i in range(0, width, 2):
    bed = 'f'
    if i%2:
        bed = 'b'
    # This pass tucks along the front bed
    k.tuck('+', (bed,i), carrier)

# WRITE TRANSFER INSTRUCTIONS BASED ON REMAINDER OF (r,b,r2,f)

iteration = r1 + b + r2 + f
# Create list of out iteration to check for remainders for patterning fold! 
r1rem = []
for i in range(0, r1):
    r1rem.append(i)
brem = []
for i in range(r1, r1+b):
    brem.append(i)
r2rem = []
for i in range(r1+b, r1+b+r2):
    r2rem.append(i)
frem = []
for i in range(r1+b+r2, r1+b+r2+f):
    frem.append(i)

# Transfer based on specifc patterns
# Based on cast on, keep odd needles on b bed, even needles on f bed for 1x1 rib
for i in range(width - 1, -1, -1):
    if i%iteration in r1rem:
        # No transfers needed as cast on sets up 1x1 rib
        break
    if i%iteration in brem:
        # Transfer to b bed if i%2 = 0
        if not i%2:
            k.xfer(('f',i), ('b',i))
    if i%iteration in r2rem:
        # No transfers needed as cast on sets up 1x1 rib
        break
    if i%iteration in frem:
        # Transfer to f if i%2 = 1
        if i%2:
            k.xfer(('b',i), ('f',i))

# Knit
for j in range(0, height):
    if j%2 == 0:
        for i in range(0, width, 1):
            if i%iteration in r1rem:
                # Knit 1x1 Rib
                if i%2:
                    k.knit('+', ('f',i), carrier)
                else:
                    k.knit('+', ('b',i), carrier)
            if i%iteration in frem:
                # Knit F
                k.knit('+', ('f',i), carrier)
            if i%iteration in r2rem:
                # Knit 1x1 Rib
                if i%2:
                    k.knit('+', ('f',i), carrier)
                else:
                    k.knit('+', ('b',i), carrier)
            if i%iteration in brem:
                # Knit B
                k.knit('+', ('b',i), carrier)
    else:
        for i in range(width - 1, 0, -1):
            if i%iteration in r1rem:
                # Knit 1x1 Rib
                if i%2:
                    k.knit('-', ('f',i), carrier)
                else:
                    k.knit('-', ('b',i), carrier)
            if i%iteration in frem:
                # Knit F
                k.knit('-', ('f',i), carrier)
            if i%iteration in r2rem:
                # Knit 1x1 Rib
                if i%2:
                    k.knit('-', ('f',i), carrier)
                else:
                    k.knit('-', ('b',i), carrier)
            if i%iteration in brem:
                # Knit B
                k.knit('-', ('b',i), carrier)
        

k.outhook(carrier)
for i in range(0, width):
    # Since ribbing is on both beds, drop f and b!
    k.drop('f', i)
    k.drop('b', i)
k.write('alec-variable-rib-test-'+str(r1)+'-'+str(b)+'-'+str(r2)+'-'+str(f)+str(width)+'x'+str(height)+'.k')