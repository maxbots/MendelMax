from __future__ import division # allows floating point division from integers
from FreeCAD import Base
import math
import sys
import os

try:
    path = os.path.join(os.path.dirname(__file__), '..', '..', 'include')
    i = sys.path.index(path)
except:
	sys.path.append(path)

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
#  <--extrusion_profile-->

extrusion_slot_opening_width = 6 #A
extrusion_slot_opening_depth = 2 #B
extrusion_slot_width = 11 #C
extrusion_slot_vertical_depth = 1 #D
extrusion_slot_depth = 4 #E
#F=C-(E-D) as long as the diagonals are 45 degrees

#minimum thickness
#TODO: enforce this everywhere, alert the user when it is violated
thick_min = 1

hole_spacing_medium = 20

from MendelMax import *

clip_thickness = 2

#clearance between printed part and metal surfaces
gap_horizontal = 0.25
gap_vertical = 0.1

clip_length_padding = 4
#TODO: use the bolt module once it's written
bolt_diameter = 4

#should the clip have "wings"?
flange_width = 20
#how many bolts/nuts does this part take?
num_holes = 2

base_padding = max(bolt_diameter/2+thick_min,clip_padding)
hole_span = max((num_holes-1),0) * hole_spacing_medium
clip_length = hole_span + base_padding*2
clip_width = extrusion_profile + clip_thickness*2 + gap_horizontal*2

clip_top = Part.makeBox(clip_length, clip_width + flange_width*2, clip_thickness)

clip_arm_height = extrusion_profile/2 + extrusion_slot_opening_width/2 - gap_vertical
clip_barb_width = extrusion_slot_opening_depth
clip_arm_cross_section = Part.makePolygon([
Base.Vector(0,0,0),
Base.Vector(0,0, -clip_arm_height),
Base.Vector(0, clip_thickness+clip_barb_width, -(extrusion_profile/2 - extrusion_slot_opening_width/2 + gap_vertical)),
Base.Vector(0, clip_thickness,                 -(extrusion_profile/2 - extrusion_slot_opening_width/2 + gap_vertical)),
Base.Vector(0, clip_thickness,0),
Base.Vector(0,0,0)])
face = Part.Face(clip_arm_cross_section)
clip_arm = face.extrude(Base.Vector(clip_length,0,0))
clip_arm.translate(Base.Vector(0,flange_width,0))
clip = clip_top.fuse(clip_arm)
clip_arm.rotate(Base.Vector(clip_length/2,(clip_width+flange_width*2)/2,0),Base.Vector(0,0,1),180)
clip = clip.fuse(clip_arm)

hole = Part.makeCylinder(bolt_diameter/2,clip_thickness)
hole.translate(Base.Vector(base_padding,(clip_width+flange_width*2)/2,0))
for n in range(num_holes):
    clip = clip.cut(hole)
    if(flange_width):
        hole.translate(Base.Vector(0,clip_width/2+flange_width/2,0))
        clip = clip.cut(hole)
        hole.translate(Base.Vector(0,-(clip_width+flange_width),0))
        clip = clip.cut(hole)
        hole.translate(Base.Vector(0,clip_width/2+flange_width/2,0))
    hole.translate(Base.Vector(hole_spacing_medium,0,0))

clip.translate(Base.Vector(0,0,-clip_thickness))
clip.rotate(Base.Vector(clip_length/2,0,0),Base.Vector(0,1,0),180)

Part.show(clip)
