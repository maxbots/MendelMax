from __future__ import division # allows floating point division from integers
import FreeCAD, Part, math
from FreeCAD import Base

def RodLatch(
rod_diameter = 8, 
#how far apart should the bolt holes be?
hole_spacing = 30, 
#how thick should the non-flange parts be?
thick_typical = 4.25, 
#how thick should the plastic under the bolt be?
thick_compress = 3
):

    #how big are the bolts?
    #TODO: replace with use of bolt module after it's written
    bolt_hole_diameter = 5.5
    bolt_head_diameter = 8.5

    latch_width = bolt_head_diameter + thick_typical*2

    #bounding box for the main curved part of the latch
    box = Part.makeBox(hole_spacing,latch_width,rod_diameter/2+thick_typical)
    box.translate(Base.Vector(latch_width/2,0,0))

    #main curved part of the latch, around the rod
    cylinder = Part.makeCylinder(rod_diameter/2+thick_typical,latch_width)
    cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
    cylinder.translate(Base.Vector(latch_width/2+hole_spacing/2,0,0))
    latch = box.common(cylinder)

    #connects the curved part to the bolt holes
    box = Part.makeBox(hole_spacing,latch_width,max(thick_typical,thick_compress))
    box.translate(Base.Vector(latch_width/2,0,0))
    latch = latch.fuse(box)

    #housings for the bolt holes
    cylinder = Part.makeCylinder(latch_width/2,thick_typical)
    cylinder.translate(Base.Vector(latch_width/2,latch_width/2,0))
    latch = latch.fuse(cylinder)
    cylinder = Part.makeCylinder(latch_width/2,thick_typical)
    cylinder.translate(Base.Vector(latch_width/2+hole_spacing,latch_width/2,0))
    latch = latch.fuse(cylinder)

    #bolt holes
    cylinder = Part.makeCylinder(bolt_hole_diameter/2,rod_diameter/2+thick_typical)
    cylinder.translate(Base.Vector(latch_width/2,latch_width/2,0))
    latch = latch.cut(cylinder)
    cylinder = Part.makeCylinder(bolt_head_diameter/2,rod_diameter/2+thick_typical)
    cylinder.translate(Base.Vector(latch_width/2,latch_width/2,thick_compress))
    latch = latch.cut(cylinder)
    cylinder = Part.makeCylinder(bolt_hole_diameter/2,rod_diameter/2+thick_typical)
    cylinder.translate(Base.Vector(latch_width/2+hole_spacing,latch_width/2,0))
    latch = latch.cut(cylinder)
    cylinder = Part.makeCylinder(bolt_head_diameter/2,rod_diameter/2+thick_typical)
    cylinder.translate(Base.Vector(latch_width/2+hole_spacing,latch_width/2,thick_compress))
    latch = latch.cut(cylinder)

    #rod hole
    cylinder = Part.makeCylinder(rod_diameter/2,latch_width)
    cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
    cylinder.translate(Base.Vector(latch_width/2+hole_spacing/2,0,0))
    latch = latch.cut(cylinder)
    
    return latch

if __name__ == "__main__":
    Part.show(RodLatch())
