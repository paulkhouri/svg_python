import math


def top_angle(n):
    N = n
    """ return the angle at the top vertex of the polygon
    for one of the triangular faces"""
    if N % 4 != 0:
        print("Sides must be divisible by 4")
        return None

    theta = 2*math.pi / N
    Q = N/4
    cos_theta = 1 - math.pow(math.cos((Q-1)*theta), 2)/2
    angle = math.acos(cos_theta)
    return angle


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


def create_svg_code(p_string, m=""):
    output= """<?xml version="1.0" encoding="utf-8"?>
<!-- Generator: Adobe Illustrator 24.2.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 viewBox="-100 -200 500 500" style="enable-background:new 0 0 85.04 85.04;" xml:space="preserve">
<style type="text/css">
	.st0{fill:none;stroke:#000000;stroke-miterlimit:10;}
	.st1{fill:none;stroke:#FF0000;stroke-miterlimit:10;}
</style>
    """

    output += '<polygon class="st0" points="{}"/> \n'.format(p_string)
    output += m
    output += '</svg>'
    #print(output)
    return output

def create_svg_file(file_path, contents):
    write_file = open(file_path, "w")
    write_file.write(contents)
    write_file.close()

def gen_tests():
    angle = top_angle(8)
    print(angle)
    rad_to_deg(angle)
    #angle = top_angle(12)
    #print(angle)
    #rad_to_deg(angle)
    theta = 2 * math.pi / 8
    angle = trapezium_angle(theta, 1)
    print(angle)
    rad_to_deg(angle)
    theta = 2*math.pi/12
    for i in range(2,0, -1):
        angle = trapezium_angle(theta, i)
        print(angle)
        rad_to_deg(angle)

def reflect_on_line(point,theta):
    # reflect on line half theta
    # reflect B on the line <tcos(theta_top/2),tsin(theta_top/2)>
    #x_b, y_b ---> x_b*cos(2 theta_top/2) + y_b*sin(2 theta_top/2), x_b*sin(2 theta_top/2) - y_b*cos(2 theta_top/2)
    x= point[0] * math.cos(2 * theta/ 2) + + point[1] * math.sin(2 * theta / 2)
    y= point[0] * math.sin(2 * theta / 2) - point[1] * math.cos(2 * theta / 2)
    return [x,y]

def rotate(point,theta):
    x = point[0]*math.cos(theta) - point[1]*math.sin(theta)
    y = point[0]*math.sin(theta) +point[1]*math.cos(theta)
    return [x,y]

def polygon_set():
    # [theta_top, phi for trapezium]
    #0.7227342478134157
    #41.40962210927086
    #1.4238211361313915
    #81.57894188185058
    angles = [0.7227342478134157, 1.4238211361313915]
    #gamma = phi - pi/2 + theta_t/2
    gamma = angles[1] - math.pi / 2 + angles[0]/ 2
    rad_to_deg(gamma)
    # octogon
    O=[0,0]
    A=[1,0]
    B= [A[0]+math.cos(gamma), A[1] + math.sin(gamma)]
    # reflect B on the line <tcos(theta_top/2),tsin(theta_top/2)>
    #x_b, y_b ---> x_b*cos(2 theta_top/2) + y_b*sin(2 theta_top/2), x_b*sin(2 theta_top/2) - y_b*cos(2 theta_top/2)
    B_prime = reflect_on_line(B, angles[0])
    A_prime = reflect_on_line(A, angles[0])
    points = [O,A,B, B_prime, A_prime]
    c=0
    while c<7:
        for i in range(len(points)-3, len(points)):
            points.append( rotate(points[i], angles[0]) )
        c+=1


    #scale
    for i in range(0, len(points)):
        for j in range(0, len(points[i])):
            points[i][j] = 100*points[i][j]
    # translate y
    # for i in range(0, len(points)):
    #     points[i][1]+=100




    points_set = create_string(points)
    print(points_set)
    polyline_block = ""

    lines = [O, A_prime, A]
    lines_set = create_string(lines)
    polyline = '<polyline class="st1" points="{}"/> \n'.format(lines_set)
    polyline_block += polyline
    c= 0
    while c<7:
        if c == 6:
            lines.pop(0)
        for i in range(0, len(lines)):
            lines[i] = rotate(lines[i],angles[0])
        lines_set = create_string(lines)
        polyline = '<polyline class="st1" points="{}"/> \n'.format(lines_set)
        polyline_block += polyline
        c+=1



    svg = create_svg_code(points_set,polyline_block)

    create_svg_file("test_octogon.svg", svg)




if __name__ == "__main__":
    polygon_set()
    #gen_tests()



