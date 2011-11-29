from __future__ import division # allows floating point division from integers
from FreeCAD import Base
import sys
from math import *
import os

try:
    path = os.path.join(os.path.dirname(__file__), '..', 'include')
    i = sys.path.index(path)
except:
	sys.path.append(path)

from RegularPolygon import regPolygon

z_rail_type = 'smooth rod'
z_rod_diameter = 8
z_rod_spacing = 30
extrusion_width = 20
extrusion_y_length = 420
extrusion_diagonal_length = 340
#how far apart should the rod clamp bolt holes be?
rod_bolt_hole_spacing = 26

# import MendelMax.py settings here

#how thick should the non-flange parts be?
part_thickness = 5
#how big are the structural bolts?
main_bolt_hole_diameter = 5.5
nut_depth = 4
nut_width = 8.5
#how big are the motor bolts?
motor_bolt_hole_diameter = 3.5
motor_bolt_head_diameter = 6 #?


#voodoo based on Lower Vertex Middle dimensions (15)
hole_spacing = extrusion_y_length-((15+extrusion_diagonal_length+(extrusion_width/2))*sin(radians(30))-(extrusion_width/2)*cos(radians(30)))*2
box = Part.makeBox(hole_spacing-(extrusion_width/2*cos(radians(30))-extrusion_width/2*sin(radians(30)))*2,extrusion_width*cos(radians(30))+part_thickness,part_thickness)
mount = box

#housings for the upper X extrusions
box = Part.makeBox(extrusion_width,extrusion_width,part_thickness)
box2= Part.makeBox(part_thickness,extrusion_width,75)
box2.translate(Base.Vector(extrusion_width,0,0))
box = box.fuse(box2)
#add mounting on the inner side of the extrusion?
#box2= Part.makeBox(extrusion_width+part_thickness,part_thickness,75)
#box2.translate(Base.Vector(0,-part_thickness,0))
#box = box.fuse(box2)
#bolt holes
cylinder = Part.makeCylinder(main_bolt_hole_diameter/2,part_thickness)
cylinder.translate(Base.Vector(extrusion_width/2,extrusion_width/2,0))
box = box.cut(cylinder)
cylinder = Part.makeCylinder(main_bolt_hole_diameter/2,part_thickness)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
cylinder.translate(Base.Vector(extrusion_width/2,0,75-extrusion_width/2))
#bolt holes on the inner side
#box = box.cut(cylinder)
#cylinder.translate(Base.Vector(0,0,-20))
#box = box.cut(cylinder)
cylinder.rotate(Base.Vector(extrusion_width+part_thickness/2,-part_thickness/2,0),Base.Vector(0,0,1),-90)
box = box.cut(cylinder)
#second bolt hole on the top side
#cylinder.translate(Base.Vector(0,0,20))
#box = box.cut(cylinder)
box.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),60)
mount = mount.fuse(box)
#mirror behaves oddly with rotated parts, so we unrotate before mirroring
box.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),-60)
box = box.mirror(Base.Vector((hole_spacing-(extrusion_width/2*cos(radians(30))-extrusion_width/2*sin(radians(30)))*2)/2,0,0),Base.Vector(1,0,0))
box.rotate(Base.Vector(hole_spacing-(extrusion_width/2*cos(radians(30))-extrusion_width/2*sin(radians(30)))*2,0,0),Base.Vector(0,0,1),-60)
mount = mount.fuse(box)

