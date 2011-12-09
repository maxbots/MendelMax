from __future__ import division # allows floating point division from integers
import FreeCAD, Part, math
from FreeCAD import Base

#TODO: make all of this a package so we can do local imports without hacking the path
import sys, os
try:
    path = os.path.dirname(__file__)
    i = sys.path.index(path)
except:
    sys.path.append(path)

def MendelMax():
    # Determines whether we are just generating the model, or if we are exporting the STL's as we go
    # 0 = No STL's
    # 1 = Export STL's
    export_stl = 0
    
    #all measurements are in mm until unit conversion is added

    #extrusion_profile 20mm, 25mm, 1"
    extrusion_profile = 20

    #how tall is the gap between the two bottom frame rectangles?
    frame_rectangle_spacing = 30

    #size_type ["extrusion length", "build area", "bounding box"]
    size_type = "extrusion length"

    extrusion_x_length = 300
    extrusion_y_length = 420
    extrusion_diagonal_length = 340

    #build_x_length, build_y_width, build_z_height (build area)
    #outside_x_length, outside_y_width, outsize_z_height (bounding box)

    #x_rail_type ["makerslide", "smooth rod"]
    x_rail_type = "smooth rod"
    x_rod_diameter = 8
    x_rod_spacing = 50
    #x_rod_orientation ["horizontal","vertical"]
    x_rod_orientation = "horizontal"

    #y_rail_type ["makerslide", "smooth rod"]
    y_rail_type = "smooth rod"
    y_rod_diameter = 8
    y_rod_spacing = 100

    #z_rail_type ["makerslide", "smooth rod"]
    z_rail_type = "smooth rod"
    z_rod_diameter = 8
    z_screw_diameter = 8
    #distance from z smooth rod to z threaded rod
    z_rod_spacing = 30

    #["NEMA14", "NEMA17", "NEMA23"]
    #TODO: implement motor module for dimensions, etc
    x_motor_size = "NEMA17"
    y_motor_size = "NEMA17"
    z_motor_size = "NEMA17"

    x_pulley_teeth_count = 36
    x_pulley_teeth_spacing = 2
    x_pulley_pitch_diameter = 72/math.pi
    y_pulley_teeth_count = 36
    y_pulley_teeth_spacing = 2
    y_pulley_pitch_diameter = 72/math.pi

    #should we limit parts to 100mmx100mm build area?
    small_printer = False

    #bushing_type ["printed","IGUS [part#]"LM8UU",etc]
    #y_carriage_height, y_carriage_width, y_carriage_depth
    #x_bearing_type, y_bearing_type ["608ZZ"]
    #build_platform_height, build_platform_width, build_platform_depth

    #absolute minimum thickness of any printed part, this is usually a constraint of the printing method to be used
    thick_min = 1
    #minimum vertical (the layered direction) thickness of any printed part
    thick_min_vertical = 2
    #minimum thickness of a part under compression, such as the edge of bolt holes
    thick_compress = 3
    #typical thickness of printed parts, for flat plates and such
    thick_typical = 4.25

    #TODO: better system for organizing these
    hole_spacing_narrow = 10
    hole_spacing_medium = 20
    hole_spacing_wide = 30

    # .-------.       .-------. -
    # |       | <-A-> |       |   B
    # | .-----         -----. | -    -    
    # | |       <-C->       | | _ D  ^
    # |  \                 /  |      |
    # |   \               /   |      E
    # |    \             /    |      v
    # |     ----<-F->----     |      -
    #
    #  <--extrusion_profile-->

    extrusion_slot_opening_width = 6 #A
    extrusion_slot_opening_depth = 2 #B
    extrusion_slot_width = 11 #C
    extrusion_slot_vertical_depth = 1 #D
    extrusion_slot_depth = 4 #E

    #TODO: describe the profile more thoroughly
    extrusion_outline = Part.makePolygon([Base.Vector(0,0,0),Base.Vector(0,extrusion_profile,0),Base.Vector(extrusion_profile,extrusion_profile,0),Base.Vector(extrusion_profile,0,0),Base.Vector(0,0,0)])
    extrusion_face = Part.Face(extrusion_outline)

    #TODO: learn how to initialize this object correctly
    extrusions = Part.makeBox(1,1,1)

    x_extrusion_lower = extrusion_face.extrude(Base.Vector(0,0,extrusion_x_length))
    x_extrusion_lower.rotate(Base.Vector(extrusion_profile/2,0,extrusion_profile/2),Base.Vector(0,1,0),90)
    extrusions = extrusions.fuse(x_extrusion_lower)
    x_extrusion_lower.translate(Base.Vector(0,0,frame_rectangle_spacing+extrusion_profile))
    extrusions = extrusions.fuse(x_extrusion_lower)
    x_extrusion_lower.translate(Base.Vector(0,extrusion_y_length+extrusion_profile,0))
    extrusions = extrusions.fuse(x_extrusion_lower)
    x_extrusion_lower.translate(Base.Vector(0,0,-(frame_rectangle_spacing+extrusion_profile)))
    extrusions = extrusions.fuse(x_extrusion_lower)

    y_extrusion = extrusion_face.extrude(Base.Vector(0,0,extrusion_y_length))
    y_extrusion.rotate(Base.Vector(0,extrusion_profile/2,extrusion_profile/2),Base.Vector(1,0,0),-90)
    y_extrusion.translate(Base.Vector(0,extrusion_profile,0))
    extrusions = extrusions.fuse(y_extrusion)
    y_extrusion.translate(Base.Vector(0,0,frame_rectangle_spacing+extrusion_profile))
    extrusions = extrusions.fuse(y_extrusion)
    y_extrusion.translate(Base.Vector(extrusion_x_length-extrusion_profile,0,0))
    extrusions = extrusions.fuse(y_extrusion)
    y_extrusion.translate(Base.Vector(0,0,-(frame_rectangle_spacing+extrusion_profile)))
    extrusions = extrusions.fuse(y_extrusion)

    diagonal_extrusion = extrusion_face.extrude(Base.Vector(0,0,extrusion_diagonal_length))
    diagonal_extrusion.translate(Base.Vector(0,0,frame_rectangle_spacing+extrusion_profile*2+15))
    diagonal_extrusion.rotate(Base.Vector(0,extrusion_profile,frame_rectangle_spacing+extrusion_profile*2),Base.Vector(1,0,0),-30)
    extrusions = extrusions.fuse(diagonal_extrusion)
    diagonal_extrusion.translate(Base.Vector(extrusion_x_length-extrusion_profile,0,0))
    extrusions = extrusions.fuse(diagonal_extrusion)
    diagonal_extrusion.rotate(Base.Vector(extrusion_x_length-extrusion_profile/2,(extrusion_y_length+extrusion_profile*2)/2,0),Base.Vector(0,0,1),180)
    extrusions = extrusions.fuse(diagonal_extrusion)
    diagonal_extrusion.translate(Base.Vector(-(extrusion_x_length-extrusion_profile),0,0))
    extrusions = extrusions.fuse(diagonal_extrusion)

    x_extrusion_upper = extrusion_face.extrude(Base.Vector(0,0,extrusion_x_length+120))
    x_extrusion_upper.rotate(Base.Vector(extrusion_profile/2,0,extrusion_profile/2),Base.Vector(0,1,0),90)
    x_extrusion_upper.translate(Base.Vector(-60,0,frame_rectangle_spacing+extrusion_profile*2+15+extrusion_diagonal_length))
    x_extrusion_upper.rotate(Base.Vector(0,extrusion_profile,frame_rectangle_spacing+extrusion_profile*2),Base.Vector(1,0,0),-30)
    extrusions = extrusions.fuse(x_extrusion_upper)
    x_extrusion_upper.rotate(Base.Vector(extrusion_x_length/2,(extrusion_y_length+extrusion_profile*2)/2,0),Base.Vector(0,0,1),180)
    extrusions = extrusions.fuse(x_extrusion_upper)

    Part.show(extrusions)

    y_rod = Part.makeCylinder(y_rod_diameter/2,extrusion_y_length,Base.Vector(0,0,0),Base.Vector(0,1,0))
    y_rod.translate(Base.Vector(extrusion_x_length/2-y_rod_spacing/2,extrusion_profile,(frame_rectangle_spacing+extrusion_profile*2)/2))
    Part.show(y_rod)
    y_rod.translate(Base.Vector(y_rod_spacing,0,0))
    Part.show(y_rod)

    import partsrc.LowerVertexMiddle
    import partsrc.LowerVertex
    import partsrc.RodLatch
    import partsrc.TopVertexX
    import partsrc.YIdlerMount
    import partsrc.YMotorMount
    import partsrc.YRodMount
    import partsrc.ZMotorMount
    import partsrc.ZRodLowerMount

    #TODO: figure out or fix mirroring so that we can avoid code duplication in all of these translations
    lvm = partsrc.LowerVertexMiddle.LowerVertexMiddle(extrusion_profile, frame_rectangle_spacing, thick_typical)
    lvm.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)
    lvm.translate(Base.Vector(0,0,frame_rectangle_spacing+extrusion_profile*2))
    Part.show(lvm)
    lvm.translate(Base.Vector(extrusion_x_length-extrusion_profile,0,0))
    Part.show(lvm)
    lvm.rotate(Base.Vector(extrusion_x_length-extrusion_profile/2,(extrusion_y_length+extrusion_profile*2)/2,0),Base.Vector(0,0,1),180)
    Part.show(lvm)
    lvm.translate(Base.Vector(-(extrusion_x_length-extrusion_profile),0,0))
    Part.show(lvm)

    lv = partsrc.LowerVertex.LowerVertex(extrusion_profile, frame_rectangle_spacing, hole_spacing_medium, thick_typical)
    lv.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)
    lv.translate(Base.Vector(-thick_typical,0,frame_rectangle_spacing+extrusion_profile*2))
    Part.show(lv)
    lv.translate(Base.Vector(extrusion_x_length+thick_typical,0,0))
    Part.show(lv)
    lv.rotate(Base.Vector(extrusion_x_length+thick_typical/2,(extrusion_y_length+extrusion_profile*2)/2,0),Base.Vector(0,0,1),180)
    Part.show(lv)
    lv.translate(Base.Vector(-(extrusion_x_length+thick_typical),0,0))
    Part.show(lv)

    tvx = partsrc.TopVertexX.TopVertexX(extrusion_profile, thick_typical, hole_spacing_medium)
    tvx.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
    tvx.translate(Base.Vector(0,-thick_typical,frame_rectangle_spacing+extrusion_profile*3+15+extrusion_diagonal_length))
    tvx.rotate(Base.Vector(0,extrusion_profile,frame_rectangle_spacing+extrusion_profile*2),Base.Vector(1,0,0),-30)
    Part.show(tvx)
    tvx.rotate(Base.Vector(extrusion_x_length/2,(extrusion_y_length+extrusion_profile*2)/2,0),Base.Vector(0,0,1),180)
    Part.show(tvx)
    tvx = partsrc.TopVertexX.TopVertexX()
    tvx.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),-90)
    tvx.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)
    tvx.translate(Base.Vector(extrusion_x_length,-thick_typical,frame_rectangle_spacing+extrusion_profile*3+15+extrusion_diagonal_length))
    tvx.rotate(Base.Vector(0,extrusion_profile,frame_rectangle_spacing+extrusion_profile*2),Base.Vector(1,0,0),-30)
    Part.show(tvx)
    tvx.rotate(Base.Vector(extrusion_x_length/2,(extrusion_y_length+extrusion_profile*2)/2,0),Base.Vector(0,0,1),180)
    Part.show(tvx)

    yim = partsrc.YIdlerMount.YIdlerMount(extrusion_profile, frame_rectangle_spacing, thick_typical)
    yim.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
    yim.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),-90)
    yim.translate(Base.Vector(extrusion_x_length/2-10,0,0))
    Part.show(yim)
    yim.rotate(Base.Vector(extrusion_x_length/2,0,(frame_rectangle_spacing+extrusion_profile*2)/2),Base.Vector(0,1,0),180)
    Part.show(yim)

    ymm = partsrc.YMotorMount.YMotorMount(extrusion_profile, frame_rectangle_spacing, thick_typical, thick_compress)
    ymm.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
    ymm.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),-90)
    ymm.translate(Base.Vector(extrusion_x_length/2+20+ymm.BoundBox.YLength-thick_typical,0,0))
    ymm.rotate(Base.Vector(extrusion_x_length/2,(extrusion_y_length+extrusion_profile*2)/2,(frame_rectangle_spacing+extrusion_profile*2)/2),Base.Vector(0,0,1),180)
    Part.show(ymm)

    yrm = partsrc.YRodMount.YRodMount(extrusion_profile, y_rail_type, y_rod_diameter, y_rod_spacing, frame_rectangle_spacing, thick_typical, thick_compress, thick_min, hole_spacing_wide)
    yrm.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
    yrm.rotate(Base.Vector(0,extrusion_profile/2,(frame_rectangle_spacing+extrusion_profile*2)/2),Base.Vector(1,0,0),180)
    yrm.translate(Base.Vector(extrusion_x_length/2-y_rod_spacing/2,0,0))
    Part.show(yrm)
    yrm.rotate(Base.Vector(extrusion_x_length/2,(extrusion_y_length+extrusion_profile*2)/2,(frame_rectangle_spacing+extrusion_profile*2)/2),Base.Vector(0,0,1),180)
    Part.show(yrm)

    zrlm = partsrc.ZRodLowerMount.ZRodLowerMount(extrusion_profile, z_rod_spacing, z_rod_diameter, z_screw_diameter, hole_spacing_wide, thick_typical, thick_min)
    zrlm.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),-90)
    zrlm.rotate(Base.Vector(0,extrusion_profile,0),Base.Vector(1,0,0),-90)
    zrlm.translate(Base.Vector(0,extrusion_y_length/2-zrlm.BoundBox.YLength/2))
    Part.show(zrlm)
    zrlm.rotate(Base.Vector(extrusion_x_length/2,(extrusion_y_length+extrusion_profile*2)/2,0),Base.Vector(0,0,1),180)
    Part.show(zrlm)

    zmm = partsrc.ZMotorMount.ZMotorMount(z_rail_type, z_rod_diameter, z_rod_spacing, extrusion_profile, extrusion_y_length, extrusion_diagonal_length, hole_spacing_wide, thick_typical, thick_compress)
    zmm.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),90)
    zmm.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)
    zmm.translate(Base.Vector(
    -60-thick_typical,
    (extrusion_y_length+extrusion_profile*2)/2-zmm.BoundBox.YLength/2,
    (extrusion_diagonal_length+15)*math.cos(math.radians(30))+frame_rectangle_spacing+extrusion_profile*2
    ))
    Part.show(zmm)
    zmm.rotate(Base.Vector(extrusion_x_length/2,(extrusion_y_length+extrusion_profile*2)/2,0),Base.Vector(0,0,1),180)
    Part.show(zmm)

    #TODO: place all 8 rod latches in the correct positions
        #partsrc.RodLatch.RodLatch(z_rod_diameter, hole_spacing_wide, thick_typical, thick_compress)
        #partsrc.RodLatch.RodLatch(y_rod_diameter, hole_spacing_wide, thick_typical, thick_compress)

    #TODO: add Z rods
    #TODO: add motors
    #TODO: add bolts, probably in the form of a toggle when generating the parts
    #TODO: add Y idler hardware

MendelMax()