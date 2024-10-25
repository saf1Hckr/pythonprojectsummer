# Analysis of Algorithms (CS 323)
# Summer 2024
# Assignment 4 - Computational Geometry
# Mubashirul Islam

# Acknowleagements：
# I worked with class
# I used the following sites
# GeeksforGeek


from random import randint
import matplotlib.pyplot as plt
import math
from functools import cmp_to_key


# [1] Define a function generate_points(n, mn, mx) to make a random list of points in 2D, with each coordinate being between mn and mx.
def generate_points(n, mn, mx):
    return [(randint(mn, mx), randint(mn, mx)) for i in range(n)]

# [2] Define a function line(points, i, j) that finds the line between two points in a list.
def compute_line(points, i, j):
    Q = points[i]
    P = points[j]
    a = Q[1] - P[1]
    b = P[0] - Q[0]
    c = a * (P[0]) + b * (P[1])
    sign = "-" if b < 0 else "+"
    line = f"{a}x {sign} {b}y = {c}"
    return line

# [3] Define a function draw_points(points) to draw the points using a package like matplotlib
def draw_points(points, file_name):
    x, y = get_x_y(points)
    style = 'go-'
    for i in range(0, len(x)):
        plt.plot(x[i:i + 2], y[i:i + 2], style)
    plt.plot([x[0], x[-1]], [y[0], y[-1]], style)
    plt.savefig(file_name)
    plt.show()

# [5] Define a  function sort_points(points) to sort the points in clockwise (or counterclockwise) order
def sort_points(points):
        def key(x):
            atan = math.atan2(x[1], x[0])
            return (atan, x[1] ** 2 + x[0] ** 2) if atan >= 0 else (2 * math.pi + atan, x[0] ** 2 + x[1] ** 2)
        return sorted(points, key=key)

# [6] Define a function to compute the convex hull of a set of points. You may use any algorithm
def quad(p):
    if p[0] >= 0 and p[1] >= 0:
        return 1
    if p[0] <= 0 and p[1] >= 0:
        return 2
    if p[0] <= 0 and p[1] <= 0:
        return 3
    return 4
# Checks whether the line is crossing the polygon
def orientation(a, b, c):
    res = (b[1]-a[1]) * (c[0]-b[0]) - (c[1]-b[1]) * (b[0]-a[0])
    if res == 0:
        return 0
    if res > 0:
        return 1
    return -1
# compare function for sorting

def compare(p1, q1):
    p = [p1[0]-mid[0], p1[1]-mid[1]]
    q = [q1[0]-mid[0], q1[1]-mid[1]]
    one = quad(p)
    two = quad(q)
    if one != two:
        if one < two:
            return -1
        return 1
    if p[1]*q[0] < q[1]*p[0]:
        return -1
    return 1
# Finds upper tangent of two polygons 'a' and 'b'
# represented as two vectors.

def merger(a, b):
    # n1 -> number of points in polygon a
    # n2 -> number of points in polygon b
    n1, n2 = len(a), len(b)
    ia, ib = 0, 0
    # ia -> rightmost point of a
    for i in range(1, n1):
        if a[i][0] > a[ia][0]:
            ia = i
    # ib -> leftmost point of b
    for i in range(1, n2):
        if b[i][0] < b[ib][0]:
            ib = i
    # finding the upper tangent
    inda, indb = ia, ib
    done = 0
    while not done:
        done = 1
        while orientation(b[indb], a[inda], a[(inda+1) % n1]) >= 0:
            inda = (inda + 1) % n1
        while orientation(a[inda], b[indb], b[(n2+indb-1) % n2]) <= 0:
            indb = (indb - 1) % n2
            done = 0
    uppera, upperb = inda, indb
    inda, indb = ia, ib
    done = 0
    g = 0
    while not done:  # finding the lower tangent
        done = 1
        while orientation(a[inda], b[indb], b[(indb+1) % n2]) >= 0:
            indb = (indb + 1) % n2
        while orientation(b[indb], a[inda], a[(n1+inda-1) % n1]) <= 0:
            inda = (inda - 1) % n1
            done = 0
    ret = []
    lowera, lowerb = inda, indb
    # ret contains the convex hull after merging the two convex hulls
    # with the points sorted in anti-clockwise order
    ind = uppera
    ret.append(a[uppera])
    while ind != lowera:
        ind = (ind+1) % n1
        ret.append(a[ind])
    ind = lowerb
    ret.append(b[lowerb])
    while ind != upperb:
        ind = (ind+1) % n2
        ret.append(b[ind])
    return ret
# Brute force algorithm to find convex hull for a set
# of less than 6 points

def bruteHull(a):
    # Take any pair of points from the set and check
    # whether it is the edge of the convex hull or not.
    # if all the remaining points are on the same side
    # of the line then the line is the edge of convex
    # hull otherwise not
    global mid
    s = set()
    for i in range(len(a)):
        for j in range(i+1, len(a)):
            x1, x2 = a[i][0], a[j][0]
            y1, y2 = a[i][1], a[j][1]
            a1, b1, c1 = y1-y2, x2-x1, x1*y2-y1*x2
            pos, neg = 0, 0
            for k in range(len(a)):
                if (k == i) or (k == j) or (a1*a[k][0]+b1*a[k][1]+c1 <= 0):
                        neg += 1
                if (k == i) or (k == j) or (a1*a[k][0]+b1*a[k][1]+c1 >= 0):
                        pos += 1
            if pos == len(a) or neg == len(a):
                s.add(tuple(a[i]))
                s.add(tuple(a[j]))
    ret = []
    for x in s:
        ret.append(list(x))
    # Sorting the points in the anti-clockwise order
    mid = [0, 0]
    n = len(ret)
    for i in range(n):
        mid[0] += ret[i][0]
        mid[1] += ret[i][1]
        ret[i][0] *= n
        ret[i][1] *= n
    ret = sorted(ret, key=cmp_to_key(compare))
    for i in range(n):
        ret[i] = [ret[i][0]/n, ret[i][1]/n]
    return ret
