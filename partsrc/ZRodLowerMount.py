from __future__ import division # allows floating point division from integers
from FreeCAD import Base
import sys
from math import *

extrusion_width = 20
z_rod_spacing = 30
z_rod_diameter = 8
z_screw_diameter = 9
screw_hole_spacing = 26

# import MendelMax.py settings here

#TODO: calculate these
extrusion_to_z_screw = 35
thrust_bearing_diameter = 16
thrust_bearing_depth = 4

#how thick should the non-flange parts be?
part_thickness = 5
#how big are the clear holes for structural bolts?
bolt_hole_diameter = 5.5
#how big are the to-be-threaded holes for structural bolts?
screw_hole_diameter = 4.5
screw_hole_depth = 10


#plate to attach to extrusion
box = Part.makeBox(extrusion_width*2+screw_hole_spacing,extrusion_width,part_thickness)
box.translate(Base.Vector(extrusion_width/2,0,0))
vertex = box
cylinder = Part.makeCylinder(extrusion_width/2,part_thickness)
cylinder.translate(Base.Vector(extrusion_width/2,extrusion_width/2,0))
vertex = vertex.fuse(cylinder)
cylinder.translate(Base.Vector(screw_hole_spacing+extrusion_width*2,0,0))
vertex = vertex.fuse(cylinder)
#bolt holes into extrusion
cylinder = Part.makeCylinder(bolt_hole_diameter/2,part_thickness)
cylinder.translate(Base.Vector(extrusion_width/2,extrusion_width/2,0))
vertex = vertex.cut(cylinder)
cylinder.translate(Base.Vector(screw_hole_spacing+extrusion_width*2,0,0))
vertex = vertex.cut(cylinder)

#"tower"
box = Part.makeBox(screw_hole_spacing,extrusion_width,extrusion_to_z_screw+z_rod_spacing-part_thickness)
box.translate(Base.Vector(extrusion_width*3/2,0,part_thickness))
vertex = vertex.fuse(box)
cylinder = Part.makeCylinder(extrusion_width/2,extrusion_to_z_screw+z_rod_spacing-part_thickness)
cylinder.translate(Base.Vector(extrusion_width*3/2,extrusion_width/2,part_thickness))
vertex = vertex.fuse(cylinder)
cylinder.translate(Base.Vector(screw_hole_spacing,0,0))
vertex = vertex.fuse(cylinder)

#screw holes
cylinder = Part.makeCylinder(screw_hole_diameter/2,screw_hole_depth)
cylinder.translate(Base.Vector(extrusion_width*3/2,extrusion_width/2,extrusion_to_z_screw+z_rod_spacing-screw_hole_depth))
vertex = vertex.cut(cylinder)
cylinder.translate(Base.Vector(screw_hole_spacing,0,0))
vertex = vertex.cut(cylinder)

#smooth rod hole
cylinder = Part.makeCylinder(z_rod_diameter/2,extrusion_width)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
cylinder.translate(Base.Vector(extrusion_width*3/2+screw_hole_spacing/2,0,extrusion_to_z_screw+z_rod_spacing))
vertex = vertex.cut(cylinder)

#threaded rod and thrust bearing hole
cylinder = Part.makeCylinder(z_screw_diameter/2+1,extrusion_width)
cylinder2 = Part.makeCylinder(thrust_bearing_diameter/2+2,thrust_bearing_depth)
cylinder = cylinder.fuse(cylinder2)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
cylinder.translate(Base.Vector(extrusion_width*3/2+screw_hole_spacing/2,0,extrusion_to_z_screw))
vertex = vertex.cut(cylinder)

Part.show(vertex)
