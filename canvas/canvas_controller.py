#!/usr/local/bin/python
# coding: utf-8

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigCanvas
from matplotlib import colors
from PyQt4 import QtCore
from elements_view import *
import matplotlib.pyplot as plt
import numpy as np
from model import tools
import six


colrs = list(six.iteritems(colors.cnames))


class AbstractMplCanvas(FigCanvas):

    def __init__(self, base=1.1):
        self.fig = plt.figure()
        FigCanvas.__init__(self, self.fig)
        self.base = base
        self.setAxes()

    def setAxes(self):
        self.ax = plt.Axes(plt.gcf(), [0, 0, 1, 1])
        plt.gcf().add_axes(self.ax)
        plt.xlim([0, 1000])
        plt.ylim([0, 1000])
        self.ax.grid()
        self.activateMovement()

    def activateMovement(self):
        Zoomable(self, self.ax, self.base).setUp()
        Pannable(self, self.ax).setUp()


class MplCanvas(AbstractMplCanvas):

    def __init__(self, stat, t_max, base=1.1):
        AbstractMplCanvas.__init__(self, base)
        self.polygonFlag = False
        self.curveFlag = False
        self.subFlag = False
        self.drawFlag = True
        self.points = []
        self.t_max = t_max
        self.stat = stat

        self.mpl_connect('motion_notify_event', self.onMotion)
        self.mpl_connect('pick_event', self.onPick)
        self.mpl_connect('button_press_event', self.setPoint)
        self.mpl_connect('button_release_event', self.onRelease)

    def onMotion(self, event):
        x, y = event.xdata, event.ydata
        if not x or not y:
            return
        text = QtCore.QString("x=%5.2f, y=%5.2f" % (x, y))
        self.stat.showMessage(text, 0)
        if event.button == 1 and not self.drawFlag:
            self.element.set_data(x, y)
            self.element.second.set_data(x, y)
            self.element.clazz.x = x
            self.element.clazz.y = y
            self.updatePlot(self.t_max)

    def onPick(self, event):
        self.drawFlag = False
        self.element = event.artist

    def setPoint(self, event):
        if self.drawFlag:
            pt = MplPoint(self.ax, event.xdata,
                          event.ydata, 'o', '0.5', 10, 0.5, True)
            self.points.append(pt)
            self.updatePlot(self.t_max)

    def setPointsFromFile(self, t, points):
        self.t_max = t
        self.points = []
        for pt in points:
            p = MplPoint(self.ax, pt[0], pt[1],
                         'o', '0.5', 10, 0.5, True)
            self.points.append(p)
        self.updatePlot(self.t_max)

    def onRelease(self, event):
        self.drawFlag = True

    def resetCanvas(self):
        self.deleteElements()
        self.deletePoints()

    def deleteElements(self):
        if hasattr(self, "elements"):
            for idx, el in enumerate(self.elements):
                el.remove()
            self.elements = []

    def deletePoints(self):
        for pt in self.points:
            pt.remove()
        self.points = []

    def deleteLastPoint(self):
        if hasattr(self, 'points'):
            if len(self.points) > 0:
                self.points[-1].remove()
                del self.points[-1]
                self.updatePlot(self.t_max)

    def updatePlot(self, t_max):
        self.deleteElements()
        self.elements = []
        self.t_max = t_max
        points_x = np.array([p.x for p in self.points])
        points_y = np.array([p.y for p in self.points])
        if self.curveFlag:
            self.buildBezierSpline()
        if self.polygonFlag:
            self.buildPolygon()
        if self.subFlag:
            self.buildSublines(points_x, points_y)
        self.draw()

    def buildBezierSpline(self):
        x, y = tools.createBezierSpline(self.t_max, self.points)
        scatters = tools.getScatters(self.t_max, self.points)
        for idx, point in enumerate(self.points):
            self.elements.append(
                MplCircle(self.ax, point.x, point.y, scatters[idx]))
            self.elements.append(
                MplText(self.ax, point.x, point.y, scatters[idx]))
        self.elements.append(MplCurveBezier(self.ax, x, y))
        self.elements.append(MplPoint(self.ax, x[-1], y[-1], 'o', 'red'))

    def buildPolygon(self):
        self.elements.append(MplLine(self.ax, self.points, '-', '0.5', 5))

    def buildSublines(self, points_x, points_y):
        sub_x, sub_y = tools.createSublines(self.t_max, points_x, points_y)
        sub_size = len(sub_x)
        for idx in range(sub_size):
            pts = []
            for jdx in range(len(sub_x[idx])):
                pt = MplPoint(self.ax, sub_x[idx][jdx],
                              sub_y[idx][jdx], 'o', colrs[idx][0])
                pts.append(pt)
            self.elements.extend(pts)
            self.elements.append(MplLine(self.ax, pts, '-', colrs[idx][0]))

    def setCurveFlag(self, flag):
        self.curveFlag = flag

    def setPolygonFlag(self, flag):
        self.polygonFlag = flag

    def setSubFlag(self, flag):
        self.subFlag = flag


class Zoomable(object):

    def __init__(self, canvas, ax, base=1.1):
        self.xmin = ax.get_xlim()
        self.ymin = ax.get_ylim()
        self.base = base
        self.ax = ax
        self.canvas = canvas

    def setUp(self):

        def onScroll(event):
            print event.button
            if event.button == 'down' or event.button == '-':
                self.scale = 1 / self.base
            elif event.button == 'up' or event.button == '+':
                self.scale = self.base
            else:
                self.scale = 1
            self.zoom(event)

        self.canvas.mpl_connect('scroll_event', onScroll)
        self.canvas.mpl_connect('key_press_event', onScroll)

    def zoom(self, event):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        x = int(event.xdata)
        y = int(event.ydata)

        w = (xlim[1] - xlim[0]) * self.scale
        h = (ylim[1] - ylim[0]) * self.scale

        xrel = (xlim[1] - x) / (xlim[1] - xlim[0])
        yrel = (ylim[1] - y) / (ylim[1] - ylim[0])

        self.ax.set_xlim([x - w * (1 - xrel), x + w * xrel])
        self.ax.set_ylim([y - h * (1 - yrel), y + h * yrel])
        self.canvas.draw()


class Pannable(object):

    def __init__(self, canvas, ax):
        self.xmin = ax.get_xlim()
        self.ymin = ax.get_ylim()
        self.canvas = canvas
        self.ax = ax
        self.xpress = None

    def setUp(self):

        def onPress(event):
            if event.inaxes is None:
                return
            if event.inaxes != self.ax:
                return

            if event.button == 3:
                self.xpress = event.xdata
                self.ypress = event.ydata

        def onRelease(event):
            self.xpress = None

        def onMotion(event):
            if event.inaxes is None:
                return
            if self.xpress is None:
                return

            x = event.xdata
            y = event.ydata
            xlim = np.array(self.ax.get_xlim())
            ylim = np.array(self.ax.get_ylim())

            if event.button == 3:
                dx = x - self.xpress
                dy = y - self.ypress
                xlim -= dx
                ylim -= dy
                self.ax.set_xlim(xlim)
                self.ax.set_ylim(ylim)

            self.canvas.draw()

        self.canvas.mpl_connect('button_press_event', onPress)
        self.canvas.mpl_connect('button_release_event', onRelease)
        self.canvas.mpl_connect('motion_notify_event', onMotion)
