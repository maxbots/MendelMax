from __future__ import division # allows floating point division from integers
import FreeCAD, Part, math
from FreeCAD import Base

def YIdlerMount(
extrusion_profile = 20, 
#how far apart should the bottom frame rectangles be?
frame_rectangle_spacing = 30, 
#how thick should the non-flange parts be?
thick_typical = 4.25
):

    idler_axle_diameter = 8
    #how big are the bolts?
    bolt_hole_diameter = 5.5

    #build the flat part of the mount
    box = Part.makeBox(frame_rectangle_spacing+extrusion_profile*2-extrusion_profile,thick_typical*2,thick_typical)
    box.translate(Base.Vector(extrusion_profile/2.0,0))
    mount = box
    cylinder = Part.makeCylinder(extrusion_profile/2,thick_typical)
    cylinder.translate(Base.Vector(extrusion_profile/2,extrusion_profile/2,0))
    mount = mount.fuse(cylinder)
    cylinder.translate(Base.Vector(frame_rectangle_spacing+extrusion_profile,0,0))
    mount = mount.fuse(cylinder)

    box = Part.makeBox(extrusion_profile/2,extrusion_profile/2,thick_typical)
    box.translate(Base.Vector(extrusion_profile/2,thick_typical,0))
    mount = mount.fuse(box)
    box.translate(Base.Vector(frame_rectangle_spacing+extrusion_profile/2,0,0))
    mount = mount.fuse(box)

    box = Part.makeBox(extrusion_profile/2,thick_typical,thick_typical)
    box.translate(Base.Vector(0,extrusion_profile/2,0))
    mount = mount.fuse(box)
    box.translate(Base.Vector(frame_rectangle_spacing+extrusion_profile*3/2,0,0))
    mount = mount.fuse(box)

    cylinder = Part.makeCylinder(extrusion_profile/2,thick_typical)
    cylinder.translate(Base.Vector(extrusion_profile/2,extrusion_profile/2+thick_typical,0))
    mount = mount.fuse(cylinder)
    cylinder.translate(Base.Vector(frame_rectangle_spacing+extrusion_profile,0,0))
    mount = mount.fuse(cylinder)

    box = Part.makeBox(bolt_hole_diameter/2,bolt_hole_diameter/2,thick_typical)
    box.translate(Base.Vector(extrusion_profile,thick_typical*2,0))
    mount = mount.fuse(box)
    box.translate(Base.Vector(frame_rectangle_spacing-bolt_hole_diameter/2,0,0))
    mount = mount.fuse(box)

    cylinder = Part.makeCylinder(bolt_hole_diameter/2,thick_typical)
    cylinder.translate(Base.Vector(extrusion_profile+bolt_hole_diameter/2,thick_typical*2+bolt_hole_diameter/2,0))
    mount = mount.cut(cylinder)
    cylinder.translate(Base.Vector(frame_rectangle_spacing-bolt_hole_diameter,0,0))
    mount = mount.cut(cylinder)


    #extrusion bolt holes
    cylinder = Part.makeCylinder(bolt_hole_diameter/2,thick_typical)
    cylinder.translate(Base.Vector(extrusion_profile/2,extrusion_profile/2+thick_typical,0))
    mount = mount.cut(cylinder)
    cylinder.translate(Base.Vector(frame_rectangle_spacing+extrusion_profile,0,0))
    mount = mount.cut(cylinder)

    box = Part.makeBox(idler_axle_diameter*2+thick_typical*2,thick_typical*2,idler_axle_diameter/2+thick_typical)
    box.translate(Base.Vector((frame_rectangle_spacing+extrusion_profile*2)/2-(idler_axle_diameter*2+thick_typical*2)/2,0,0))
    mount = mount.fuse(box)

    cylinder = Part.makeCylinder(idler_axle_diameter/2+thick_typical,thick_typical*2)
    cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
    cylinder.translate(Base.Vector((frame_rectangle_spacing+extrusion_profile*2)/2,0,idler_axle_diameter/2+thick_typical))
    mount = mount.fuse(cylinder)

    #rounded corners and idler axle hole
    cylinder = Part.makeCylinder(idler_axle_diameter/2,thick_typical*2)
    cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
    cylinder.translate(Base.Vector((frame_rectangle_spacing+extrusion_profile*2)/2-idler_axle_diameter-thick_typical,0,idler_axle_diameter/2+thick_typical))
    mount = mount.cut(cylinder)
    cylinder.translate(Base.Vector(idler_axle_diameter+thick_typical,0,0))
    mount = mount.cut(cylinder)
    cylinder.translate(Base.Vector(idler_axle_diameter+thick_typical,0,0))
    mount = mount.cut(cylinder)
    
    return mount

if __name__ == "__main__":
    Part.show(YIdlerMount())