# Returns the convex hull for the given set of points

def divide(a):
    # If the number of points is less than 6 then the
    # function uses the brute algorithm to find the
    # convex hull
    if len(a) <= 5:
        return bruteHull(a)
    # left contains the left half points
    # right contains the right half points
    left, right = [], []
    start = int(len(a)/2)
    for i in range(start):
        left.append(a[i])
    for i in range(start, len(a)):
        right.append(a[i])
    # convex hull for the left and right sets
    left_hull = divide(left)
    right_hull = divide(right)
    # merging the convex hulls
    return merger(left_hull, right_hull)


def convex_hull(points):
    n = len(points)
    sorted_points = sort_points(points)
    ch = divide(sorted_points)
    print('The Convex Hull for the points', points, "is", ch)
    return ch

# [7] Define a function compute_area(points) to find the area of the convex hull, not the original set.
def compute_area(points):
    area = 0.0
    n = len(points)
    j = n - 1
    x, y = get_x_y(points)
    for i in range(n):
        area += (x[j] + x[i]) * (y[j] - y[i])
        j = i
    return (abs(area / 2.0))

# [8] Define a function compute_perimeter(points) to find the perimeter of the convex hull, not the original set.
def compute_perimeter(points):
    perimeter = 0.0
    n = len(points)
    j = n - 1
    x, y = get_x_y(points)
    for i in range(n):
        perimeter += math.sqrt((x[j] - x[i]) * (x[j] - x[i]) +
                               (y[j] - y[i]) * (y[j] - y[i]))
        j = i
    return perimeter

def get_x_y(points):
    return [point[0] for point in points], [point[1] for point in points]

# [9] Define a function is_equable(points) to determine if the shape is equable (area and perimeter are equal)
def is_equable(points):
    if (compute_perimeter(points) == compute_area(points)):
        print("The shape of convex hull is Equable")
    else:
        print("The shape of convex hull is Not Equable")

# [10] Define a function closest_pair(points) to determine the closest pair in a set of points
def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def brute_force(points):
    min_dist = float('inf')
    closest_pair = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = dist(points[i], points[j])
            if d < min_dist:
                min_dist = d
                closest_pair = (points[i], points[j])
    return closest_pair, min_dist

def strip_closest(strip, d):
    min_dist = d
    closest_pair = None
    strip.sort(key=lambda x: x[1])  # Sort by y coordinate
    for i in range(len(strip)):
        for j in range(i + 1, min(i + 8, len(strip))):  # Check next 7 points
            d = dist(strip[i], strip[j])
            if d < min_dist:
                min_dist = d
                closest_pair = (strip[i], strip[j])
    return closest_pair, min_dist

def closest_pair(points):
    def closest_pair_rec(points_sorted_x):
        n = len(points_sorted_x)
        if n <= 3:
            return brute_force(points_sorted_x)

        mid = n // 2
        mid_point = points_sorted_x[mid]

        left_half = points_sorted_x[:mid]
        right_half = points_sorted_x[mid:]

        (pair_left, dist_left) = closest_pair_rec(left_half)
        (pair_right, dist_right) = closest_pair_rec(right_half)

        if dist_left < dist_right:
            min_pair = pair_left
            min_distance = dist_left
        else:
            min_pair = pair_right
            min_distance = dist_right

        strip = [point for point in points_sorted_x if abs(point[0] - mid_point[0]) < min_distance]
        (pair_strip, dist_strip) = strip_closest(strip, min_distance)

        if dist_strip < min_distance:
            return pair_strip, dist_strip
        else:
            return min_pair, min_distance

    points_sorted_x = sorted(points, key=lambda point: point[0])
    closest_pair, min_distance = closest_pair_rec(points_sorted_x)
    return closest_pair, min_distance

# [11] Define a function farthest_pairs(points) to determine the closest pair in a set of points
def farthest_pairs(points):
    max_distance = 0
    farthest_pair = None
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            distance = dist(points[i], points[j])
            if distance > max_distance:
                max_distance = distance
                farthest_pair = (points[i], points[j])
    return farthest_pair, max_distance

def main():
    points = generate_points(10, -10, 10)
    line = compute_line(points, 0, 1)
    print(line, points)
    draw_points(points, "Assignnent4-unsorted.png")
    sorted_points = sort_points(points)
    draw_points(sorted_points, "Assignment4-sorted.png")
    ch = convex_hull(points)
    draw_points(ch, "Assignment4-ch.png")
    area = compute_area(ch)
    print("The area of the convex hull is", area)
    perimeter = compute_perimeter(ch)
    print("The perimeter of the convex hull is", perimeter)
    is_equable(points)
    closest_points, min_dist = closest_pair(points)
    print(f"The closest pair of points is: {closest_points} with a distance of {min_dist:.2f}")
    farthest_points, max_dist = farthest_pairs(points)
    print(f"The furthest pair of points is: {farthest_points} with a distance of {max_dist:.2f}")

if __name__ == '__main__':
    main()