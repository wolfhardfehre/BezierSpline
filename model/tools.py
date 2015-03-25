#!/usr/local/bin/python
# coding: utf-8

import numpy as np
import timeit


class Point():
    """Point class for testing puposes"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.p = np.array([x, y])

    def __mul__(self, other):
        return other * self.p

    def __rmul__(self, other):
        return other * self.p

    def __add__(self, other):
        print isinstance(other, np.array)
        return self.p + other

    def __str__(self):
        return "(%6.3f, %6.3f)" % (self.x, self.y)


def binCoeff(n, k):
    """Binomial coefficient"""
    if k == 0:
        return 1
    if 2 * k > n:
        result = binCoeff(n, n - k)
    else:
        result = n - k + 1
        for i in range(2, k + 1):
            result *= (n - k + i)
            result /= i
    return result


def bernstein(t, k, n):
    return binCoeff(n, k) * t**k * (1 - t)**(n - k)


def bezier(t0, points, n):
    sum = np.array([0.0, 0.0])
    for k, point in enumerate(points):
        bern = bernstein(t0, k, n)
        sum += bern * point
    return sum


def deCasteljau(t0, points, n):
    ply = points[:]
    for j in range(n):
        for i in range(n-j):
            ply[i] = (1 - t0) * ply[i] + t0 * ply[i + 1]
    return ply[0]


def createBezierSpline(t_max, points):
    """Bezier spline"""
    ts = np.arange(0.0, t_max + 0.01, 0.01)
    n = len(points) - 1
    xs = []
    ys = []
    for t in ts:
        x, y = bezier(t, points, n)
        xs.append(x)
        ys.append(y)
    return xs, ys


def createSublines(t_max, pts_x, pts_y):
    sub_x = []
    sub_y = []
    while len(pts_x) > 2:
        pts_x = (1 - t_max) * pts_x[:-1] + t_max * pts_x[1:]
        pts_y = (1 - t_max) * pts_y[:-1] + t_max * pts_y[1:]
        sub_x.append(pts_x)
        sub_y.append(pts_y)
    return sub_x, sub_y

# PARAMS ##################################
T_MAX = 0.6
'''
POINTS = [Point(0.0, 0.0), Point(25.0, 50.0),
          Point(50.0, 0.0), Point(-50.0, -25.0)]
'''
POINTS = [Point(0.0, 0.0), Point(1.0, 1.0),
          Point(2.0, 2.0), Point(3.0, 3.0),
          Point(4.0, 4.0), Point(5.0, 5.0),
          Point(6.0, 6.0), Point(7.0, 7.0),
          Point(8.0, 8.0), Point(9.0, 9.0),
          Point(10.0, 10.0), Point(11.0, 11.0),
          Point(12.0, 10.0), Point(13.0, 9.0),
          Point(14.0, 8.0), Point(15.0, 7.0),
          Point(16.0, 6.0), Point(17.0, 5.0),
          Point(18.0, 4.0), Point(19.0, 3.0),
          Point(20.0, 2.0), Point(21.0, 1.0),
          Point(22.0, 0.0), Point(23.0, -1.0),
          Point(24.0, -2.0), Point(25.0, -3.0),
          Point(26.0, -4.0), Point(27.0, -5.0),
          Point(28.0, -6.0), Point(29.0, -7.0),
          Point(30.0, -8.0), Point(31.0, -9.0)]

N = len(POINTS) - 1
###########################################

if __name__ == '__main__':

    print "x = %6.3f, y = %6.3f" % tuple(bezier(T_MAX, POINTS, N))
    print "x = %6.3f, y = %6.3f" % tuple(deCasteljau(T_MAX, POINTS, N))
    print "deCasteljau: %7.4f s" % timeit.timeit('deCasteljau(T_MAX, POINTS, N)',
                                                 setup='from tools import deCasteljau, T_MAX, POINTS, N',
                                                 number=1000)
    print "     bezier: %7.4f s" % timeit.timeit('bezier(T_MAX, POINTS, N)',
                                                 setup='from tools import bezier, T_MAX, POINTS, N',
                                                 number=1000)
