"""
Creates a figure demonstrating how the algorithm finds periodic cycles. 
"""

from svgfig import *
from math import sqrt, cos, sin, pi

# Create triangle and circle.
c = Ellipse(0, 0, 1, 0, 1)
l1 = Line(2, 0, -1, sqrt(3))
l2 = Line(-1, sqrt(3), -1, -sqrt(3))
l3 = Line(-1, -sqrt(3), 2, 0)

# Wedge A->B, A->C.
arc = Curve("cos(t), sin(t)", 0, pi/3, stroke="red")
l4 = Line(1, 0, -1, -sqrt(3))
l5 = Line(cos(pi/3), sin(pi/3), -1, -sqrt(3))


f = Fig(c, l1, l2, l3, arc, l4, l5)
f.SVG(window(-2,2,-2,2)).save('algorithm-desc.svg')

# Add points.
# d = [(0.963525, 0.267617), (-0.250000, -0.968246), (-0.713525, 0.700629)]
# d = Dots(d, width=1.5, height=1.5)

# # Add lines.
# l4 = Line(2, 0, 0.963525, 0.267617)
# l5 = Line(0.963525, 0.267617, -0.713525, 0.700629)
# l6 = Line(-1, sqrt(3), -0.713525, 0.700629)
# l7 = Line(-0.713525, 0.700629, -0.250000, -0.968246)
# l8 = Line(-1, -sqrt(3), -0.250000, -0.968246)
# l9 = Line(-0.250000, -0.968246, 0.963525, 0.267617)

# # Group and transform window.
# f = Fig(c, l1, l2, l3, l4, l5, l6, l7, l8, l9, d)
# f.SVG(window(-2,2,-2,2)).save('action-of-map.svg')

