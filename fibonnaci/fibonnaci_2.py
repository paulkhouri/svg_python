import math

def create_svg_file(file_path, contents):
    write_file = open(file_path, "w")
    write_file.write(contents)
    write_file.close()


def create_svg(shapes=[]):
    start_code = """
    <svg version = "1.1" viewBox = "-100 -100 200 200" xmlns = "http://www.w3.org/2000/svg" >
    <rect x = "-100" y = "-100" width = "200" height = "200" fill = "rgb(200,200,200)" />
    <line x1 = "0" x2 = "0" y1 = "-100" y2 = "100" stroke = "black" stroke-width = "0.1" />
    <line x1 = "-100" x2 = "100" y1 = "0" y2 = "0" stroke = "black" stroke-width = "0.1" />
    """
    for s in shapes:
        start_code += s
    start_code += "</svg>"
    return start_code

def circle(x,y,r, rot, x_rotation_pt, y_rotation_pt):
    circle ="""
    <circle
    cx = "{}"
    cy = "{}"
    r = "{}"
    stroke = "red"
    fill = "transparent"
    stroke-width = "1"
    transform = "{}" />
    """.format(x,y,r, run_matrix(rot, x_rotation_pt, y_rotation_pt))
    return circle

def rect(x,y,w,h,rot,rgb, x_rotation_pt=0, y_rotation_pt=0, op=1):
    xpos = x
    ypos = y
    rectangle ="""
    <rect
    x = "{}"
    y = "{}"
    width = "{}"
    height = "{}"
    fill = "{}"
    fill-opacity = "{}"
    transform = "{}" />
    """.format(xpos,ypos,w,h, rgb , op, run_matrix(rot, x_rotation_pt, y_rotation_pt))
    return rectangle

def run_matrix(rot, x_rotation_pt=0, y_rotation_pt=0):
    angle = rot*math.pi/180
    R= 1
    a = R*math.cos(angle)
    b = R*math.sin(angle)
    c= -R*math.sin(angle)
    d = R*math.cos(angle)
    e = -x_rotation_pt*math.cos(angle) + y_rotation_pt*math.sin(angle) + x_rotation_pt
    f = -x_rotation_pt*math.sin(angle) - y_rotation_pt*math.cos(angle) + y_rotation_pt
    tup = [a,b,c,d,e,f]
    for i in range(0, len(tup)):
        tup[i] = round(tup[i],3)

    text_str = "matrix({})".format(",".join(map(str, tup)) )
    print(text_str)

    return text_str

def color_set(n= 8,r_s = 115, g_s=195, b_s= 105, r_f=25, g_f=50, b_f=25):
    n = n - 1
    r_grad = (r_f - r_s) / n
    g_grad = (g_f - g_s) / n
    b_grad = (b_f - b_s) / n
    print(g_grad)
    colours = []
    for i in range(0, n + 1):
        r = r_s + i * r_grad
        g = g_s + i * g_grad
        b = b_s + i * b_grad
        col = "rgb({}, {}, {})".format(round(r), round(g), round(b))
        colours.append(col)
    return colours

if __name__ == "__main__":
    f = 'fibonacci_2.svg'
    rot=45
    x_rotation_pt = 5
    y_rotation_pt = 40
    shapes=[]
    shapes.append(rect(0, 30, 10, 20, rot, "rgb(200,50,50)", x_rotation_pt, y_rotation_pt))
    shapes.append(circle(0,0,5, rot, x_rotation_pt, y_rotation_pt))
    shapes.append(circle(x_rotation_pt, y_rotation_pt, 1,0, 0, 0))
    n= 21
    colours = color_set(n)
    w = 200/n
    h = 10
    for i in range(0, len(colours)):
        r = rect(-100+i*w, -100, w, h, 0,colours[i],0,0)
        shapes.append(r)

    svg = create_svg(shapes)
    create_svg_file(f, svg)
    #print(color_set())
