#!/usr/local/bin/python
# coding: utf-8

import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def binCoeff(n, k):
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


def createBezierSpline(t_max, points):
    ts = np.arange(0.0, t_max + 0.01, 0.01)
    n = len(points) - 1
    all_xs = []
    all_ys = []
    for t in ts:
        sum_x = 0.0
        sum_y = 0.0
        for k, point in enumerate(points):
            bc = binCoeff(n, k)
            fac1 = t**k
            fac2 = (1 - t)**(n - k)
            factor = bc * fac1 * fac2
            sum_x += factor * point.x
            sum_y += factor * point.y
        all_xs.append(sum_x)
        all_ys.append(sum_y)
    return all_xs, all_ys


def createSublines(t_max, pts_x, pts_y):
    sublines_x = []
    sublines_y = []
    while len(pts_x) > 2:
        pts_x = (1 - t_max) * pts_x[:-1] + t_max * pts_x[1:]
        pts_y = (1 - t_max) * pts_y[:-1] + t_max * pts_y[1:]
        sublines_x.append(pts_x)
        sublines_y.append(pts_y)
    return sublines_x, sublines_y


if __name__ == '__main__':
    # PARAMS ##################################
    T_MAX = .6
    POINTS = [Point(0.0, 0.0), Point(25.0, 30.0),
              Point(50.0, 0.0), Point(-50.0, -25.0)]
    ###########################################
    xs, ys = createBezierSpline(T_MAX, POINTS)
    print xs[-1], ys[-1]
