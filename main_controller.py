#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from PyQt4 import QtGui, QtCore
from basic_gui.main_view import View
from settings.settings import *
import sys


class Controller(View):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.updatePlot()

        self.resetButton.clicked.connect(self.resetValues)
        self.paramtSlider.valueChanged.connect(self.sliderchanged)
        self.curveCheckBox.clicked.connect(self.curveCheckBoxChanged)
        self.polygonCheckBox.clicked.connect(self.polygonCheckBoxChanged)
        self.sublinesCheckBox.clicked.connect(self.sublinesCheckBoxChanged)
        self.paramtSpinbox.valueChanged.connect(self.paramtSpinboxchanged)

    def deleteLastPoint(self):
        self.canvas.deleteLastPoint()

    def paramTChanged(self):
        self.paramtLineEdit.setText(CURRENT_LINEEDIT % self._t)
        self.paramtSlider.setValue(int(self._t * 100.0))
        self.paramtSpinbox.setValue(self._t)
        self.updatePlot()

    def sublinesCheckBoxChanged(self):
        self.canvas.setSubFlag(self.sublinesCheckBox.isChecked())
        self.updatePlot()

    def curveCheckBoxChanged(self):
        self.canvas.setCurveFlag(self.curveCheckBox.isChecked())
        self.updatePlot()

    def polygonCheckBoxChanged(self):
        self.canvas.setPolygonFlag(self.polygonCheckBox.isChecked())
        self.updatePlot()

    def sliderchanged(self):
        self._t = self.paramtSlider.value() / 100.
        self.paramTChanged()

    def paramtSpinboxchanged(self):
        self._t = self.paramtSpinbox.value()
        self.paramTChanged()

    def resetValues(self):
        self.paramtSlider.setValue(int(self._t0 * 100.0))
        self.paramtLineEdit.setText(RESET_LINEEDIT % self._t0)
        self.paramtSpinbox.setValue(self._t0)
        self.curveCheckBox.setChecked(CURVE_CHECKBOX_BOOL)
        self.polygonCheckBox.setChecked(POLYGON_CHECKBOX_BOOL)
        self.sublinesCheckBox.setChecked(SUBLINES_CHECKBOX_BOOL)
        self.canvas.resetCanvas()
        self.updatePlot()

    def updatePlot(self):
        self.canvas.updatePlot(self._t)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = Controller()
    main.setWindowTitle("%s %s" % (PROGRAM_NAME, VERSION))
    main.show()
    sys.exit(app.exec_())
