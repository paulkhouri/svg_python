import math


def top_angle(n):
    N = n
    """ return the angle at the top vertex of the polygon
    for one of the triangular faces"""
    if N % 4 != 0:
        print("Sides must be divisible by 4")
        return None
    # centre angle of one sector of the polygon
    theta = 2*math.pi / N
    Q = N/4
    cos_theta_top = 1 - math.pow(math.cos((Q-1)*theta), 2)/2
    top_angle = math.acos(cos_theta_top)
    return top_angle


def trapezium_angle(theta, n):
    """get lower internal angle of an isosceles trapezium where
    sides are length S, the top side is length SCos(n*theta) and the
    bottom side is length SCos((n-1)*theta)

    :argument
    theta (float) 1 centre angle of polygon
    n (int) the first (top) n value

    :return
    angle (float)
     """
    numerator = math.pow(math.cos((n-1)*theta), 2) - math.pow(math.cos((n)*theta), 2)
    denominator = 2*(math.cos(n*theta) + math.cos((n-1)*theta))
    cos_phi = numerator/denominator
    angle = math.acos(cos_phi)
    return angle


def rad_to_deg(rad):
    deg = rad*180/math.pi
    print(deg)


def create_string(side_list):
    p_string = ""
    for p in side_list:
        p_string += ",".join(str(e) for e in p) + " "
    #print(p_string)
    return p_string


def create_svg_code(pointstrings):
    output= """<?xml version="1.0" encoding="utf-8"?>
<!-- Generator: Adobe Illustrator 24.2.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 viewBox="-100 -200 500 500" style="enable-background:new 0 0 85.04 85.04;" xml:space="preserve">
<style type="text/css">
	.st0{fill:none;stroke:#000000;stroke-miterlimit:10;}
	.st1{fill:none;stroke:#FF0000;stroke-miterlimit:10;}
</style>\n
    """
    for x in pointstrings:
        output += x
        output+='\n'


    output += '</svg>'
    #print(output)
    return output

def create_svg_file(file_path, contents):
    write_file = open(file_path, "w")
    write_file.write(contents)
    write_file.close()


def reflect_on_line(point,theta):
    # reflect on line half theta
    # reflect B on the line <tcos(theta_top/2),tsin(theta_top/2)>
    #x_b, y_b ---> x_b*cos(2 theta_top/2) + y_b*sin(2 theta_top/2), x_b*sin(2 theta_top/2) - y_b*cos(2 theta_top/2)
    x= point[0] * math.cos(2 * theta/ 2) + + point[1] * math.sin(2 * theta / 2)
    y= point[0] * math.sin(2 * theta / 2) - point[1] * math.cos(2 * theta / 2)
    return [x,y]

def rotate(point,theta):
    # rotate 2D point on theta
    x = point[0]*math.cos(theta) - point[1]*math.sin(theta)
    y = point[0]*math.sin(theta) + point[1]*math.cos(theta)
    return [x,y]

