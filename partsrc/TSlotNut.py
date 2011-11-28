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
extrusion_slot_width = 12
extrusion_slot_depth = 4
extrusion_slot_opening_width = 6
bolt_diameter = 4
metal_nut_width = 7.5
min_padding = 1
spacing = 20

num_holes = 2

base_padding = max(min_padding,max(bolt_diameter+1,metal_nut_width * (2/math.sqrt(3))+1))
nut_simple_length = (num_holes-1) * spacing
nut_length = nut_simple_length + base_padding

nut_top = Part.makeBox(nut_length, extrusion_slot_opening_width - 1, 1.75)


nut_bottom_width = extrusion_slot_width - 1
nut_bottom_height = max(extrusion_slot_depth/2,min(extrusion_slot_depth,1))
nut_bottom_cross_section = Part.makePolygon([Base.Vector(0,0,0),Base.Vector(0,nut_bottom_width,0),Base.Vector(0,nut_bottom_width - nut_bottom_height,-nut_bottom_height),Base.Vector(0,nut_bottom_height,-nut_bottom_height),Base.Vector(0,0,0)])
face = Part.Face(nut_bottom_cross_section)
nut_bottom = face.extrude(Base.Vector(nut_length,0,0))
nut_bottom.translate(Base.Vector(0,-(nut_bottom_width-(extrusion_slot_opening_width - 1))/2,0))
nut = nut_bottom.fuse(nut_top)

bolthole = Part.makeCylinder(bolt_diameter/2,1.75)
nuthole = regPolygon(sides = 6, radius = metal_nut_width/2, extrude = nut_bottom_height, Z_offset = -nut_bottom_height)
holes = bolthole.fuse(nuthole)
holes.translate(Base.Vector(base_padding/2,(extrusion_slot_opening_width-1)/2,0))
for n in range(num_holes):
    nut = nut.cut(holes)
    holes.translate(Base.Vector(spacing,0,0))

#bring back into octant 1
nut.translate(Base.Vector(0,nut_bottom_height,nut_bottom_height))

Part.show(nut)
