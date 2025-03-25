### CODE FROM RECTANGLE RIB FUNCTION IN KNITOUT.PY

import sys
sys.path.append("/Users/aleclippman/Desktop/Knit/additionalresources")
sys.path.append('/Users/aleclippman/Desktop/Knit/knitout-frontend-py')
from hereadWrappers import *
import knitout

width = 10
height = 20

writer = knitout.Writer('1 2 3 4')
writer.addHeader('Machine', 'swg')
carrier = '1'
writer.inhook(carrier)
for i in range(width-1, 0, -2):
    bed = 'f'
    if i%2:
        bed = 'b'
    writer.tuck('-', (bed,i), carrier)

writer.releasehook(carrier)

for i in range(0, width, 2):
    bed = 'f'
    if i%2:
        bed = 'b'

    writer.tuck('+', (bed, i), carrier)
for j in range(0, height):
    if j%2 == 0:
        for i in range(width, 0,-1):
            bed = 'f'
            if (i-1)%2:
                bed = 'b'
            writer.knit('-', (bed, i-1), carrier)
    else:
        for i in range(0, width):
            bed = 'f'
            if i%2:
                bed = 'b'
            writer.knit('+', (bed, i), carrier)

writer.outhook(carrier)
for i in range(0, width):
    writer.drop(('f', i))
    writer.drop(('b', i))

writer.write('rib-'+str(width)+'x'+str(height)+'.k')
