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

z_rod_diameter = 8
#how far apart should the bolt holes be?
bolt_hole_spacing = 26
#how thick should the non-flange parts be?
latch_thickness = 7
#how thick should the plastic under the bolt be?
bolt_flange_thickness = 3
#how big are the bolts?
#TODO: add logic to specify bolt type instead of bolt dimensions
bolt_hole_diameter = 5.5
bolt_head_diameter = 8.5

#TODO: import MendelMax.py settings here

#bounding box for the main curved part of the latch
box = Part.makeBox(bolt_hole_spacing,14,z_rod_diameter/2+latch_thickness)
box.translate(Base.Vector(7,0,0))

#main curved part of the latch, around the rod
cylinder = Part.makeCylinder(z_rod_diameter/2+latch_thickness,14)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
cylinder.translate(Base.Vector(7+bolt_hole_spacing/2,0,0))
latch = box.common(cylinder)

#connects the curved part to the bolt holes
box = Part.makeBox(bolt_hole_spacing,14,max(latch_thickness,bolt_flange_thickness))
box.translate(Base.Vector(7,0,0))
latch = latch.fuse(box)

#rod hole
cylinder = Part.makeCylinder(z_rod_diameter/2,14)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
cylinder.translate(Base.Vector(7+bolt_hole_spacing/2,0,0))
latch = latch.cut(cylinder)

#housings for the bolt holes
cylinder = Part.makeCylinder(7,latch_thickness)
cylinder.translate(Base.Vector(7,7,0))
latch = latch.fuse(cylinder)
cylinder = Part.makeCylinder(7,latch_thickness)
cylinder.translate(Base.Vector(7+bolt_hole_spacing,7,0))
latch = latch.fuse(cylinder)

#bolt holes
cylinder = Part.makeCylinder(bolt_hole_diameter/2,z_rod_diameter/2+latch_thickness)
cylinder.translate(Base.Vector(7,7,0))
latch = latch.cut(cylinder)
cylinder = Part.makeCylinder(bolt_head_diameter/2,z_rod_diameter/2+latch_thickness)
cylinder.translate(Base.Vector(7,7,bolt_flange_thickness))
latch = latch.cut(cylinder)
cylinder = Part.makeCylinder(bolt_hole_diameter/2,z_rod_diameter/2+latch_thickness)
cylinder.translate(Base.Vector(7+bolt_hole_spacing,7,0))
latch = latch.cut(cylinder)
cylinder = Part.makeCylinder(bolt_head_diameter/2,z_rod_diameter/2+latch_thickness)
cylinder.translate(Base.Vector(7+bolt_hole_spacing,7,bolt_flange_thickness))
latch = latch.cut(cylinder)

Part.show(latch)