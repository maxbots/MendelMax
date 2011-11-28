from __future__ import division # allows floating point division from integers
from FreeCAD import Base
import math

small_printer = 1
extrusion_width = 20

# import MendelMax.py settings here

bolt_hole_diameter = 5.5
# how thick should the part be?
part_thickness = 4
# how far apart should the holes be?
hole_spacing = 20
# how much wider than the spacing should the plates be?
plate_padding = 10
# how far should the plates be from the extrusion corner?
corner_offset = 60
# how wide should the strut be?
diagonal_width = 17

if(small_printer):
    if(corner_offset+hole_spacing+plate_padding*2>100):
        plate_padding = max(bolt_hole_diameter/2+1,(100-(corner_offset+hole_spacing))/2)
        hole_spacing = 100-(corner_offset+plate_padding*2)
        #need logic to reduce the number of holes if they overlap
        diagonal_width = min(diagonal_width,(hole_spacing+plate_padding*2)/math.sqrt(2))

shape = Part.makePolygon([
Base.Vector(corner_offset,0,0),
Base.Vector(corner_offset+hole_spacing+plate_padding*2,0,0),
Base.Vector(corner_offset+hole_spacing+plate_padding*2,extrusion_width,0),
Base.Vector(corner_offset+(hole_spacing+plate_padding*2)/2+diagonal_width/2*math.sqrt(2),extrusion_width,0),
Base.Vector(extrusion_width,corner_offset+(hole_spacing+plate_padding*2)/2+diagonal_width/2*math.sqrt(2),0),
Base.Vector(extrusion_width,corner_offset+hole_spacing+plate_padding*2,0),
Base.Vector(0,corner_offset+hole_spacing+plate_padding*2,0),
Base.Vector(0,corner_offset,0),
Base.Vector(extrusion_width,corner_offset,0),
Base.Vector(extrusion_width,corner_offset+(hole_spacing+plate_padding*2)/2-diagonal_width/2*math.sqrt(2),0),
Base.Vector(corner_offset+(hole_spacing+plate_padding*2)/2-diagonal_width/2*math.sqrt(2),extrusion_width,0),
Base.Vector(corner_offset,extrusion_width,0),
Base.Vector(corner_offset,0,0),
])
face = Part.Face(shape)
vertex = face.extrude(Base.Vector(0,0,part_thickness))

cylinder = Part.makeCylinder(bolt_hole_diameter/2,part_thickness)
cylinder.translate(Base.Vector(corner_offset+plate_padding,extrusion_width/2,0))
vertex = vertex.cut(cylinder)
cylinder.translate(Base.Vector(hole_spacing,0,0))
vertex = vertex.cut(cylinder)
cylinder.rotate(Base.Vector(0,0,part_thickness/2),Base.Vector(1,1,0),180)
vertex = vertex.cut(cylinder)
cylinder.translate(Base.Vector(0,-hole_spacing,0))
vertex = vertex.cut(cylinder)

Part.show(vertex)