#horizontal motor mount plate
box = Part.makeBox(hole_spacing-(extrusion_width/2*cos(radians(30))+extrusion_width/2*sin(radians(30)))*2,part_thickness,75)
box.translate(Base.Vector(extrusion_width*sin(radians(30)),extrusion_width*cos(radians(30)),0))
mount = mount.fuse(box)
#motor hole
cylinder = Part.makeCylinder(25/2,part_thickness)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
cylinder.translate(Base.Vector((hole_spacing-(extrusion_width/2*cos(radians(30))+extrusion_width/2*sin(radians(30)))*2)/2,0,z_rod_spacing))
cylinder.translate(Base.Vector(extrusion_width*sin(radians(30)),extrusion_width*cos(radians(30)),0))
mount = mount.cut(cylinder)
#motor bolt hole
cylinder = Part.makeCylinder(motor_bolt_hole_diameter/2,part_thickness)
#conditionally necessary counterbore 
cylinder2 = Part.makeCylinder(motor_bolt_head_diameter/2,99)
cylinder2.translate(Base.Vector(0,0,-99))
cylinder = cylinder.fuse(cylinder2)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
cylinder.translate(Base.Vector((hole_spacing-(extrusion_width/2*cos(radians(30))+extrusion_width/2*sin(radians(30)))*2)/2-31/2,0,z_rod_spacing-31/2))
cylinder.translate(Base.Vector(extrusion_width*sin(radians(30)),extrusion_width*cos(radians(30)),0))
mount = mount.cut(cylinder)
cylinder.translate(Base.Vector(31,0,0))
mount = mount.cut(cylinder)
cylinder.translate(Base.Vector(0,0,31))
mount = mount.cut(cylinder)
cylinder.translate(Base.Vector(-31,0,0))
mount = mount.cut(cylinder)

#move the mount over so we can build the latch in place before moving it back
mount.translate(Base.Vector(-((hole_spacing-(extrusion_width/2*cos(radians(30))-extrusion_width/2*sin(radians(30)))*2)/2-(7+rod_bolt_hole_spacing/2)),0,0))

#most of this code is called from RodLatch.py
#TODO: the common bits from this, RodLatch, and YRodMount should end up in a file together
#bounding box for the main curved part of the latch
box = Part.makeBox(rod_bolt_hole_spacing,extrusion_width*cos(radians(30))+part_thickness,z_rod_diameter/2+part_thickness)
box.translate(Base.Vector(7,0,0))

#main curved part of the latch, around the rod
cylinder = Part.makeCylinder(z_rod_diameter/2+part_thickness,extrusion_width*cos(radians(30))+part_thickness)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
cylinder.translate(Base.Vector(7+rod_bolt_hole_spacing/2,0,0))
latch = box.common(cylinder)

#connects the curved part to the bolt holes
box = Part.makeBox(rod_bolt_hole_spacing,14,max(part_thickness,bolt_flange_thickness))
box.translate(Base.Vector(7,0,0))
latch = latch.fuse(box)
mount = mount.fuse(latch)

#rod hole
cylinder = Part.makeCylinder(z_rod_diameter/2,extrusion_width*cos(radians(30))+part_thickness)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
cylinder.translate(Base.Vector(7+rod_bolt_hole_spacing/2,0,0))
mount = mount.cut(cylinder)

#housings for the bolt holes
cylinder = Part.makeCylinder(7,bolt_flange_thickness+nut_depth)
cylinder.translate(Base.Vector(7,7,0))
mount = mount.fuse(cylinder)
cylinder = Part.makeCylinder(7,bolt_flange_thickness+nut_depth)
cylinder.translate(Base.Vector(7+rod_bolt_hole_spacing,7,0))
mount = mount.fuse(cylinder)

#bolt holes
cylinder = Part.makeCylinder(bolt_hole_diameter/2,z_rod_diameter/2+part_thickness)
cylinder.translate(Base.Vector(7,7,0))
mount = mount.cut(cylinder)
cylinder = Part.makeCylinder(bolt_hole_diameter/2,z_rod_diameter/2+part_thickness)
cylinder.translate(Base.Vector(7+rod_bolt_hole_spacing,7,0))
mount = mount.cut(cylinder)
#captive nuts
nuthole = regPolygon(sides = 6, radius = nut_width/2, extrude = nut_depth, Z_offset = 0)
nuthole.translate(Base.Vector(7,7,bolt_flange_thickness))
mount = mount.cut(nuthole)
nuthole = regPolygon(sides = 6, radius = nut_width/2, extrude = nut_depth, Z_offset = 0)
nuthole.translate(Base.Vector(7+rod_bolt_hole_spacing,7,bolt_flange_thickness))
mount = mount.cut(nuthole)

#move the mount back into postive coordinates
mount.translate(Base.Vector(((hole_spacing-(extrusion_width/2*cos(radians(30))-extrusion_width/2*sin(radians(30)))*2)/2-(7+rod_bolt_hole_spacing/2)),0,0))
mount.translate(Base.Vector(extrusion_width*cos(radians(30)),0,0))

Part.show(mount)