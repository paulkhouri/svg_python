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
    
    <defs>
    <style>
      .cls-1 {
        fill: #3ab54a;
        stroke-width: 0px;
        fill-opacity:0.7;
      }
        .cls-2 {
        fill: #3ab5aa;
        stroke-width: 0px;
        fill-opacity:0.7;
      }
    </style>
  </defs>
<g transform="scale(1.5)">
  <rect x="0" y="0" width="30" height="70" fill = "black"/>
  <path class="cls-2" d="m30 ,38.3C30,27.74 ,15 ,0 ,15,0,15,0,0,27.74,0,38.3s14.06,10.57,14.06,10.57v18.49l-.94,2.64h3.75l-.94-2.64v-18.49s14.06,0,14.06-10.57Z"
  transform="scale(0.5) translate(-15,-70) rotate(80 15 70)"
  />
    <path class="cls-2" d="m30 ,38.3C30,27.74 ,15 ,0 ,15,0,15,0,0,27.74,0,38.3s14.06,10.57,14.06,10.57v18.49l-.94,2.64h3.75l-.94-2.64v-18.49s14.06,0,14.06-10.57Z"
  transform="scale(0.75) translate(-15,-70) rotate(120 15 70)"
  />
  </g>
 

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
    f = 'fibonacci.svg'
    sequence = [1,1,2,3,5,8,13,21,34]
    r = 2
    n = 5
    shapes = []
    rot = r*2*math.pi/n
    for i in range(0,n):
        shapes.append(generate_shape(1,5*i+5, i*rot, "rgb(200,50,50)"))
    svg = create_svg(shapes)
    create_svg_file(f, svg)