#!/usr/local/bin/python
# coding: utf-8

import numpy as np


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
    ply = np.array(points)
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


if __name__ == '__main__':
    # PARAMS ##################################
    T_MAX = 0.6
    POINTS = [Point(0.0, 0.0), Point(25.0, 50.0),
              Point(50.0, 0.0), Point(-50.0, -25.0)]
    N = len(POINTS) - 1
    ###########################################
    xs, ys = createBezierSpline(T_MAX, POINTS)
    print xs[-1], ys[-1]

    print bezier(T_MAX, POINTS, N)
    print deCasteljau(T_MAX, POINTS, N)
