from __future__ import division # allows floating point division from integers
import FreeCAD, Part, math
from FreeCAD import Base

def ZRodLowerMount(
extrusion_profile = 20, 
z_rod_spacing = 30, 
z_rod_diameter = 8, 
z_screw_diameter = 9, 
hole_spacing = 30, 
#how thick should the non-flange parts be?
thick_typical = 4.25, 
thick_min = 1, 
):

    #TODO: calculate these
    extrusion_to_z_screw = 35
    thrust_bearing_diameter = 16
    thrust_bearing_depth = 4

    #TODO: 
    #how big are the clear holes for structural bolts?
    bolt_hole_diameter = 5.5
    #how big are the to-be-threaded holes for structural bolts?
    screw_hole_diameter = 4.5
    screw_hole_depth = 10

    tower_x = extrusion_profile/2+hole_spacing
    plate_x = tower_x+extrusion_profile*2

    #plate to attach to extrusion
    box = Part.makeBox(plate_x-extrusion_profile,extrusion_profile,thick_typical)
    box.translate(Base.Vector(extrusion_profile/2,0,0))
    vertex = box
    cylinder = Part.makeCylinder(extrusion_profile/2,thick_typical)
    cylinder.translate(Base.Vector(extrusion_profile/2,extrusion_profile/2,0))
    vertex = vertex.fuse(cylinder)
    cylinder.translate(Base.Vector(plate_x-extrusion_profile,0,0))
    vertex = vertex.fuse(cylinder)
    #bolt holes into extrusion
    cylinder = Part.makeCylinder(bolt_hole_diameter/2,thick_typical)
    cylinder.translate(Base.Vector(extrusion_profile/2,extrusion_profile/2,0))
    vertex = vertex.cut(cylinder)
    cylinder.translate(Base.Vector(plate_x-extrusion_profile,0,0))
    vertex = vertex.cut(cylinder)

    #"tower"
    box = Part.makeBox(tower_x-extrusion_profile,extrusion_profile,extrusion_to_z_screw+z_rod_spacing-thick_typical)
    box.translate(Base.Vector(plate_x/2-(tower_x-extrusion_profile)/2,0,thick_typical))
    vertex = vertex.fuse(box)
    cylinder = Part.makeCylinder(extrusion_profile/2,extrusion_to_z_screw+z_rod_spacing-thick_typical)
    cylinder.translate(Base.Vector(plate_x/2-(tower_x-extrusion_profile)/2,extrusion_profile/2,thick_typical))
    vertex = vertex.fuse(cylinder)
    cylinder = Part.makeCylinder(extrusion_profile/2,extrusion_to_z_screw+z_rod_spacing-thick_typical)
    cylinder.translate(Base.Vector(plate_x/2+(tower_x-extrusion_profile)/2,extrusion_profile/2,thick_typical))
    vertex = vertex.fuse(cylinder)

    #screw holes
    cylinder = Part.makeCylinder(screw_hole_diameter/2,screw_hole_depth)
    cylinder.translate(Base.Vector(plate_x/2-hole_spacing/2,extrusion_profile/2,extrusion_to_z_screw+z_rod_spacing-screw_hole_depth))
    vertex = vertex.cut(cylinder)
    cylinder.translate(Base.Vector(hole_spacing,0,0))
    vertex = vertex.cut(cylinder)

    #smooth rod hole
    cylinder = Part.makeCylinder(z_rod_diameter/2,extrusion_profile)
    cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
    cylinder.translate(Base.Vector(plate_x/2,0,extrusion_to_z_screw+z_rod_spacing))
    vertex = vertex.cut(cylinder)

    #threaded rod and thrust bearing hole
    cylinder = Part.makeCylinder(z_screw_diameter/2+1,extrusion_profile)
    cylinder2 = Part.makeCylinder(thrust_bearing_diameter/2+2,thrust_bearing_depth)
    cylinder = cylinder.fuse(cylinder2)
    cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
    cylinder.translate(Base.Vector(plate_x/2,0,extrusion_to_z_screw))
    vertex = vertex.cut(cylinder)

    #eliminate some bulk from the part to save plastic
    #cut holes in the bottom, requires bridging that will not be visible on the installed part
    cylinder = Part.makeCylinder(extrusion_profile/2-(thick_typical+thick_min)/2,extrusion_to_z_screw*3/4)
    cylinder.translate(Base.Vector(plate_x/2-(tower_x-extrusion_profile)/2,extrusion_profile/2,0))
    vertex = vertex.cut(cylinder)
    cylinder = Part.makeCylinder(extrusion_profile/2-(thick_typical+thick_min)/2,extrusion_to_z_screw*3/4)
    cylinder.translate(Base.Vector(plate_x/2+(tower_x-extrusion_profile)/2,extrusion_profile/2,0))
    vertex = vertex.cut(cylinder)
    
    return vertex

if __name__ == "__main__":
    Part.show(ZRodLowerMount())
