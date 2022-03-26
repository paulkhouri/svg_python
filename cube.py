import copy

def top_create_first_list_points(n):
    """
    Get first line of points

    This creates the first side of the top section
    This side is then rotated and translated to create the other 3 sides

    :param n : (int) number of units of the side
    :return: (list)  points for that side
    """
    base_list = []
    for i in range(0,2*(n-1)):
        base_list.append(0)
    # set first and last point
    base_list[0] = [0,1]
    base_list[2*(n-1)-1] = [n-2, 0]

    c = 1
    for i in range(3, 2*(n-1) , 4):
        base_list[i] = [c,1]
        base_list[i+1] = [c+1, 1]
        base_list[i-2] = [c-1,0]
        base_list[i-2 +1 ] = [c, 0]

        c+=2

    return base_list

def side_create_first_list_points(base_list):
    # remove first point of base list
    #  reflect on y = 0.5
    side_face=[]
    base_list.pop(0)
    for p in base_list:
        p_temp = reflect_on_line(0.5,p)
        side_face.append(translate_only([1,0], p_temp))

    print(side_face)
    return side_face


def reflect_on_line(c, point):
    """
    Relect a point on a horizontal line

    :param c: (float) the c for the y = c line for reflection
    :param point: (list) x,y point
    :return: (list) x_new , y_new
    """

    return [point[0] , 2*c - point[1]]


def rotate_translate(rotate_point, translate_vector, point):
    """
       rotate 90 degree clockwise and translate a given point

       x_new = a + b - y + x_t
       y_new = x - a + b + y_t

       Parameters:
       rotate_point (list): a,b point
       translate_vector (list): x_t, y_t vector
       point (list) : x,y point

       Returns:
       list: new x,y

       """
    x = point[0]
    y = point[1]
    a = rotate_point[0]
    b = rotate_point[1]
    x_t = translate_vector[0]
    y_t = translate_vector[1]
    # result
    x_n = a + b - y + x_t
    y_n = x - a + b + y_t

    return [x_n, y_n]

def translate_only(translate_vector, point):
    """
       translate a given point

       Parameters:
       translate_vector (list): x_t, y_t vector
       point (list) : x,y point

       Returns:
       list: new x,y

       """
    x_n = translate_vector[0] + point[0]
    y_n = translate_vector[1] + point[1]
    return [x_n, y_n]

def rotate_only(point):
    """
       rotate a given point 90 degrees clockwise on (0,0)

       Parameters:
       point (list) : x,y point

       Returns:
       list: new x,y

       """

    return [-point[1], point[0]]



def rotate_translate_side(rotate_point, translate_vector, side_list):
    final_list = []
    final_list += side_list
    #rotate_point = [0,1]
    #translate_vector = [n-1, -1]
    loop_list = side_list
    for i in range(0,3):
        temp_list = []
        for p in loop_list:
            temp_list.append(rotate_translate(rotate_point, translate_vector, p))
        #print(temp_list)
        # move rotation point by translation vector
        final_list += temp_list
        rotate_point = translate_only(translate_vector, rotate_point)
        # rotate translation vector
        translate_vector = rotate_only(translate_vector)
        # update loop list to the last created tem list
        loop_list = temp_list


    #print(side_list)
    #print(final_list)
    return final_list

def set_unit_expand(u, side_list):
    # illustrator pixel - mm convert
    # 72 ppi
    # 1 inch = 25.4 mm
    # 72/25.4 = 2.834645669
    # c = 2.83
    c = 2.834645669
    for p in side_list:
        p[0] = p[0]*u*c
        p[1] = p[1]*u*c
    #print(side_list)
    return side_list

def create_string(side_list):
    p_string = ""
    for p in side_list:
        p_string += ",".join(str(e) for e in p) + " "
    #print(p_string)
    return p_string


def create_svg_code(p_string):
    output= """<?xml version="1.0" encoding="utf-8"?>
<!-- Generator: Adobe Illustrator 24.2.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 viewBox="0 0 283 283" style="enable-background:new 0 0 85.04 85.04;" xml:space="preserve">
<style type="text/css">
	.st0{fill:none;stroke:#000000;stroke-miterlimit:10;}
</style>
    """

    output += '<polygon class="st0" points="{}"/> \n'.format(p_string)
    output += '</svg>'
    #print(output)
    return output


def create_svg_file(file_path, contents):
    write_file = open(file_path, "w")
    write_file.write(contents)
    write_file.close()


if __name__ == "__main__":
    # number of sides
    n = 8
    # top_bottom
    base_list = top_create_first_list_points(n)
    print(base_list)
    # rotate_point = [0,1]
    # translate_vector = [n-1, -1]
    # point = [0,0]
    # print(rotate_translate(rotate_point, translate_vector, point))

    side_list = copy.deepcopy(base_list)
    full_points = rotate_translate_side( [0,1], [n-1, -1], side_list)
    print(base_list)
    expanded_full_points = set_unit_expand(10,full_points)
    print(base_list)

    points_string = create_string(expanded_full_points)




    svg_graphic = create_svg_code(points_string)
    create_svg_file("top_bottom.svg", svg_graphic)

    # sides
    side_base = side_create_first_list_points(base_list)
    full_points = rotate_translate_side([1, 1], [n - 2, 0], side_base)
    expanded_full_points = set_unit_expand(10, full_points)
    points_string = create_string(expanded_full_points)
    svg_graphic = create_svg_code(points_string)
    create_svg_file("side.svg", svg_graphic)

