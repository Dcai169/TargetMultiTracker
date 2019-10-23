import numpy as np

# Color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
YELLOW = (0, 255, 255)
AQUA = (255, 255, 0)
FUCHSIA = (255, 0, 255)

# Different for each resolution
# Don't Forget!
RETICLE = (int(640/2), int(480/2))

# Points of the hitbox relative to the center of the hatch
HITBOX = np.array([(1.0, 4.0, 0.0),
                   (1.0, -4.0, 0.0),
                   (-1.0, 4.0, 0.0),
                   (-1.0, -4.0, 0.0)])

# The Northernmost and Southernmost points relative to the center of the hatch
TARGET = np.array([(5.9365, 12.5, 0.0),
                   (5.375, 6.675, 0.0),
                   (-5.9365, 12.5, 0.0),
                   (-5.375, 6.675, 0.0)])
