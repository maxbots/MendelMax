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

z_rod_diameter = 8
y_rod_diameter = 8
#how far apart should the bolt holes be?
hole_spacing_wide = 30
#how thick should the non-flange parts be?
thick_typical = 4.25
#how thick should the plastic under the bolt be?
thick_compress = 3

from MendelMax import *

#TODO: copies of this part for both rod sizes during final print
rod_diameter = z_rod_diameter

#how big are the bolts?
#TODO: replace with use of bolt module after it's written
bolt_hole_diameter = 5.5
bolt_head_diameter = 8.5

latch_width = bolt_head_diameter + thick_typical*2

#bounding box for the main curved part of the latch
box = Part.makeBox(hole_spacing_wide,latch_width,z_rod_diameter/2+thick_typical)
box.translate(Base.Vector(latch_width/2,0,0))

#main curved part of the latch, around the rod
cylinder = Part.makeCylinder(z_rod_diameter/2+thick_typical,latch_width)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
cylinder.translate(Base.Vector(latch_width/2+hole_spacing_wide/2,0,0))
latch = box.common(cylinder)

#connects the curved part to the bolt holes
box = Part.makeBox(hole_spacing_wide,latch_width,max(thick_typical,thick_compress))
box.translate(Base.Vector(latch_width/2,0,0))
latch = latch.fuse(box)

#rod hole
cylinder = Part.makeCylinder(z_rod_diameter/2,latch_width)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
cylinder.translate(Base.Vector(latch_width/2+hole_spacing_wide/2,0,0))
latch = latch.cut(cylinder)

#housings for the bolt holes
cylinder = Part.makeCylinder(latch_width/2,thick_typical)
cylinder.translate(Base.Vector(latch_width/2,latch_width/2,0))
latch = latch.fuse(cylinder)
cylinder = Part.makeCylinder(latch_width/2,thick_typical)
cylinder.translate(Base.Vector(latch_width/2+hole_spacing_wide,latch_width/2,0))
latch = latch.fuse(cylinder)

#bolt holes
cylinder = Part.makeCylinder(bolt_hole_diameter/2,z_rod_diameter/2+thick_typical)
cylinder.translate(Base.Vector(latch_width/2,latch_width/2,0))
latch = latch.cut(cylinder)
cylinder = Part.makeCylinder(bolt_head_diameter/2,z_rod_diameter/2+thick_typical)
cylinder.translate(Base.Vector(latch_width/2,latch_width/2,thick_compress))
latch = latch.cut(cylinder)
cylinder = Part.makeCylinder(bolt_hole_diameter/2,z_rod_diameter/2+thick_typical)
cylinder.translate(Base.Vector(latch_width/2+hole_spacing_wide,latch_width/2,0))
latch = latch.cut(cylinder)
cylinder = Part.makeCylinder(bolt_head_diameter/2,z_rod_diameter/2+thick_typical)
cylinder.translate(Base.Vector(latch_width/2+hole_spacing_wide,latch_width/2,thick_compress))
latch = latch.cut(cylinder)

Part.show(latch)