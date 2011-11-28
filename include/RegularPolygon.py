def regPolygon(sides, radius=0, type="inner", edgeLength=0, \
    X_offset=0, Y_offset=0, Z_offset=0, \
    vX=0,vY=0,vZ=0, \
    rotation=0, extrude=0, makeFace= 1):
    # # of sides
    #sides = 6
    
    # Draw the polygon based on the radius of a circle insdie the polygon, 
    # touching the center of the flats
    #type = "inner" 
    # Draw the polygon based on the radius of a circle outside the polygon,
    # touching the corners
    #type = "outer"
    # Draw the polygon with a predefined edge length
    #type = "edgeLength"

    # Radius, either inner or outer
    # ignored if type = "edgeLength"
    #radius = 2

    # The length of each edge
    # ignored if type = "inner" or "outer" if using  
    #edgeLength = 2

    # Position of the center point of starting face
    #X_offset = 6
    #Y_offset = -3
    #Z_offset = 0

    # Vectors
    #vX = 0
    #vY = 0
    #vZ = 0

    # By default, the first point is drawn on the X axis.
    # Set to a value in radians to rotate from the default
    #rotation = -4

    # extrude length, leave 0 for a 2d polygon
    #extrude = 20
    
    # Set makeFace to 0 if you do not want a face
    #makeFace = 0

    import FreeCAD, Part, math
    from FreeCAD import Base
    from math import pi, cos, sin

    if sides < 3:
        raise ValueError("Sides must be >=3")
    if radius == 0 and edgeLength == 0:
        raise ValueError("Either radius or edgeLength must be assigined a non-zero value")
    
    r = {'inner': 0, 'outer': 0}
    i = 'innner' ## Allows shorthand r[i] instead of r["inner"]
    o = 'outer'  ## Bad form, but useful
        
    # The function defines the polygon by the radius of a circle drawn 
    # outside the polygon, in other words, the radius is the distance 
    # from the center of the circle to one of the corners. 
    ## Many common polygons, such as nuts and bolts are defined by 
    # the radius inside the polygon, IOW the radius is the distance 
    # from the center of the circle to the point on the flat side 
    # closest to the center. 
    #
    # In other cases, we may want to define a polygon by the length of the 
    # sides rather than the radius. 
    #
    # Since we need the outside radius for our calculations, we need 
    # to calculate the correct outer radius here 
    #
    # We should never need to know the R[i], but if we are specifying
    # the outer radius we will calculate the R[i] anyway, just for 
    # future flexibility
    # http://www.algebra.com/algebra/homework/Polygons/Inscribed-and-circumscribed-polygons.lesson
    if type == "inner":
        r[i] = radius 
        r[o] = radius / cos(pi/sides)
        radius = r[o]   
    elif type == "edgeLength":
        radius = (edgeLength / (2*sin(pi/sides)))
        r[o] = radius
        r[i] = (edgeLength / (2*tan(pi/sides)))
    else:
        r[i] = cos(pi/sides) * radius 
        r[o] = radius
    
    # Define the starting point for our calculations
    # regardless of the final orientation, we will start working in the X & Y
    x = radius
    y = 0
    z = Z_offset
    
    # Set initial point if rotation was specified and save it for the end point 
    startx = round((x*cos((0))) - (y*sin((0))), 4)
    starty = round((x*sin((0))) + (y*cos((0))), 4)
    
    x = startx
    y = starty  
    
    # create the points list and define the first point, off set in X,Y, and Z as needed
    points = [(Base.Vector(x + X_offset,y  + Y_offset, z))]
    
    # Calculate the remaining points    
    # These calculations assume the circle is centered at 0,0, so 
    # the offset is applied after the calculations are applied
    for step in range (1, sides):
        # http://en.wikipedia.org/wiki/Cartesian_coordinate_system#Rotation
        newx = round((x*cos((2*pi/sides))) - (y*sin((2*pi/sides))), 4)
        newy = round((x*sin((2*pi/sides))) + (y*cos((2*pi/sides))), 4)
        x = newx
        y = newy    
        points.append((Base.Vector(x + X_offset,y  + Y_offset,z)))
    
    points.append((startx + X_offset, starty + Y_offset,z))
    print(points)
    polygon = Part.makePolygon(points)
    
    if makeFace != 0:
        polygon = Part.Face(polygon)

    if extrude != 0:
        polygon = polygon.extrude(Base.Vector(0,0,extrude))
    
    #polygon.rotate(vX, vY, vZ)

    return polygon