def polygon(n):
    if n % 4 != 0:
        print("Sides must be divisible by 4")
        return None
    N = n
    angle_set=[]
    #and at top point of polyhedron
    theta_top = top_angle(N)
    angle_set.append(theta_top)
    #rad_to_deg(theta_top)

    # center angle of one side of polygon that makes the polyhedron
    theta_centre = 2 * math.pi / N
    a= (N/4)-1
    while a>0:
        phi = trapezium_angle(theta_centre, a)
        angle_set.append(phi)
        a -= 1
    # have [theta top, phi_1, phi_2, ...]
    #print(angle_set)
    # first gamma calculation
    gamma = angle_set[1] - math.pi / 2 + angle_set[0]/ 2
    O=[0,0]
    A=[1,0]
    points = [O,A]
    a = (N / 4) - 1
    c = 1
    while c <= a:
        P = [points[c][0]+math.cos(gamma), points[c][1] + math.sin(gamma)]
        points.append(P)
        # unused on last iteration
        gamma += angle_set[2] - angle_set[1]
        c += 1
    #print(points)
    # reflect points C , B , A on half theta_top line
    p = len(points)-1
    while p > 0:
        prime = reflect_on_line(points[p], angle_set[0])
        points.append(prime)
        p -= 1
    # [O, A, B, C, C', B', A']
    #print(points)
    # side length
    R=100
    S = R*math.sqrt( 2*(1 - math.cos(theta_centre)) )
    #scale
    for i in range(0, len(points)):
        for j in range(0, len(points[i])):
            points[i][j] = S*points[i][j]
    print(points)
    # ------ folding lines
    folding_lines=[]
    a= len(points)-1
    b=1
    temp = [points[a], points[0]]

    while a-b > 1:
        folding_lines.append([points[a],points[b]])
        a -= 1
        b += 1
    folding_lines.append(temp)
    print(folding_lines)
    #--------
    #rotate
    # if N is 12 there will now be 7 points in the list (N/2)+1
    # take the last 5 of these in any iteration and rotate by theta_top
    c=0
    while c<N-1:
        for i in range(len(points) - (int(N/2) - 1 ), len(points)):
            points.append( rotate(points[i], angle_set[0]) )
        c+=1
    #---- folding lines
    c=0
    len_f_lines = len(folding_lines)
    while c < N-1:
        for i in range(len(folding_lines) - len_f_lines, len(folding_lines)):
            temp = []
            for x in folding_lines[i]:
                temp.append(rotate(x, angle_set[0]))
            folding_lines.append(temp)
        c+=1
    folding_lines.pop()


    #-----
    lines_to_svg =[]
    # points and produce points as svg string for polyline
    points_string = create_string(points)
    polygon = '<polygon class="st0" points="{}"/> \n'.format(points_string)
    lines_to_svg.append(polygon)

    # ---- folding lines
    for x in folding_lines:
        temp = create_string(x)
        polyline = '<polyline class="st1" points="{}"/> \n'.format(temp)
        lines_to_svg.append(polyline)
    #---------
    svg_code = create_svg_code(lines_to_svg)
    create_svg_file("test_v4.svg", svg_code)


def polygon_twelve():
    N = 12
    angle_set=[]
    theta_top = top_angle(N)
    angle_set.append(theta_top)
    print(theta_top)
    rad_to_deg(theta_top)

    theta_centre = 2 * math.pi / N
    a= (N/4)-1
    while a>0:
        phi = trapezium_angle(theta_centre, a)
        angle_set.append(phi)
        a -= 1
    # have [theta top, phi_1, phi_2, ...]
    print(angle_set)
    # first gamma calculation
    gamma = angle_set[1] - math.pi / 2 + angle_set[0]/ 2
    rad_to_deg(gamma)
    O=[0,0]
    A=[1,0]
    B= [A[0]+math.cos(gamma), A[1] + math.sin(gamma)]
    # subsequent gamma calculations form
    gamma += angle_set[2] - angle_set[1]
    C = [B[0] + math.cos(gamma), B[1] + math.sin(gamma)]
    points = [O, A, B, C]
    # reflect points C , B , A on half theta_top line
    p = len(points)-1
    while p > 0:
        prime = reflect_on_line(points[p], angle_set[0])
        points.append(prime)
        p -= 1
    # [O, A, B, C, C', B', A']
    # set up folding lines ------  start here but complete looping after the lines have been scaled
    line_set = [ [ points[0], points[-1] ] ]
    c= 1
    upper_limit = math.floor(len(points)/2)
    while c < upper_limit:
        line_set.append( [ points[c] , points[len(points) - c] ])
        c+=1
    print(len(line_set))
    print(line_set)

    c=0
    while c<N-1:
        for i in range(len(points) - (int(N/2) - 1 ), len(points)):
            points.append( rotate(points[i], angle_set[0]) )
        c+=1




    # side length
    R=100
    S = R*math.sqrt( 2*(1 - math.cos(theta_centre)) )
    #scale
    for i in range(0, len(points)):
        for j in range(0, len(points[i])):
            points[i][j] = S*points[i][j]

    points_set = create_string(points)
    #print(points_set)
    # complete folding lines - now that scaling has been done
    c = 0
    while c<N-1:
        for j in range(len(line_set)-3, len(line_set)):
            line_set.append( [ rotate( line_set[j][0] , angle_set[0]), rotate(line_set[j][1] , angle_set[0]) ] )
        c+=1


    polyline_block = ""
    for i in range(0, len(line_set)):
        short_line = create_string(line_set[i])

        polyline = '<polyline class="st1" points="{}"/> \n'.format(short_line)
        polyline_block += polyline

    svg = create_svg_code(points_set, polyline_block)
    create_svg_file("test_twelve_v2.svg", svg)





if __name__ == "__main__":
    #polygon_set()
    #gen_tests()
    #polygon_twelve()
    polygon(12)



