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
# Create list of out iteration to check for remainders for patterning fold! 
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

stitch_locations = {}

for i in range(width - 1, 0, -2):
    bed = 'f'
    if i%2:
        bed = 'b'
    # This pass tucks along the back bed 
    stitch_locations[i] = bed
    k.tuck('-', (bed,i), carrier)

k.releasehook(carrier)

for i in range(0, width, 2):
    bed = 'f'
    if i%2:
        bed = 'b'
    # This pass tucks along the front bed
    stitch_locations[i] = bed
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
            stitch_locations[i] = 'f'
    if i%iteration in r2rem:
        # No transfers needed as cast on sets up 1x1 rib
        continue
    if i%iteration in brem:
        # Transfer to b if i%2 = 0
        if not i%2:
            k.xfer(('f',i), ('b',i))
            stitch_locations[i] = 'b'

stitch_location = {}
stitch_order = sorted(stitch_locations.keys())
for key in stitch_order:
    stitch_location[key] = stitch_locations[key]

print("Stitch Locations Inititally")
print(stitch_location)

print("bed_rules")
print(bed_rules)

# Knit
for j in range(0, height):
    print("J pass Number Below")
    print(j)
    # - Pass
    if j%2 == 0:
         print("- pass")
         for i in range(width - 1, -1, -1):
            print("i below (needle we at)")
            print(i)
            shifted = (i-j) % iteration
            if shifted in r1rem:
                print(" r1 rib, knitting")
                # Knit 1x1 ribd
                if bed_rules[shifted] != stitch_location[i]:  
                    print("trasnfer occured")
                    k.xfer((stitch_location[i], i), (bed_rules[shifted], i))
                print("just knit on the following bed!")
                print(bed_rules[shifted])
                k.knit('-', (bed_rules[shifted],i), carrier)
                stitch_location[i] = bed_rules[shifted]
            if shifted in frem:
                print('front knitting')
                if stitch_location[i] != 'f':
                    k.xfer(('b', i), ('f', i))
                # Knit F
                k.knit('-', ('f',i), carrier)
                stitch_location[i] = 'f'
            if shifted in r2rem:
                # Knit 1x1 Rib
                print(" r2 rib, knitting")
                if bed_rules[shifted] != stitch_location[i]:
                    print("transfer occured")
                    k.xfer((stitch_location[i], i), (bed_rules[shifted], i))
                k.knit('-', (bed_rules[shifted],i), carrier)
                print("just knit on the following bed!")
                print(bed_rules[shifted])
                stitch_location[i] = bed_rules[shifted]
            if shifted in brem:
                # Knit B
                print("back knitting")
                if stitch_location[i] != 'b':
                    print("transfer occured")
                    k.xfer(('f', i), ('b', i))
                k.knit('-', ('b',i), carrier)
                print("just knit on back bed!")
                stitch_location[i] = 'b'
            print("Updated Stitch Locations")
            print(stitch_location)
    # + Pass
    ### I=2 needs to transfer f to b and knit b
    else:
       print("+ Pass")
       for i in range(0, width, 1):
            print(f"i is here: {i}")
            shifted = (i-j) % iteration
            print(f"shifted value is here: {shifted}")
            if shifted in r1rem:
                print(" r1 rib, knitting")
                # Knit 1x1 rib
                if bed_rules[shifted] != stitch_location[i]:  
                    print("trasnfer occured")
                    k.xfer((stitch_location[i], i), (bed_rules[shifted], i))
                print("just knit on the following bed!")
                print(bed_rules[shifted])
                k.knit('+', (bed_rules[shifted],i), carrier)
                stitch_location[i] = bed_rules[shifted]
            if shifted in frem:
                print('front knitting')
                if stitch_location[i] != 'f':
                    k.xfer(('b', i), ('f', i))
                # Knit F
                k.knit('+', ('f',i), carrier)
                stitch_location[i] = 'f'
            if shifted in r2rem:
                # Knit 1x1 Rib
                print(" r2 rib, knitting")
                if bed_rules[shifted] != stitch_location[i]:
                    print("transfer occured")
                    k.xfer((stitch_location[i], i), (bed_rules[shifted], i))
                k.knit('+', (bed_rules[shifted],i), carrier)
                print("just knit on the following bed!")
                print(bed_rules[shifted])
                stitch_location[i] = bed_rules[shifted]
            if shifted in brem:
                # Knit B
                print("back knitting")
                if stitch_location[i] != 'b':
                    print("transfer occured")
                    k.xfer(('f', i), ('b', i))
                k.knit('+', ('b',i), carrier)
                print("just knit on back bed!")
                stitch_location[i] = 'b'
            print("Updated Stitch Locations")
            print(stitch_location)

k.outhook(carrier)
for i in range(0, width):
    # Since ribbing is on both beds, drop f and b!
    k.drop('f', i)
    k.drop('b', i)
k.write('alecdiagonalv2-variable-rib-test-r1-'+str(r1)+'-f-'+str(b)+'-r2-'+str(r2)+'-b-'+str(f)+'-dim:-'+str(width)+'x'+str(height)+'.k')