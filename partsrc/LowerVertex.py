from __future__ import division # allows floating point division from integers
from FreeCAD import Base
from math import *
import sys
import os

try:
    path = os.path.join(os.path.dirname(__file__), '..', 'include')
    i = sys.path.index(path)
except:
    sys.path.append(path)

extrusion_profile = 20
#how far apart should the bottom frame rectangles be?
frame_rectangle_spacing = 30
#how far apart should bolt holes into the same extrusion be?
hole_spacing_medium = 20
#how thick should the non-flange parts be?
thick_typical = 4.25

from MendelMax import *

#how big are the structural bolts?
#TODO: replace with use of bolt module after it's written
bolt_hole_diameter = 5.5

box = Part.makeBox(extrusion_profile*2+frame_rectangle_spacing+thick_typical,extrusion_profile*2,thick_typical)
box.translate(Base.Vector(-thick_typical,0,0))
vertex = box

#reinforce the base rectangle plate to the diagonal plate
filler_cross_section = Part.makePolygon([
Base.Vector(0,0,0),
Base.Vector(0,-(extrusion_profile*sqrt(3)-thick_typical)/sqrt(3),0),
Base.Vector(-(extrusion_profile*sqrt(3)-thick_typical),0,0),
Base.Vector(0,0,0),
])
filler_face = Part.Face(filler_cross_section)
filler = filler_face.extrude(Base.Vector(0,0,thick_typical))
filler.translate(Base.Vector(-thick_typical,extrusion_profile*2,0))
vertex = vertex.fuse(filler)

#TODO: cleaner calculation of length of this part to reduce trimming
box = Part.makeBox(extrusion_profile+hole_spacing_medium+40,extrusion_profile,thick_typical)
cylinder = Part.makeCylinder(bolt_hole_diameter/2,thick_typical)
cylinder.translate(Base.Vector(extrusion_profile/2,extrusion_profile/2,0))
box = box.cut(cylinder)
cylinder.translate(Base.Vector(hole_spacing_medium,0,0))
box = box.cut(cylinder)
box.translate(Base.Vector(-(extrusion_profile+hole_spacing_medium+15),0,0))
box.rotate(Base.Vector(0,extrusion_profile,0),Base.Vector(0,0,1),-30)
vertex = vertex.fuse(box)
#TODO: reduce or eliminate this trimming
box = Part.makeBox(40,10,extrusion_profile)
box.translate(Base.Vector(-thick_typical-5,-10,0))
vertex = vertex.cut(box)

cylinder = Part.makeCylinder(bolt_hole_diameter/2,thick_typical)
cylinder.translate(Base.Vector(extrusion_profile/2,extrusion_profile/2,0))
vertex = vertex.cut(cylinder)
cylinder.translate(Base.Vector(0,extrusion_profile,0))
vertex = vertex.cut(cylinder)
cylinder.translate(Base.Vector(frame_rectangle_spacing+extrusion_profile,0,0))
vertex = vertex.cut(cylinder)
cylinder.translate(Base.Vector(0,-extrusion_profile,0))
vertex = vertex.cut(cylinder)

Part.show(vertex)
