#!/usr/local/bin/python
# coding: utf-8


from PyQt4 import QtGui
import numpy as np


class MplDrawables(object):

    def __init__(self, ax, sign="o", col="black", width=5, alpha=0.8):
        self.ax = ax
        self.col = col
        self.width = width
        self.sign = sign
        self.alpha = alpha

    def remove(self):
        self.element.remove()


class MplPoint(MplDrawables):

    def __init__(self, ax, x, y, sign="o", col="black", width=5, alpha=0.8, prim=False):
        MplDrawables.__init__(self, ax, sign, col, width, alpha)
        self.moveFlag = False
        self.x = x
        self.y = y
        self.prim = prim
        self.drawElement()
        self.p = np.array([x, y])

    def __mul__(self, other):
        return other * self.p

    def __rmul__(self, other):
        return other * self.p

    def __add__(self, other):
        print isinstance(other, np.array)
        return self.p + other

    def remove(self):
        self.element.remove()
        if self.prim:
            self.element2.remove()

    def drawElement(self):
        if self.prim:
            self.element = self.ax.plot(self.x,
                                        self.y,
                                        self.sign,
                                        picker=5,
                                        ms=self.width,
                                        color=self.col,
                                        alpha=self.alpha).pop(0)
            self.element2 = self.ax.plot(self.x,
                                         self.y,
                                         "+",
                                         ms=self.width * 2.0,
                                         mew=2,
                                         color='0.1',
                                         alpha=self.alpha).pop(0)
            self.element.second = self.element2
        else:
            self.element = self.ax.plot(self.x,
                                        self.y,
                                        self.sign,
                                        ms=self.width,
                                        color=self.col,
                                        alpha=self.alpha).pop(0)
        self.element.clazz = self

    def getCoords(self):
        if not hasattr(self, 'element'):
            QtGui.QMessageBox.about(QtGui.QWidget(),
                                    "Zero Point Error",
                                    "Please Set A Zero Point\n\
                                    Before Calculate The Model")
            return self.x, self.y


class MplLine(MplDrawables):

    def __init__(self, ax, pts, sign="-", col="black", width=2, alpha=0.8):
        MplDrawables.__init__(self, ax, sign, col, width, alpha)
        self.pts = pts
        self.pts_x = [pt.x for pt in pts]
        self.pts_y = [pt.y for pt in pts]
        self.drawElement()

    def drawElement(self):
        self.element = self.ax.plot(self.pts_x,
                                    self.pts_y,
                                    self.sign,
                                    lw=self.width,
                                    color=self.col,
                                    alpha=self.alpha).pop(0)

    def getCoords(self):
        return self.pts


class MplCurveBezier(MplDrawables):

    def __init__(self, ax, x, y, sign="-", col="red", width=5, alpha=0.8):
        MplDrawables.__init__(self, ax, sign, col, width, alpha)
        self.x = x
        self.y = y
        self.drawElement()

    def drawElement(self):
        self.element = self.ax.plot(self.x,
                                    self.y,
                                    self.sign,
                                    lw=self.width,
                                    color=self.col,
                                    alpha=self.alpha).pop(0)


class MplCircle(MplDrawables):

    def __init__(self, ax, x, y, radius, alpha=0.4):
        MplDrawables.__init__(self, ax, alpha=alpha)
        self.x = x
        self.y = y
        if radius < 0.33:
            self.col = 'green'
        elif radius < 0.66:
            self.col = 'yellow'
        else:
            self.col = 'red'
        self.radius = radius * 10000
        self.drawElement()

    def drawElement(self):
        self.element = self.ax.scatter(
            self.x, self.y, self.radius, c=self.col, alpha=self.alpha)


class MplText(MplDrawables):

    def __init__(self, ax, x, y, radius, alpha=0.8):
        MplDrawables.__init__(self, ax, alpha=alpha)
        self.x = x - 13
        self.y = y + 25
        self.radius = "%.1f" % radius
        self.drawElement()

    def drawElement(self):
        self.element = self.ax.text(self.x, self.y, self.radius,
                                    color="black", alpha=self.alpha,
                                    fontsize=15, fontweight='bold')
