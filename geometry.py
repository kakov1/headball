def solve(a, b, r, floor, roof):
    d = r**2 - b**2
    if d < 0:
        return 0
    elif d == 0:
        return a if floor <= a <= roof else 0
    else:
        x1 = d**0.5 + a
        x2 = -(d**0.5) + a
        if floor <= x1 <= roof:
            return x1
        elif floor <= x2 <= roof:
            return x2
        else: 
            return 0

def intersection(a, b, c, x0, y0, r, floor, roof): 
    if a == 0:
        x = solve(x0, c - y0, r, floor, roof)
        if x == 0:
            return -1, -1
        else:
            return x, c          
    else:
        y = solve(y0, c - x0, r, floor ,roof)
        if y == 0:
            return -1, -1
        else:
            return c, y  
