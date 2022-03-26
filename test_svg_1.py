import math

def create_svg_file(file_path, contents):
    writeFile = open(file_path, "w")
    writeFile.write(contents)
    writeFile.close()

def get_primes():
    prime_list = []
    p_file = open("prime_set.txt")

    for x in p_file:
        clean_x = x.replace(" ", "").replace("\n", "").rstrip(",")
        #print(clean_x)
        prime_list +=clean_x.split(",")
    return prime_list

width = 300
height = 200
header = '<svg version="1.1" x="0px" y="0px" viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg">'
end = '</svg>'
background = '<rect width="100%" height="100%" fill="#ffeeaa" />'


def create_circle(cx, cy, r, fill):
    return '<circle cx="{}" cy="{}" r="{}" fill="{}" />'.format(cx, cy, r, fill)


def create_circle_in_square(tx, ty, s , fill):
    r= s/2
    cx = tx + r
    cy = ty + r
    return '<circle cx="{}" cy="{}" r="{}" fill="{}" />'.format(cx, cy, r, fill)


def circle_grid(s, c):
    #print(create_circle(3,4,5,"blue"))
    circle_string = '\n'
    square_side = s
    #
    for y in range(0, int(height/square_side)):
        for x in range(0, int(width/square_side)):
            circle_string += create_circle_in_square(x*square_side, y*square_side, square_side, c)
            circle_string += '\n'

    return circle_string


if __name__ == "__main__":
    #get_primes()
    full_code = header + background
    c= 1
    for s in [4,10,20, 25,50,100]:
        
        full_code+=circle_grid(s, "#88eeff22")
        c += 1
    full_code += end
    create_svg_file("svg_1.svg", full_code)







