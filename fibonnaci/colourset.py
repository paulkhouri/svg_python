import numpy as np
import math

n=8
n= n-1
r_s = 115
g_s= 195
b_s = 105
r_f = 25
g_f= 50
b_f = 25

r_grad= (r_f - r_s)/n
g_grad= (g_f - g_s)/n
b_grad= (b_f - b_s)/n
print(g_grad)
colours = []
for i in range(0, n+1):
    r = r_s + i*r_grad
    g = g_s + i * g_grad
    b = b_s + i * b_grad
    col = "rgb({}, {}, {})".format(round(r),round(g),round(b))
    print(col)


