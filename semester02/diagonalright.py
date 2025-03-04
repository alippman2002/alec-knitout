# Setup
import sys
sys.path.append("/Users/aleclippman/Desktop/Knit/additionalresources")
sys.path.append('/Users/aleclippman/Desktop/Knit/knitout-frontend-py')
from hereadWrappers import *
import knitout

k = knitout.Writer('1 2 3 4 5 6')
# Half-pitch
k.rack(0.5)

### Same issues as before

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
# Create list of out iteration to check for remainders for patterning fold! 
r1rem = []
for i in range(0, r1):
    r1rem.append(i)
frem = []
for i in range(r1, r1+f):
    frem.append(i)
r2rem = []
for i in range(r1+b, r1+f+r2):
    r2rem.append(i)
brem = []
for i in range(r1+b+r2, r1+f+r2+f):
    brem.append(i)

# Can be arbitrary
height = 80

stitch_location = {}

for i in range(width - 1, 0, -2):
    bed = 'f'
    if i%2:
        bed = 'b'
    # This pass tucks along the back bed 
    stitch_location[i % iteration] = bed
    k.tuck('-', (bed,i), carrier)

k.releasehook(carrier)

for i in range(0, width, 2):
    bed = 'f'
    if i%2:
        bed = 'b'
    # This pass tucks along the front bed
    stitch_location[i % iteration] = bed
    k.tuck('+', (bed,i), carrier)

# WRITE TRANSFER INSTRUCTIONS BASED ON REMAINDER OF (r,b,r2,f)

# FROM ORIGINAL CAST ON:
    # i%2=0 was cast onto F
    # i%2= 1 was cast onto B

# Transfer based on specific portions of iteration!
for i in range(width - 1, -1, -1):
    if i%iteration in r1rem:
        # No transfers needed as cast on sets up 1x1 rib
        continue
    if i%iteration in frem:
        # Transfer to f bed if i%2 = 1
        if i%2:
            k.xfer(('b',i), ('f',i))
            stitch_location[i % iteration] = 'f'
    if i%iteration in r2rem:
        # No transfers needed as cast on sets up 1x1 rib
        continue
    if i%iteration in brem:
        # Transfer to b if i%2 = 0
        if not i%2:
            k.xfer(('f',i), ('b',i))
            stitch_location[i % iteration] = 'b'

### Debugging, chaning i%2 to shifted, so pattern tracks shifted pattern for transferring.
### THINK MORE ABOUT HOW TO MOVE PATTERN OVER AND CHECK WHERE NEEDLES NEED TO BE!!!!
### ORIGINAL PATTERN
# R1 - starts F at i%0 == 0 / not i%0 and ends at B i%0 == 1 / i%0
# R2 - starts at B with opposite logic
#### 
### SHIFTING PATTERN, i want to move over by j to check what part of teh pattern i am in, but still use the i place to see what needle i am
#### --> 

### NEW IDEA
    # store previous locations of BED AND COMPARE TO WHERE NEEDLE SHOULD BE BASED on from dictionary of iterating through first setup list
# Knit
for j in range(0, height):
    # - Pass
    print(f"J pass {j}")
    if j%2 == 0:
         print("- Pass!")
         for i in range(width - 1, -1, -1):
            shifted = (i+j) % iteration
            if shifted in r1rem:
                # Knit 1x1 Rib
                if shifted%2:
                    if stitch_location[(i-j) % iteration] != 'b':  
                        k.xfer(('f', i), ('b', i))
                    k.knit('-', ('b',i), carrier)
                    stitch_location[i % iteration] = 'b'
                else:
                    if stitch_location[(i-j) % iteration] != 'f':
                        k.xfer(('b', i), ('f', i))
                    k.knit('-', ('f',i), carrier)
                    stitch_location[i % iteration] = 'f'
            if shifted in frem:
                if stitch_location[(i-j) % iteration] != 'f':
                    k.xfer(('b', i), ('f', i))
                # Knit F
                k.knit('-', ('f',i), carrier)
                stitch_location[i % iteration] = 'f'
            if shifted in r2rem:
                # Knit 1x1 Rib
                if shifted%2:
                    if stitch_location[(i-j) % iteration] != 'b':
                        k.xfer(('f', i), ('b', i))
                    k.knit('-', ('b',i), carrier)
                    stitch_location[i%iteration] = 'b'
                else:
                    if stitch_location[(i-j) % iteration] != 'f':
                        k.xfer(('b', i), ('f', i))
                    k.knit('-', ('f',i), carrier)
                    stitch_location[i%iteration] = 'f'
            if shifted in brem:
                # Knit B
                if stitch_location[(i-j) % iteration] != 'b':
                    k.xfer(('f', i), ('b', i))
                k.knit('-', ('b',i), carrier)
                stitch_location[i % iteration] = 'b'
    # + Pass
    ### I=2 needs to transfer f to b and knit b
    else:
       print("+ Pass")
       for i in range(0, width, 1):
            print("I")
            print(i)
            print("shifted")
            shifted = (i+j) % iteration
            print(shifted)
            if shifted in r1rem:
                # Knit 1x1 Rib
                if shifted%2:
                    if stitch_location[(i-j) % iteration] != 'b':  
                        k.xfer(('f', i), ('b', i))
                    k.knit('+', ('b',i), carrier)
                    stitch_location[i % iteration] = 'b'
                else:
                    if stitch_location[(i-j) % iteration] != 'f':  
                        k.xfer(('b', i), ('f', i))
                    k.knit('+', ('f',i), carrier)
                    stitch_location[i%iteration] = 'f'
            if shifted in frem:
                # Knit F
                if stitch_location[(i-j) %iteration] != 'f':  
                        k.xfer(('b', i), ('f', i))
                k.knit('+', ('f',i), carrier)
                stitch_location[i%iteration] = 'f'
            if shifted in r2rem:
                # Knit 1x1 Rib
                if shifted%2:
                    if stitch_location[(i-j) %iteration] != 'b':  
                        k.xfer(('f', i), ('b', i))
                    k.knit('+', ('b',i), carrier)
                    stitch_location[i%iteration] = 'b'
                else:
                    if stitch_location[(i-j) %iteration] != 'f':  
                        k.xfer(('b', i), ('f', i))
                    k.knit('+', ('f',i), carrier)
                    stitch_location[i%iteration] = 'f'
            if shifted in brem:
                if stitch_location[(i-j) %iteration] != 'b':  
                        k.xfer(('f', i), ('b', i))
                # Knit B
                k.knit('+', ('b',i), carrier)
                stitch_location[i%iteration] = 'b'

k.outhook(carrier)
for i in range(0, width):
    # Since ribbing is on both beds, drop f and b!
    k.drop('f', i)
    k.drop('b', i)
k.write('alecdiagonal-variable-rib-test-r1-'+str(r1)+'-f-'+str(b)+'-r2-'+str(r2)+'-b-'+str(f)+'-dim:-'+str(width)+'x'+str(height)+'.k')