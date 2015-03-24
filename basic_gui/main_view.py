#!/usr/local/bin/python
# coding: utf-8

from PyQt4 import QtCore, QtGui
from canvas.canvas_controller import MplCanvas
from settings.settings import *
import ast
import csv


class View(QtGui.QMainWindow):

    def setupUi(self, dialog):
        self._t0 = T0_PARAMETER
        self._t = self._t0

        self.setMinimumSize(WIDTH_WINDOWSIZE, HEIGHT_WINDOWSIZE)

        # MENU Bar
        self.file_menu = QtGui.QMenu(EDIT_MENUBAR, self)
        self.file_menu.addAction(
            CLOSE_ACTION, self.fileQuit, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.file_menu.addAction(
            NEW_ACTION, self.resetValues, QtCore.Qt.CTRL + QtCore.Qt.Key_N)
        self.file_menu.addAction(
            OPEN_ACTION, self.openFile, QtCore.Qt.CTRL + QtCore.Qt.Key_L)
        self.file_menu.addAction(
            SAVE_ACTION, self.saveFile, QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.file_menu.addAction(
            DELETE_ACTION, self.deleteLastPoint,
            QtCore.Qt.CTRL + QtCore.Qt.Key_Z)

        self.menuBar().addMenu(self.file_menu)
        self.help_menu = QtGui.QMenu(HELP_MENUBAR, self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)
        self.help_menu.addAction(HELP_ACTION, self.about)

        # Statusbar
        self.stat = self.statusBar()

        # Create main widget and create main and sub layouts
        self.main_widget = QtGui.QWidget(dialog)
        main_layout = QtGui.QVBoxLayout(self.main_widget)
        h1_layout = QtGui.QHBoxLayout()
        h2_layout = QtGui.QHBoxLayout()

        # Implement matplotlib (mpl) canvas
        self.canvas = MplCanvas(self.stat, self._t0)

        # Set sub layouts and mpl-canvas to main layout
        main_layout.addWidget(self.canvas)
        main_layout.addLayout(h1_layout)
        main_layout.addLayout(h2_layout)

        # LineEdit
        self.paramtLineEdit = QtGui.QLineEdit()
        self.paramtLineEdit.setReadOnly(True)
        self.paramtLineEdit.setText(CURRENT_LINEEDIT % self._t0)

        # Spinbox
        self.paramtSpinbox = QtGui.QDoubleSpinBox()
        self.paramtSpinbox.setMaximum(1.0)
        self.paramtSpinbox.setSingleStep(STEP_SPINBOX)
        self.paramtSpinbox.setValue(self._t0)

        # Slider
        self.paramtSlider = QtGui.QSlider()
        self.paramtSlider.setMaximum(100)
        self.paramtSlider.setSingleStep(STEP_SLIDER)
        self.paramtSlider.setSliderPosition(int(100 * self._t0))
        self.paramtSlider.setOrientation(QtCore.Qt.Horizontal)
        self.paramtSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.paramtSlider.setTickInterval(TICKS_SLIDER)

        # ResetButton
        self.resetButton = QtGui.QPushButton(
            QtCore.QString(RESET_BUTTON))

        # CheckBoxes
        self.curveCheckBox = QtGui.QCheckBox(
            QtCore.QString(CURVE_CHECKBOX_TEXT))
        self.polygonCheckBox = QtGui.QCheckBox(
            QtCore.QString(POLYGON_CHECKBOX_TEXT))
        self.sublinesCheckBox = QtGui.QCheckBox(
            QtCore.QString(SUBLINES_CHECKBOX_TEXT))

        self.curveCheckBox.setChecked(CURVE_CHECKBOX_BOOL)
        self.polygonCheckBox.setChecked(POLYGON_CHECKBOX_BOOL)
        self.sublinesCheckBox.setChecked(SUBLINES_CHECKBOX_BOOL)

        # Add Widgets to specific layouts
        h1_layout.addWidget(self.paramtLineEdit)
        h1_layout.addWidget(self.paramtSpinbox)
        h1_layout.addWidget(self.paramtSlider)

        h2_layout.addWidget(self.resetButton)
        h2_layout.addWidget(self.curveCheckBox)
        h2_layout.addWidget(self.polygonCheckBox)
        h2_layout.addWidget(self.sublinesCheckBox)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def openFile(self):
        filename = str(QtGui.QFileDialog.getOpenFileName(
            self, OPEN_FILEDIALOG, '', FILE_FROMAT))
        if filename != '':
            points = []
            with open(filename, 'rb') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                for idx, row in enumerate(reader):
                    if idx == 0:
                        self._t = float(row[0])
                        self.paramTChanged()
                    else:
                        points.append(ast.literal_eval(row[0]))
            self.canvas.setPointsFromFile(self._t, points)

    def saveFile(self):
        filename = str(QtGui.QFileDialog.getSaveFileName(
            self, SAVE_FILEDIALOG, DEFAULT_FILENAME, FILE_FROMAT))
        if filename.split('.')[-1] == FILE_FROMAT.split('.')[-1]:
            out = [str(self._t)]
            op = [str((p.x, p.y)) for p in self.canvas.points]
            out.extend(op)
            with open(filename, 'wb') as f:
                f.write('\n'.join(out))

    def fileQuit(self):
        self.close()

    def about(self):
        QtGui.QMessageBox.about(self, HELP_ACTION, ABOUT_TEXT)
