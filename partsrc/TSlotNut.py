from __future__ import division # allows floating point division from integers
from FreeCAD import Base
import sys
import math
import os

try:
    path = os.path.join(os.path.dirname(__file__), '..', 'include')
    i = sys.path.index(path)
except:
	sys.path.append(path)

from RegularPolygon import regPolygon

# all measurements in mm

# .-------.       .-------. -
# |       | <-A-> |       |   B
# | .-----         -----. | -    -    
# | |       <-C->       | | _ D  ^
# |  \                 /  |      |
# |   \               /   |      E
# |    \             /    |      v
# |     ----<-F->----     |      -
#

extrusion_slot_opening_width = 6 #A
extrusion_slot_opening_depth = 2 #B
extrusion_slot_width = 11 #C
extrusion_slot_vertical_depth = 1 #D
extrusion_slot_depth = 4 #E
#F=C-(E-D) as long as the diagonals are 45 degrees

bolt_diameter = 4
metal_nut_width = 8

min_padding = 1
hole_spacing = 20

#clearance between printed part and metal surfaces
gap_horizontal = 0.25
gap_vertical = 0.1

num_holes = 2

base_padding = max(bolt_diameter/2,metal_nut_width * (1/math.sqrt(3)))+min_padding
hole_span = (num_holes-1) * hole_spacing
nut_length = hole_span + base_padding*2

nut_top = Part.makeBox(nut_length, extrusion_slot_opening_width - gap_horizontal*2, extrusion_slot_opening_depth - gap_vertical)

nut_bottom_width = extrusion_slot_width - gap_horizontal*2
nut_bottom_height = extrusion_slot_depth - gap_vertical
nut_bottom_cross_section = Part.makePolygon([
Base.Vector(0,0,0),
Base.Vector(0,nut_bottom_width,0),
Base.Vector(0,nut_bottom_width,-(extrusion_slot_vertical_depth-gap_vertical)),
Base.Vector(0,nut_bottom_width - (nut_bottom_height-(extrusion_slot_vertical_depth-gap_vertical)),-nut_bottom_height),
Base.Vector(0,nut_bottom_height-(extrusion_slot_vertical_depth-gap_vertical),-nut_bottom_height),
Base.Vector(0,0,-(extrusion_slot_vertical_depth-gap_vertical)),
Base.Vector(0,0,0)])
face = Part.Face(nut_bottom_cross_section)
nut_bottom = face.extrude(Base.Vector(nut_length,0,0))
nut_bottom.translate(Base.Vector(0,-(nut_bottom_width-(extrusion_slot_opening_width - 0.5))/2,0))
nut = nut_bottom.fuse(nut_top)

bolthole = Part.makeCylinder(bolt_diameter/2,extrusion_slot_opening_depth - gap_vertical)
nuthole = regPolygon(sides = 6, radius = metal_nut_width/2, extrude = nut_bottom_height, Z_offset = -nut_bottom_height)
holes = bolthole.fuse(nuthole)
holes.translate(Base.Vector(base_padding,(extrusion_slot_opening_width-gap_horizontal*2)/2,0))
for n in range(num_holes):
    nut = nut.cut(holes)
    holes.translate(Base.Vector(hole_spacing,0,0))

#bring back into octant 1
nut.translate(Base.Vector(0,(nut_bottom_width - (extrusion_slot_opening_width - gap_horizontal*2))/2,nut_bottom_height))

Part.show(nut)
