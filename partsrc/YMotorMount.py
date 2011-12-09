from __future__ import division # allows floating point division from integers
import FreeCAD, Part, math
from FreeCAD import Base

def YMotorMount(
extrusion_profile = 20, 
#how far apart should the bottom frame rectangles be?
frame_rectangle_spacing = 30, 
thick_typical = 4.25, 
thick_compress = 3
):

    #TODO: use the bolt module
    main_bolt_hole_diameter = 5.5
    main_bolt_head_diameter = 10 #?
    main_bolt_bore_depth = 4

    #TODO: use the motor and bolt modules
    motor_bolt_hole_diameter = 3.5
    motor_bolt_head_diameter = 6 #?

    mount_x = frame_rectangle_spacing+extrusion_profile*2
    mount_y = extrusion_profile+thick_typical+6
    base_z = thick_compress+main_bolt_bore_depth

    motor_plate_height = 16

    #build the flat part of the mount
    box = Part.makeBox(mount_x,mount_y,base_z)
    mount = box

    #TODO: use parametric motor dimensions
    #TODO: waste less plastic on this plate
    box = Part.makeBox(mount_x-motor_plate_height*2,thick_typical,motor_plate_height)
    box.translate(Base.Vector(motor_plate_height,0,0))
    plate = box
    cylinder = Part.makeCylinder(motor_plate_height,thick_typical,Base.Vector(motor_plate_height,0,0),Base.Vector(0,1,0),90)
    cylinder.rotate(Base.Vector(motor_plate_height,0,0),Base.Vector(0,1,0),-90)
    plate = plate.fuse(cylinder)
    cylinder.rotate(Base.Vector(mount_x/2,thick_typical/2,0),Base.Vector(0,0,1),180)
    plate = plate.fuse(cylinder)
    #motor bolt holes
    cylinder = Part.makeCylinder(motor_bolt_hole_diameter/2,thick_typical)
    cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
    cylinder.translate(Base.Vector(mount_x/2-31/2,0,5.5))
    plate = plate.cut(cylinder)
    cylinder.translate(Base.Vector(31,0,0))
    plate = plate.cut(cylinder)
    cylinder.translate(Base.Vector(0,0,31))
    plate = plate.cut(cylinder)
    cylinder.translate(Base.Vector(-31,0,0))
    plate = plate.cut(cylinder)
    #motor cylinder hole
    cylinder = Part.makeCylinder(23/2,thick_typical)
    cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
    cylinder.translate(Base.Vector(mount_x/2,0,motor_plate_height))
    plate = plate.cut(cylinder)
    plate.translate(Base.Vector(0,mount_y-thick_typical,base_z))
    mount = mount.fuse(plate)

    #extrusion bolt holes
    cylinder = Part.makeCylinder(main_bolt_hole_diameter/2,base_z)
    cylinder2 = Part.makeCylinder(main_bolt_head_diameter/2,main_bolt_bore_depth)
    cylinder2.translate(Base.Vector(0,0,thick_compress))
    cylinder = cylinder.fuse(cylinder2)
    cylinder.translate(Base.Vector(extrusion_profile/2,(mount_y-thick_typical)/2,0))
    mount = mount.cut(cylinder)
    cylinder.translate(Base.Vector(mount_x-extrusion_profile,0,0))
    mount = mount.cut(cylinder)

    #reinforcements
    support_cross_section = Part.makePolygon([
    Base.Vector(0,0,0),
    Base.Vector(0,mount_y-thick_typical,0),
    Base.Vector(0,mount_y-thick_typical,motor_plate_height*math.sin(math.acos((motor_plate_height-thick_typical)/motor_plate_height))),
    Base.Vector(0,0,0)])
    face = Part.Face(support_cross_section)
    support = face.extrude(Base.Vector(thick_typical,0,0))
    cylinder = Part.makeCylinder(motor_plate_height,mount_y,Base.Vector(motor_plate_height,0,0),Base.Vector(0,1,0),90)
    cylinder.rotate(Base.Vector(motor_plate_height,0,0),Base.Vector(0,1,0),-90)
    support1 = support.common(cylinder)
    support1.translate(Base.Vector(0,0,base_z))
    mount = mount.fuse(support1)
    support.translate(Base.Vector(mount_x-thick_typical,0,0))
    cylinder.rotate(Base.Vector(motor_plate_height,0,0),Base.Vector(0,1,0),90)
    cylinder.translate(Base.Vector(mount_x-motor_plate_height*2))
    support = support.common(cylinder)
    support.translate(Base.Vector(0,0,base_z))
    mount = mount.fuse(support)

    #zip-tie tab
    box = Part.makeBox(10,10,base_z)
    box.translate(Base.Vector((mount_x-10)/2,-10,0))
    mount = mount.fuse(box)
    
    return mount

if __name__ == "__main__":
    Part.show(YMotorMount())