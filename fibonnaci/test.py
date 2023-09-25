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

def generate_shape(w,h,rot,rgb):
    xpos = -w/2
    ypos = -h/2
    xpos = 0
    ypos = 0
    rectangle ="""
    <rect
    x = "{}"
    y = "{}"
    width = "{}"
    height = "{}"
    fill = "{}"
    fill-opacity = "{}"
    transform = "{}" />
    """.format(xpos,ypos,w,h, rgb , 0.2, run_matrix(rot))
    return rectangle

def run_matrix(rot):
    angle = rot
    R= 1
    a = R*math.cos(angle)
    b = R*math.sin(angle)
    c= -R*math.sin(angle)
    d = R*math.cos(angle)
    x= 0
    y = 0
    tup = [a,b,c,d,x,y]
    for i in range(0, len(tup)):
        tup[i] = round(tup[i],3)

    return "matrix({})".format(",".join(map(str, tup)) )





if __name__ == "__main__":
    f = 'test.svg'
    shapes = []
    for i in range(0,48):
        shapes.append(generate_shape(1,i+5, i*math.pi/12, "rgb(200,50,50)"))
    svg = create_svg(shapes)
    create_svg_file(f, svg)