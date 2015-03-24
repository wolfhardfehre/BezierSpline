#!/usr/local/bin/python
# coding: utf-8

from PyQt4 import QtGui


class MplDrawables(object):

    def __init__(self, canvas, ax, sign="o", col="black", width=5, alpha=0.8):
        self.canvas = canvas
        self.ax = ax
        self.col = col
        self.width = width
        self.sign = sign
        self.alpha = alpha

    def remove(self):
        self.element.remove()


class MplPoint(MplDrawables):

    def __init__(self, canvas, ax, x, y, sign="o", col="black", width=5, alpha=0.8, prim=False):
        MplDrawables.__init__(self, canvas, ax, sign, col, width, alpha)
        self.moveFlag = False
        self.x = x
        self.y = y
        self.prim = prim
        self.drawElement()

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
                                    ms=self.width*2.0,
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

    def __init__(self, canvas, ax, pts, sign="-", col="black", width=2, alpha=0.8):
        MplDrawables.__init__(self, canvas, ax, sign, col, width, alpha)
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

    def __init__(self, canvas, ax, x, y, sign="-", col="red", width=5, alpha=0.8):
        MplDrawables.__init__(self, canvas, ax, sign, col, width, alpha)
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
