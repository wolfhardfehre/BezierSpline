#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# MAIN SETTINGS ######################################################
PROGRAM_NAME = u'<< Bézier | Spline >>'
VERSION = u'0.1.0'

ABOUT_TEXT = u"""<< Bézier | Spline >>
Copyleft (ɔ) 2015, Hehl & Fehre

Dieses Programm präsenentiert die interaktive Darstellung eines
Bézier-Splines. Mit der linken Maustaste können Punkte gesetzt werden.
Weiterhin kann über die verschiedenen Checkboxen der Spline, das
Polygon oder die Hilfslinien angezeigt werden.

Das Programm kann ohne Restriktionen genutzt oder modifiziert werden.
Sowohl Rohkopien als auch modifizierte Versionen können ohne
Limitierung verbreitet werden."""

# BASIC PARAMETERS ###################################################
T0_PARAMETER = 1.0

STEP_SPINBOX = 0.05
STEP_SLIDER = 2
TICKS_SLIDER = 10

HEIGHT_WINDOWSIZE = 600
WIDTH_WINDOWSIZE = 800

# MENUBAR TEXT #######################################################
EDIT_MENUBAR = u'&Editieren'
HELP_MENUBAR = u'&Hilfe'

# ACTION TEXT ########################################################
CLOSE_ACTION = u'&Programm schließen'
NEW_ACTION = u'&Paramter zurücksetzen '
OPEN_ACTION = u'&Lade Punkte'
SAVE_ACTION = u'&Speichere Punkte'
DELETE_ACTION = u'&Letzten Punkt löschen'
HELP_ACTION = u'&Beschreibung'

# BUTTON TEXT ########################################################
RESET_BUTTON = u'Parameter zurücksetzen'

# CHECKBOX ###########################################################
CURVE_CHECKBOX_TEXT = u'Kurve plotten'
POLYGON_CHECKBOX_TEXT = u'Polygon plotten'
SUBLINES_CHECKBOX_TEXT = u'Subpolygone plotten'

CURVE_CHECKBOX_BOOL = False
POLYGON_CHECKBOX_BOOL = False
SUBLINES_CHECKBOX_BOOL = False

# LINEEDIT TEXT ######################################################
CURRENT_LINEEDIT = u'aktuell: t = %.2f'
RESET_LINEEDIT = u'reset: t = %.2f'

# FILEDIALOG TEXT ####################################################
OPEN_FILEDIALOG = u'Datei öffnen'
SAVE_FILEDIALOG = u'Datei speichern'
DEFAULT_FILENAME = u'untitled'
FILE_FROMAT = u'*.bezier'
