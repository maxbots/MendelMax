from __future__ import division # allows floating point division from integers
from FreeCAD import Base
import sys
from math import *

extrusion_width = 20
#how far apart should the bottom frame rectangles be?
frame_rectangle_spacing = 30
#how far apart should bolt holes into the same extrusion be?
hole_spacing = 20

# import MendelMax.py settings here

#how thick should the non-flange parts be?
part_thickness = 5
#how big are the structural bolts?
bolt_hole_diameter = 5.5

box = Part.makeBox(extrusion_width*2+frame_rectangle_spacing+part_thickness,extrusion_width*2,part_thickness)
box.translate(Base.Vector(-part_thickness,0,0))
vertex = box

#reinforce the base rectangle plate to the diagonal plate
filler_cross_section = Part.makePolygon([
Base.Vector(0,0,0),
Base.Vector(0,-(extrusion_width*sqrt(3)-part_thickness)/sqrt(3),0),
Base.Vector(-(extrusion_width*sqrt(3)-part_thickness),0,0),
Base.Vector(0,0,0),
])
filler_face = Part.Face(filler_cross_section)
filler = filler_face.extrude(Base.Vector(0,0,part_thickness))
filler.translate(Base.Vector(-part_thickness,extrusion_width*2,0))
vertex = vertex.fuse(filler)

#TODO: cleaner calculation of length of this part to reduce trimming
box = Part.makeBox(extrusion_width+hole_spacing+40,extrusion_width,part_thickness)
cylinder = Part.makeCylinder(bolt_hole_diameter/2,part_thickness)
cylinder.translate(Base.Vector(extrusion_width/2,extrusion_width/2,0))
box = box.cut(cylinder)
cylinder.translate(Base.Vector(hole_spacing,0,0))
box = box.cut(cylinder)
box.translate(Base.Vector(-(extrusion_width+hole_spacing+15),0,0))
box.rotate(Base.Vector(0,extrusion_width,0),Base.Vector(0,0,1),-30)
vertex = vertex.fuse(box)
#TODO: reduce or eliminate this trimming
box = Part.makeBox(40,10,extrusion_width)
box.translate(Base.Vector(-part_thickness-5,-10,0))
vertex = vertex.cut(box)

cylinder = Part.makeCylinder(bolt_hole_diameter/2,part_thickness)
cylinder.translate(Base.Vector(extrusion_width/2,extrusion_width/2,0))
vertex = vertex.cut(cylinder)
cylinder.translate(Base.Vector(0,extrusion_width,0))
vertex = vertex.cut(cylinder)
cylinder.translate(Base.Vector(frame_rectangle_spacing+extrusion_width,0,0))
vertex = vertex.cut(cylinder)
cylinder.translate(Base.Vector(0,-extrusion_width,0))
vertex = vertex.cut(cylinder)

Part.show(vertex)
