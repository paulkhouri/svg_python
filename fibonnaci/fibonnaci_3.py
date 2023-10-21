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

def rect(x,y,w,h,rot,rgb, x_rotation_pt=0, y_rotation_pt=0, R=3,op=1):
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
    """.format(xpos,ypos,w,h, rgb , op, run_matrix(rot, x_rotation_pt, y_rotation_pt, R))
    return rectangle

def run_matrix(alpha=0, tranX=0, tranY=0, R = 1):
    """
    a c e
    b d f
    0 0 1
    R.cos(alpha)  -R.sin(alpha)   -tranX.R.cos(alpha) + tranY.R.sin(alpha) + tranX
    R.sin(alpha)   R.cos(alpha)   -tranX.R.sin(alpha) - tranY.R.cos(aplha) + tranY
    0              0                1

    :param alpha:  rotation (degrees)
    :param tranX: rotation pt x, tranX=0
    :param tranY: rotation pt y,  tranY=0
    :param R: scale, R=1
    :return:
    """
    angle = alpha*math.pi/180
    a = R*math.cos(angle)
    b = R*math.sin(angle)
    c= -R*math.sin(angle)
    d = R*math.cos(angle)
    e = -tranX*R*math.cos(angle) + tranY*R*math.sin(angle) + tranX
    f = -tranX*R*math.sin(angle) - tranY*R*math.cos(angle) + tranY
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
    f = 'fibonacci_3.svg'
    n = 21
    colours = color_set(n)
    rot=45
    x_rotation_pt = 0
    y_rotation_pt = 0
    shapes=[]
    c=0
    for rot in range(0,360,30):
        shapes.append(rect(-2, 0, 4, 20, rot, colours[c], x_rotation_pt, y_rotation_pt,1+ rot/360,1))
        c += 1
    shapes.append(circle(0,0,5, rot, x_rotation_pt, y_rotation_pt))
    shapes.append(circle(x_rotation_pt, y_rotation_pt, 1,0, 0, 0))

    w = 200/n
    h = 10
    for i in range(0, len(colours)):
        r = rect(-100+i*w, -100, w, h, 0,colours[i],0,0,1,1)
        shapes.append(r)

    svg = create_svg(shapes)
    create_svg_file(f, svg)
    #print(color_set())
