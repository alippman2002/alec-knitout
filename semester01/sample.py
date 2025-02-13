
import knitout 
# Resolve module not found error

# Start files with a k object and that will write the knitout commands
k = knitout.Writer('1 2 3 4 5 6')
k
# Bring in carrier
k.incarrier('1')

# Add knit operations
k.knit('+', 'f10', 'b')

# Bring out carrier
k.outcarrier('1')

# Write file
k.write('out.k')

# Input image
# translate crease lines into 2D array encoding positions of folds based on lines
# Identify best knit operations to create the kind of fold based on type of line?
# Based on desired swatch length spread out commands proportionately



