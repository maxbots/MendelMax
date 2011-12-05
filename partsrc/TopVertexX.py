from __future__ import division # allows floating point division from integers
from FreeCAD import Base
import math
import sys
import os

try:
    path = os.path.join(os.path.dirname(__file__), '..', 'include')
    i = sys.path.index(path)
except:
    sys.path.append(path)

extrusion_profile = 20
small_printer = True
# how thick should the part be?
thick_typical = 4
# how far apart should the holes be?
hole_spacing_medium = 20
# how much wider than the spacing should the plates be?

from MendelMax import *

bolt_hole_diameter = 5.5
# how much wider than the bolt spacing should the plates attached to the extrusion be?
plate_padding = extrusion_profile/2
# how far should the plates be from the extrusion corner?
corner_offset = 60
# how wide should the strut be?
diagonal_width = 17

# shrink the part, least important dimensions first
if(small_printer):
    if(corner_offset+hole_spacing_medium+plate_padding*2>100):
        plate_padding = max(bolt_hole_diameter/2+thick_min,(100-(corner_offset+hole_spacing_medium))/2)
        hole_spacing_medium = 100-(corner_offset+plate_padding*2)
        #need logic to reduce the number of holes if they overlap
        diagonal_width = min(diagonal_width,(hole_spacing_medium+plate_padding*2)/math.sqrt(2))
        #TODO: alert the user if the part is still too big

shape = Part.makePolygon([
Base.Vector(corner_offset,0,0),
Base.Vector(corner_offset+hole_spacing_medium+plate_padding*2,0,0),
Base.Vector(corner_offset+hole_spacing_medium+plate_padding*2,extrusion_profile,0),
Base.Vector(corner_offset+(hole_spacing_medium+plate_padding*2)/2+diagonal_width/2*math.sqrt(2),extrusion_profile,0),
Base.Vector(extrusion_profile,corner_offset+(hole_spacing_medium+plate_padding*2)/2+diagonal_width/2*math.sqrt(2),0),
Base.Vector(extrusion_profile,corner_offset+hole_spacing_medium+plate_padding*2,0),
Base.Vector(0,corner_offset+hole_spacing_medium+plate_padding*2,0),
Base.Vector(0,corner_offset,0),
Base.Vector(extrusion_profile,corner_offset,0),
Base.Vector(extrusion_profile,corner_offset+(hole_spacing_medium+plate_padding*2)/2-diagonal_width/2*math.sqrt(2),0),
Base.Vector(corner_offset+(hole_spacing_medium+plate_padding*2)/2-diagonal_width/2*math.sqrt(2),extrusion_profile,0),
Base.Vector(corner_offset,extrusion_profile,0),
Base.Vector(corner_offset,0,0),
])
face = Part.Face(shape)
vertex = face.extrude(Base.Vector(0,0,thick_typical))

cylinder = Part.makeCylinder(bolt_hole_diameter/2,thick_typical)
cylinder.translate(Base.Vector(corner_offset+plate_padding,extrusion_profile/2,0))
vertex = vertex.cut(cylinder)
cylinder.translate(Base.Vector(hole_spacing_medium,0,0))
vertex = vertex.cut(cylinder)
cylinder.rotate(Base.Vector(0,0,thick_typical/2),Base.Vector(1,1,0),180)
vertex = vertex.cut(cylinder)
cylinder.translate(Base.Vector(0,-hole_spacing_medium,0))
vertex = vertex.cut(cylinder)

Part.show(vertex)