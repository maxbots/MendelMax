import math

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
small_printer = True

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