# Setup
import sys
sys.path.append("/Users/aleclippman/Desktop/Knit/additionalresources")
sys.path.append('/Users/aleclippman/Desktop/Knit/knitout-frontend-py')
from hereadWrappers import *
import knitout

k = knitout.Writer('1 2 3 4 5 6')
# Half-pitch
k.rack(0.5)
k.addHeader('Machine', 'swg')
carrier = '1'

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
width =(r1+b+r2+f) * 1

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
frem = []
for i in range(r1, r1+b):
    frem.append(i)
r2rem = []
for i in range(r1+b, r1+b+r2):
    r2rem.append(i)
brem = []
for i in range(r1+b+r2, r1+b+r2+f):
    brem.append(i)


# FROM ORIGINAL CAST ON:
    # i%2=0 was cast onto F
    # i%2= 1 was cast onto B

# Transfer based on specific portions of iteration!
for i in range(0, width, 1):
    if i%iteration in r1rem:
        # No transfers needed as cast on sets up 1x1 rib
        # Odd on B
        # Even on F
        continue
    if i%iteration in frem:
        # Transfer to f bed if i%2 = 1
        if i%2:
            k.xfer(('b',i), ('f',i))
    if i%iteration in r2rem:
        # No transfers needed as cast on sets up 1x1 rib
        # Odd on B
        # Even on F
        continue
    if i%iteration in brem:
        # Transfer to b if i%2 = 0
        if not i%2:
            k.xfer(('f',i), ('b',i))

# Knit
for j in range(0, height):
    # Changed from == to is not to fix logic, xfers go in - direction, but fiber must go - first, not +
    if j%2 != 0:
        for i in range(0, width, 1):
            if i%iteration in r1rem:
                # Knit 1x1 Rib
                # Knit on back bed when true (odd)
                if i%2:
                    k.knit('+', ('b',i), carrier)
                # Knit on front bed when false (even)
                else:
                    k.knit('+', ('f',i), carrier)
            if i%iteration in frem:
                # Knit F
                k.knit('+', ('f',i), carrier)
            if i%iteration in r2rem:
                # Knit 1x1 Rib
                if i%2:
                    k.knit('+', ('b',i), carrier)
                else:
                    k.knit('+', ('f',i), carrier)
            if i%iteration in brem:
                # Knit B
                k.knit('+', ('b',i), carrier)
    else:
        for i in range(width - 1, -1, -1):
            if i%iteration in r1rem:
                # Knit 1x1 Rib
                if i%2:
                    k.knit('-', ('b',i), carrier)
                else:
                    k.knit('-', ('f',i), carrier)
            if i%iteration in frem:
                # Knit F
                k.knit('-', ('f',i), carrier)
            if i%iteration in r2rem:
                # Knit 1x1 Rib
                if i%2:
                    k.knit('-', ('b',i), carrier)
                else:
                    k.knit('-', ('f',i), carrier)
            if i%iteration in brem:
                # Knit B
                k.knit('-', ('b',i), carrier)
        

k.outhook(carrier)
for i in range(0, width):
    # Since ribbing is on both beds, drop f and b!
    k.drop('f', i)
    k.drop('b', i)
k.write('alec-variable-rib-test-r1-'+str(r1)+'-f-'+str(b)+'-r2-'+str(r2)+'-b-'+str(f)+'-dim:-'+str(width)+'x'+str(height)+'.k')