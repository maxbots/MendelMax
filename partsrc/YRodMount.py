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

from RegularPolygon import regPolygon

y_rail_type = 'smooth rod'
y_rod_diameter = 8
y_rod_spacing = 100
#how far apart should the bottom frame rectangles be?
frame_rectangle_spacing = 30
#how thick should the non-flange parts be?
thick_min = 1
thick_compress = 3
thick_typical = 4.25
#how far apart should the rod bolt holes be?
hole_spacing_wide = 30

from MendelMax import *

#TODO: fail if y_rail_type is not 'smooth rod'

#TODO: add logic to specify bolt type instead of bolt dimensions
#how big are the bolts?
bolt_hole_diameter = 5.5
nut_depth = 4
nut_width = 8.5

#large printer version raises concerns, so this is an override to always use the 100mm-wide version
small_printer = False

#if(small_printer and y_rod_spacing>100):
    #error

#TODO: make sure tower_y > nut_depth + thick_compress
tower_x = y_rod_diameter/2+thick_compress
tower_y = hole_spacing_wide+nut_width+thick_min*2
tower_z = nut_width*math.sqrt(3)+thick_min*2

mount_x = y_rod_spacing
mount_y = frame_rectangle_spacing+extrusion_profile*2
mount_z = thick_typical

#base
box = Part.makeBox(mount_x,mount_y,mount_z)
box2 = Part.makeBox(mount_x-tower_x*2,frame_rectangle_spacing,mount_z)
box2.translate(Base.Vector(tower_x,extrusion_profile,0))
mount = box.cut(box2)

#"towers"
box = Part.makeBox(tower_x,tower_y,tower_z)
box.translate(Base.Vector(0,(mount_y-tower_y)/2,mount_z))
mount = mount.fuse(box)
box.translate(Base.Vector(y_rod_spacing-tower_x,0,0))
mount = mount.fuse(box)

#rod clamp bolt holes
nuthole = regPolygon(sides = 6, radius = nut_width/2, extrude = nut_depth, Z_offset = tower_x-nut_depth)
cylinder = Part.makeCylinder(bolt_hole_diameter/2,tower_x)
cutout = cylinder.fuse(nuthole)
cutout.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)
cutout.translate(Base.Vector(0,mount_y/2-hole_spacing_wide/2,mount_z+tower_z/2))
mount = mount.cut(cutout)
#rotations around lines in the middle of the part to re-use the same cutout
cutout.rotate(Base.Vector(0,mount_y/2,mount_z+tower_z/2),Base.Vector(1,0,0),180)
mount = mount.cut(cutout)
cutout.rotate(Base.Vector(mount_x/2,mount_y/2,0),Base.Vector(0,0,1),180)
mount = mount.cut(cutout)
cutout.rotate(Base.Vector(0,mount_y/2,mount_z+tower_z/2),Base.Vector(1,0,0),180)
mount = mount.cut(cutout)

#extrusion bolt holes and corner rounding
cornerbox = Part.makeBox(extrusion_profile/2,extrusion_profile/2,mount_z)
cornercylinder = Part.makeCylinder(extrusion_profile/2,mount_z)
cornercylinder.translate(Base.Vector(extrusion_profile/2,extrusion_profile/2,0))
cornerbox=cornerbox.cut(cornercylinder)
cylinder = Part.makeCylinder(bolt_hole_diameter/2,mount_z)
#TODO: deal with bolt hole being too close to tower
if(small_printer):
    cylinder.translate(Base.Vector(extrusion_profile/2,extrusion_profile/2,0))
else:
    box = Part.makeBox(extrusion_profile,mount_y,mount_z)
    box.translate(Base.Vector(-extrusion_profile,0,0))
    mount=mount.fuse(box)
    box.translate(Base.Vector(mount_x+extrusion_profile,0,0))
    mount=mount.fuse(box)
    cylinder.translate(Base.Vector(-extrusion_profile/2,extrusion_profile/2,0))
    cornerbox.translate(Base.Vector(-extrusion_profile,0,0))
#add the corner rounding
cylinder=cylinder.fuse(cornerbox)
mount = mount.cut(cylinder)
#rotations around lines in the middle of the part to re-use the same cutout
cylinder.rotate(Base.Vector(0,mount_y/2,mount_z/2),Base.Vector(1,0,0),180)
mount = mount.cut(cylinder)
cylinder.rotate(Base.Vector(mount_x/2,0,mount_z/2),Base.Vector(0,1,0),180)
mount = mount.cut(cylinder)
cylinder.rotate(Base.Vector(0,mount_y/2,mount_z/2),Base.Vector(1,0,0),180)
mount = mount.cut(cylinder)

#rod holes
cylinder = Part.makeCylinder(y_rod_diameter/2,tower_z+mount_z)
cylinder.translate(Base.Vector(0,mount_y/2,0))
mount = mount.cut(cylinder)
cylinder.translate(Base.Vector(y_rod_spacing,0,0))
mount = mount.cut(cylinder)

hole_spacing_wide = 30

Part.show(mount)