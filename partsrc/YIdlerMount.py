from __future__ import division # allows floating point division from integers
from FreeCAD import Base

idler_axle_diameter = 8
extrusion_width = 20
#how far apart should the bottom frame rectangles be?
frame_rectangle_spacing = 30
#how thick should the non-flange parts be?
part_thickness = 4.25
#how big are the bolts?
bolt_hole_diameter = 5.5

#TODO: import MendelMax.py settings here

#build the flat part of the mount
box = Part.makeBox(frame_rectangle_spacing+extrusion_width*2-extrusion_width,part_thickness*2,part_thickness)
box.translate(Base.Vector(extrusion_width/2.0,0))
mount = box
cylinder = Part.makeCylinder(extrusion_width/2,part_thickness)
cylinder.translate(Base.Vector(extrusion_width/2,extrusion_width/2,0))
mount = mount.fuse(cylinder)
cylinder.translate(Base.Vector(frame_rectangle_spacing+extrusion_width,0,0))
mount = mount.fuse(cylinder)

box = Part.makeBox(extrusion_width/2,extrusion_width/2,part_thickness)
box.translate(Base.Vector(extrusion_width/2,part_thickness,0))
mount = mount.fuse(box)
box.translate(Base.Vector(frame_rectangle_spacing+extrusion_width/2,0,0))
mount = mount.fuse(box)

box = Part.makeBox(extrusion_width/2,part_thickness,part_thickness)
box.translate(Base.Vector(0,extrusion_width/2,0))
mount = mount.fuse(box)
box.translate(Base.Vector(frame_rectangle_spacing+extrusion_width*3/2,0,0))
mount = mount.fuse(box)

cylinder = Part.makeCylinder(extrusion_width/2,part_thickness)
cylinder.translate(Base.Vector(extrusion_width/2,extrusion_width/2+part_thickness,0))
mount = mount.fuse(cylinder)
cylinder.translate(Base.Vector(frame_rectangle_spacing+extrusion_width,0,0))
mount = mount.fuse(cylinder)

box = Part.makeBox(bolt_hole_diameter/2,bolt_hole_diameter/2,part_thickness)
box.translate(Base.Vector(extrusion_width,part_thickness*2,0))
mount = mount.fuse(box)
box.translate(Base.Vector(frame_rectangle_spacing-bolt_hole_diameter/2,0,0))
mount = mount.fuse(box)

cylinder = Part.makeCylinder(bolt_hole_diameter/2,part_thickness)
cylinder.translate(Base.Vector(extrusion_width+bolt_hole_diameter/2,part_thickness*2+bolt_hole_diameter/2,0))
mount = mount.cut(cylinder)
cylinder.translate(Base.Vector(frame_rectangle_spacing-bolt_hole_diameter,0,0))
mount = mount.cut(cylinder)


#extrusion bolt holes
cylinder = Part.makeCylinder(bolt_hole_diameter/2,part_thickness)
cylinder.translate(Base.Vector(extrusion_width/2,extrusion_width/2+part_thickness,0))
mount = mount.cut(cylinder)
cylinder.translate(Base.Vector(frame_rectangle_spacing+extrusion_width,0,0))
mount = mount.cut(cylinder)

box = Part.makeBox(idler_axle_diameter*2+part_thickness*2,part_thickness*2,idler_axle_diameter/2+part_thickness)
box.translate(Base.Vector((frame_rectangle_spacing+extrusion_width*2)/2-(idler_axle_diameter*2+part_thickness*2)/2,0,0))
mount = mount.fuse(box)

cylinder = Part.makeCylinder(idler_axle_diameter/2+part_thickness,part_thickness*2)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
cylinder.translate(Base.Vector((frame_rectangle_spacing+extrusion_width*2)/2,0,idler_axle_diameter/2+part_thickness))
mount = mount.fuse(cylinder)

#rounded corners and idler axle hole
cylinder = Part.makeCylinder(idler_axle_diameter/2,part_thickness*2)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
cylinder.translate(Base.Vector((frame_rectangle_spacing+extrusion_width*2)/2-idler_axle_diameter-part_thickness,0,idler_axle_diameter/2+part_thickness))
mount = mount.cut(cylinder)
cylinder.translate(Base.Vector(idler_axle_diameter+part_thickness,0,0))
mount = mount.cut(cylinder)
cylinder.translate(Base.Vector(idler_axle_diameter+part_thickness,0,0))
mount = mount.cut(cylinder)

Part.show(mount)