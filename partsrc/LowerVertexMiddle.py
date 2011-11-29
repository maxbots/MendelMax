from __future__ import division # allows floating point division from integers
from FreeCAD import Base
import sys
from math import *

extrusion_width = 20
#how far apart should the bottom frame rectangles be?
frame_rectangle_spacing = 30

# import MendelMax.py settings here

#how thick should the non-flange parts be?
part_thickness = 5
#how big are the structural bolts?
bolt_hole_diameter = 5.5
bolt_head_diameter = 10

#should there be a visible hole for easy access to the "hidden" bolt?
accessible_hole = 1
#should we draw the extrusions?
render_extrusions = 0

#this block of code draws the extrusions as a separate Shape, for comparison purposes
if(render_extrusions):
    #y extrusion
    box = Part.makeBox(extrusion_width,80,extrusion_width)
    box.translate(Base.Vector(0,extrusion_width,0))
    extrusions = box
    #y extrusion
    box = Part.makeBox(extrusion_width,80,extrusion_width)
    box.translate(Base.Vector(0,extrusion_width,0))
    box.translate(Base.Vector(frame_rectangle_spacing+extrusion_width,0,0))
    extrusions = extrusions.fuse(box)
    #x extrusion
    box = Part.makeBox(extrusion_width,extrusion_width,80)
    extrusions = extrusions.fuse(box)
    #x extrusion
    box = Part.makeBox(extrusion_width,extrusion_width,80)
    box.translate(Base.Vector(frame_rectangle_spacing+extrusion_width,0,0))
    extrusions = extrusions.fuse(box)
    #diagonal extrusion
    box = Part.makeBox(80,extrusion_width,extrusion_width)
    box.translate(Base.Vector(-95,0,0))
    box.rotate(Base.Vector(0,extrusion_width,0),Base.Vector(0,0,1),-30)
    extrusions = extrusions.fuse(box)
    
    Part.show(extrusions)

#connect the two X extrusions
box = Part.makeBox(frame_rectangle_spacing+extrusion_width*2,part_thickness,extrusion_width)
box.translate(Base.Vector(0,-part_thickness,0))
vertex = box
cylinder = Part.makeCylinder(bolt_hole_diameter/2,part_thickness)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
cylinder.translate(Base.Vector(extrusion_width/2,0,extrusion_width/2))
vertex = vertex.cut(cylinder)
cylinder.translate(Base.Vector(frame_rectangle_spacing+extrusion_width,0,0))
vertex = vertex.cut(cylinder)

#mount to the top of the top Y extrusion
box = Part.makeBox(part_thickness,40+extrusion_width,extrusion_width)
box.translate(Base.Vector(-part_thickness,-part_thickness,0))
vertex = vertex.fuse(box)
cylinder = Part.makeCylinder(bolt_hole_diameter/2,part_thickness)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),-90)
cylinder.translate(Base.Vector(0,40+extrusion_width/2-part_thickness,extrusion_width/2))
vertex = vertex.cut(cylinder)

#mount to the top of the diagonal extrusion
#TODO: cleaner calculation of length of this part to avoid trimming
box = Part.makeBox(extrusion_width+40,part_thickness,extrusion_width)
box.translate(Base.Vector(-extrusion_width-15,-part_thickness,0))
#fill the space below the diagonal extrusion
box2 = Part.makeBox(extrusion_width+5,extrusion_width,extrusion_width) 
box2.translate(Base.Vector(-15,0,0))
box = box.fuse(box2)
cylinder = Part.makeCylinder(bolt_hole_diameter/2,part_thickness)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
cylinder.translate(Base.Vector(-15-extrusion_width/2,0,extrusion_width/2))
box = box.cut(cylinder)
box.rotate(Base.Vector(0,extrusion_width,0),Base.Vector(0,0,1),-30)
vertex = vertex.fuse(box)

if(accessible_hole):
    cylinder = Part.makeCylinder(bolt_hole_diameter/2,extrusion_width+60)
else:
    cylinder = Part.makeCylinder(bolt_hole_diameter/2,extrusion_width+5)
cylinder2 = Part.makeCylinder(bolt_head_diameter/2,extrusion_width+5-part_thickness)
cylinder2.translate(Base.Vector(0,0,part_thickness))
cylinder = cylinder.fuse(cylinder2)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)
cylinder.translate(Base.Vector(-15,0,0))
cylinder.translate(Base.Vector(0,extrusion_width/2,extrusion_width/2))
cylinder.rotate(Base.Vector(0,extrusion_width,0),Base.Vector(0,0,1),-30)
vertex = vertex.cut(cylinder)

box = Part.makeBox(extrusion_width,extrusion_width,extrusion_width) 
vertex = vertex.cut(box)
#TODO: eliminate this trim by cleaning above
box = Part.makeBox(40,10,extrusion_width)
box.translate(Base.Vector(-part_thickness-5,-10-part_thickness,0))
vertex = vertex.cut(box)

Part.show(vertex)
