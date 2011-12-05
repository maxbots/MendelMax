from __future__ import division # allows floating point division from integers
from FreeCAD import Base
from math import *
import sys
import os

try:
    path = os.path.join(os.path.dirname(__file__), '..', 'include')
    i = sys.path.index(path)
except:
    sys.path.append(path)

#relevant local defaults
extrusion_profile = 20
frame_rectangle_spacing = 30
#how thick should the non-flange parts be?
thick_typical = 4.25

from MendelMax import *

#how big are the structural bolts?
#TODO: replace with use of bolt module after it's written
bolt_hole_diameter = 5.5
bolt_head_diameter = 10

#should there be a visible hole for easy access to the "hidden" bolt?
accessible_hole = 1
#should we draw the extrusions for visualization purposes?
render_extrusions = 0

#this block of code draws the extrusions as a separate Shape, for comparison purposes
if(render_extrusions):
    #y extrusion
    box = Part.makeBox(extrusion_profile,80,extrusion_profile)
    box.translate(Base.Vector(0,extrusion_profile,0))
    extrusions = box
    #y extrusion
    box = Part.makeBox(extrusion_profile,80,extrusion_profile)
    box.translate(Base.Vector(0,extrusion_profile,0))
    box.translate(Base.Vector(frame_rectangle_spacing+extrusion_profile,0,0))
    extrusions = extrusions.fuse(box)
    #x extrusion
    box = Part.makeBox(extrusion_profile,extrusion_profile,80)
    extrusions = extrusions.fuse(box)
    #x extrusion
    box = Part.makeBox(extrusion_profile,extrusion_profile,80)
    box.translate(Base.Vector(frame_rectangle_spacing+extrusion_profile,0,0))
    extrusions = extrusions.fuse(box)
    #diagonal extrusion
    box = Part.makeBox(80,extrusion_profile,extrusion_profile)
    box.translate(Base.Vector(-95,0,0))
    box.rotate(Base.Vector(0,extrusion_profile,0),Base.Vector(0,0,1),-30)
    extrusions = extrusions.fuse(box)
    
    Part.show(extrusions)

#connect the two X extrusions
box = Part.makeBox(frame_rectangle_spacing+extrusion_profile*2,thick_typical,extrusion_profile)
box.translate(Base.Vector(0,-thick_typical,0))
vertex = box
cylinder = Part.makeCylinder(bolt_hole_diameter/2,thick_typical)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
cylinder.translate(Base.Vector(extrusion_profile/2,0,extrusion_profile/2))
vertex = vertex.cut(cylinder)
cylinder.translate(Base.Vector(frame_rectangle_spacing+extrusion_profile,0,0))
vertex = vertex.cut(cylinder)

#mount to the top of the top Y extrusion
box = Part.makeBox(thick_typical,40+extrusion_profile,extrusion_profile)
box.translate(Base.Vector(-thick_typical,-thick_typical,0))
vertex = vertex.fuse(box)
cylinder = Part.makeCylinder(bolt_hole_diameter/2,thick_typical)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),-90)
cylinder.translate(Base.Vector(0,40+extrusion_profile/2-thick_typical,extrusion_profile/2))
vertex = vertex.cut(cylinder)

#mount to the top of the diagonal extrusion
#TODO: cleaner calculation of length of this part to avoid trimming
box = Part.makeBox(extrusion_profile+40,thick_typical,extrusion_profile)
box.translate(Base.Vector(-extrusion_profile-15,-thick_typical,0))
#fill the space below the diagonal extrusion
box2 = Part.makeBox(extrusion_profile+5,extrusion_profile,extrusion_profile) 
box2.translate(Base.Vector(-15,0,0))
box = box.fuse(box2)
cylinder = Part.makeCylinder(bolt_hole_diameter/2,thick_typical)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
cylinder.translate(Base.Vector(-15-extrusion_profile/2,0,extrusion_profile/2))
box = box.cut(cylinder)
box.rotate(Base.Vector(0,extrusion_profile,0),Base.Vector(0,0,1),-30)
vertex = vertex.fuse(box)

if(accessible_hole):
    cylinder = Part.makeCylinder(bolt_hole_diameter/2,extrusion_profile+60)
else:
    cylinder = Part.makeCylinder(bolt_hole_diameter/2,extrusion_profile+5)
cylinder2 = Part.makeCylinder(bolt_head_diameter/2,extrusion_profile+5-thick_typical)
cylinder2.translate(Base.Vector(0,0,thick_typical))
cylinder = cylinder.fuse(cylinder2)
cylinder.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),90)
cylinder.translate(Base.Vector(-15,0,0))
cylinder.translate(Base.Vector(0,extrusion_profile/2,extrusion_profile/2))
cylinder.rotate(Base.Vector(0,extrusion_profile,0),Base.Vector(0,0,1),-30)
vertex = vertex.cut(cylinder)

box = Part.makeBox(extrusion_profile,extrusion_profile,extrusion_profile) 
vertex = vertex.cut(box)
#TODO: eliminate this trim by cleaning above
box = Part.makeBox(40,10,extrusion_profile)
box.translate(Base.Vector(-thick_typical-5,-10-thick_typical,0))
vertex = vertex.cut(box)

Part.show(vertex)
