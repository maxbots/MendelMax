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

from RegularPolygon import regPolygon

y_rail_type = 'smooth rod'
y_rod_diameter = 8
y_rod_spacing = 100

#how thick should the non-flange parts be?
part_thickness = 4
#TODO: add logic to specify bolt type instead of bolt dimensions
#how big are the bolts?
bolt_hole_diameter = 5.5
nut_depth = 4
nut_width = 8.5
#how far apart should the rod bolt holes be?
bolt_hole_spacing = 26

#TODO: import MendelMax.py settings here

#large printer version raises concerns, so this is an override to always use the 100mm-wide version
small_printer = 1

#if(small_printer and y_rod_spacing>100):
    #error

#base
box = Part.makeBox(y_rod_spacing,70,part_thickness)
if(small_printer):
  box2 = Part.makeBox(y_rod_spacing-y_rod_diameter-part_thickness*2,30,part_thickness)
  box2.translate(Base.Vector(y_rod_diameter/2+part_thickness,20,0))
else:
  box2 = Part.makeBox(y_rod_spacing-y_rod_diameter-part_thickness*2,40,part_thickness)
  box2.translate(Base.Vector(y_rod_diameter/2+part_thickness,15,0))
mount = box.cut(box2)

#TODO: make towers wider to accomodate wider bolt_hole_spacing
#"towers"
box = Part.makeBox(y_rod_diameter/2+part_thickness,40,nut_width+part_thickness*2)
box.translate(Base.Vector(0,15,part_thickness))
mount = mount.fuse(box)
box.translate(Base.Vector(y_rod_spacing-y_rod_diameter/2-part_thickness,0,0))
mount = mount.fuse(box)

#rod clamp bolt holes
nuthole = regPolygon(sides = 6, radius = nut_width/2, extrude = nut_depth, Z_offset = y_rod_diameter/2+part_thickness-nut_depth)
cylinder = Part.makeCylinder(bolt_hole_diameter/2,y_rod_diameter/2+part_thickness)
cutout = cylinder.fuse(nuthole)
cutout.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)
cutout.translate(Base.Vector(0,70/2-bolt_hole_spacing/2,part_thickness*2+nut_width/2))
mount = mount.cut(cutout)
#rotations around lines in the middle of the part to re-use the same cutout
cutout.rotate(Base.Vector((y_rod_diameter/2+part_thickness)/2,70/2,part_thickness*2+nut_width/2),Base.Vector(1,0,0),180)
mount = mount.cut(cutout)
cutout.rotate(Base.Vector(y_rod_spacing/2,70/2,part_thickness*2+nut_width/2),Base.Vector(0,0,1),180)
mount = mount.cut(cutout)
cutout.rotate(Base.Vector(y_rod_spacing-(y_rod_diameter/2+part_thickness)/2,70/2,part_thickness*2+nut_width/2),Base.Vector(1,0,0),180)
mount = mount.cut(cutout)

#extrusion bolt holes and corner rounding
cornerbox = Part.makeBox(12,12,part_thickness)
cornercylinder = Part.makeCylinder(12,part_thickness)
cornercylinder.translate(Base.Vector(12,12,0))
cornerbox=cornerbox.cut(cornercylinder)
cylinder = Part.makeCylinder(bolt_hole_diameter/2,part_thickness)
if(small_printer):
    cylinder.translate(Base.Vector(10,10,0))
else:
    box = Part.makeBox(12,70,part_thickness)
    box.translate(Base.Vector(-12,0,0))
    mount=mount.fuse(box)
    box.translate(Base.Vector(y_rod_spacing+12,0,0))
    mount=mount.fuse(box)
    cylinder.translate(Base.Vector(-2,10,0))
#add the corner rounding
cylinder=cylinder.fuse(cornerbox)
mount = mount.cut(cylinder)
#rotations around lines in the middle of the part to re-use the same cutout
cylinder.rotate(Base.Vector(0,70/2,part_thickness/2),Base.Vector(1,0,0),180)
mount = mount.cut(cylinder)
cylinder.rotate(Base.Vector(y_rod_spacing/2,0,part_thickness/2),Base.Vector(0,1,0),180)
mount = mount.cut(cylinder)
cylinder.rotate(Base.Vector(0,70/2,part_thickness/2),Base.Vector(1,0,0),180)
mount = mount.cut(cylinder)

#rod holes
cylinder = Part.makeCylinder(y_rod_diameter/2,nut_width+part_thickness*3)
cylinder.translate(Base.Vector(0,35,0))
mount = mount.cut(cylinder)
cylinder.translate(Base.Vector(y_rod_spacing,0,0))
mount = mount.cut(cylinder)

Part.show(mount)