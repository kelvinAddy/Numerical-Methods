# Written by Kelvin Addy

# imports the required widgets
import os
from numpy import sin, cos, tan, arange, sqrt
from PyQt6.QtWidgets import (QWidget, QPushButton, QRadioButton,
                             QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QGroupBox, QButtonGroup,
                             QGridLayout, QFormLayout, QMessageBox)

from PyQt6.QtGui import QIcon, QPixmap, QRegularExpressionValidator
from PyQt6.QtCore import Qt, QSize, QRegularExpression
from algorithms import Algorithms

basedir = os.path.dirname(__file__)

class RootSolving(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Sets up the root window widget"""
        self.root_main_hbox = QHBoxLayout()
        self.algorithms = Algorithms()
        self.createLeftSide()
        self.createMiddleSide()
        self.createRightSide()
        self.disableField(self.line_edit_list)
        self.validateFields()

    def createLeftSide(self):
        """Sets up the left side of the root window"""
        self.newton_rb = QRadioButton("Newton-Raphson Method")
        self.secant_rb = QRadioButton("Secant Method")
        self.steph_rb = QRadioButton("Steffenssen's Method")
        self.bisection_rb = QRadioButton("Bisection Method")
        self.false_rb = QRadioButton("False-Position Method")
        self.illinois_rb = QRadioButton("Illinois's Method")

        self.methods_rb_list = [self.newton_rb, self.secant_rb,
                                self.steph_rb, self.bisection_rb,
                                self.false_rb, self.illinois_rb]

        button_tooltips = []
        for i in range(6):
            buttons = QPushButton()
            buttons.setIcon(QIcon(os.path.join(basedir,"./images/information.png")))
            buttons.setStyleSheet("border-style:solid; border-width:0px")
            buttons.setIconSize(QSize(16, 16))
            button_tooltips.append(buttons)

        # GroupBox for QPushButtons
        Closed_mthds_frm = QFormLayout()
        for button, tip in zip(self.methods_rb_list[:3], button_tooltips[:3]):
            Closed_mthds_frm.addRow(button, tip)

        Closed_mthds_grpbx = QGroupBox("Closed Methods")
        Closed_mthds_grpbx.setLayout(Closed_mthds_frm)

        bracketed_mthds_frm = QFormLayout()
        for button, tip in zip(self.methods_rb_list[3:], button_tooltips[3:]):
            bracketed_mthds_frm.addRow(button, tip)

        bracketed_mthd_grpbx = QGroupBox("Bracketing Methods")
        bracketed_mthd_grpbx.setLayout(bracketed_mthds_frm)

        self.methods_btn_grp = QButtonGroup(self)
        for button in self.methods_rb_list:
            self.methods_btn_grp.addButton(button)
        self.methods_btn_grp.buttonClicked.connect(self.enableField)

        methods_grpbx = QGroupBox("Methods")
        methods_grpbx.setObjectName("main")
        methods_grpbx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        methods_vbox = QVBoxLayout()
        methods_vbox.addWidget(Closed_mthds_grpbx)
        methods_vbox.addWidget(bracketed_mthd_grpbx)
        methods_vbox.addStretch()
        methods_grpbx.setLayout(methods_vbox)

        # Adds the GroupBoxes to the main root window layout
        self.root_main_hbox.addWidget(methods_grpbx)
        self.setLayout(self.root_main_hbox)

    def createMiddleSide(self):
        """Sets up the middle section of the root window"""
        # Needed QlineEdits
        self.func_edit = QLineEdit()
        self.func_edit.setClearButtonEnabled(True)
        self.func_edit.setPlaceholderText("Enter Function in Python Syntax, Eg: x**2 - 4*x")
        self.tol_edit = QLineEdit()
        self.tol_edit.setClearButtonEnabled(True)

        self.newton_df = QLineEdit()
        self.newton_df.setPlaceholderText("Enter Function's first derivative")
        self.newton_guess = QLineEdit()

        self.secant_x1 = QLineEdit()
        self.secant_x2 = QLineEdit()

        self.steph_guess = QLineEdit()

        self.bracket_x1 = QLineEdit()
        self.bracket_x2 = QLineEdit()

        self.line_edit_list = [self.func_edit, self.tol_edit, self.newton_guess,
                               self.newton_df, self.steph_guess, self.secant_x1,
                               self.secant_x2, self.bracket_x2, self.bracket_x1]

        # GroupBox for the QlineEdits
        func_data_frm = QFormLayout()
        func_data_frm.addRow(QLabel("Function:"), self.func_edit)
        func_data_frm.addRow(QLabel("Tolerance:"), self.tol_edit)
        func_data_grpbx = QGroupBox("Function Data")
        func_data_grpbx.setObjectName("main")
        func_data_grpbx.setLayout(func_data_frm)

        newton_frm = QFormLayout()
        newton_frm.addRow(QLabel("f(x):"), self.newton_df)
        newton_frm.addRow(QLabel("Initial guess:"), self.newton_guess)
        newton_grpbx = QGroupBox("Newton-Raphson Method")
        newton_grpbx.setLayout(newton_frm)

        secant_frm = QFormLayout()
        secant_frm.addRow(QLabel("x_1:"), self.secant_x1)
        secant_frm.addRow(QLabel("x_2:"), self.secant_x2)
        secant_grpbx = QGroupBox("Secant Method")
        secant_grpbx.setLayout(secant_frm)

        step_frm = QFormLayout()
        step_frm.addRow(QLabel("Initial Guess:"), self.steph_guess)

        step_grpbx = QGroupBox("Steffenssen's Method")
        step_grpbx.setLayout(step_frm)

        Closed_vbox = QVBoxLayout()
        Closed_vbox.addWidget(newton_grpbx)
        Closed_vbox.addWidget(secant_grpbx)
        Closed_vbox.addWidget(step_grpbx)
        Closed_grpbx = QGroupBox("Closed Methods")
        Closed_grpbx.setObjectName("main")
        Closed_grpbx.setLayout(Closed_vbox)

        bracket_frm = QFormLayout()
        bracket_frm.addRow(QLabel("x-lower:"), self.bracket_x1)
        bracket_frm.addRow(QLabel("x-upper:"), self.bracket_x2)
        bracket_grpbx = QGroupBox("Bracketing Methods")
        bracket_grpbx.setObjectName("main")
        bracket_grpbx.setLayout(bracket_frm)

        self.solvebtn = QPushButton("Calculate Root")
        self.solvebtn.clicked.connect(self.solveRoot)

        # layout for all the GroupBox
        grp_bx_vbox = QVBoxLayout()
        grp_bx_vbox.addWidget(func_data_grpbx)
        grp_bx_vbox.addWidget(bracket_grpbx)
        grp_bx_vbox.addWidget(Closed_grpbx)
        grp_bx_vbox.addWidget(self.solvebtn, stretch=1)

        # Adds the Groupboxes to the main layout
        self.root_main_hbox.addLayout(grp_bx_vbox)
        self.setLayout(self.root_main_hbox)

    def createRightSide(self):
        """Sets up the right side of the root window"""
        self.solution_label = QLabel("")
        self.count_label = QLabel("")

        # GroupBox for QlineEdits
        results_grpbx = QGroupBox("Results")
        results_grpbx.setObjectName("main")
        results_frm = QFormLayout()
        results_frm.addRow(QLabel("Root Found:"), self.solution_label)
        results_frm.addRow(QLabel("Iterations:"), self.count_label)
        results_grpbx.setLayout(results_frm)

        # Adds the groupBoxes to the main layout
        results_vbox = QVBoxLayout()
        results_vbox.addWidget(results_grpbx)
        results_vbox.addStretch()
        self.root_main_hbox.addLayout(results_vbox)
        self.setLayout(self.root_main_hbox)

    def disableField(self, line_edits):
        """Disables line edits"""
        for field in line_edits[2:]:
            field.setEnabled(False)
            field.setClearButtonEnabled(True)

    def enableField(self, button):
        if button == self.newton_rb:
            self.disableField(self.line_edit_list)
            self.newton_df.setEnabled(True)
            self.newton_guess.setEnabled(True)

        elif button == self.secant_rb:
            self.disableField(self.line_edit_list)
            self.secant_x2.setEnabled(True)
            self.secant_x1.setEnabled(True)

        elif button == self.steph_rb:
            self.disableField(self.line_edit_list)
            self.steph_guess.setEnabled(True)

        elif button in [self.bisection_rb, self.false_rb, self.illinois_rb]:
            self.disableField(self.line_edit_list)
            self.bracket_x1.setEnabled(True)
            self.bracket_x2.setEnabled(True)

    def validateFields(self):
        """Allows input of text which match a given pattern"""
        regex = QRegularExpression(r"[0-9-]+.?[0-9]+")
        reg = QRegularExpression(r"[\s\w 0-9 /()*+.-]+")

        for i in self.line_edit_list:
            if i == self.func_edit or i == self.newton_df:
                i.setValidator(QRegularExpressionValidator(QRegularExpression(reg)))
            else:
                i.setValidator(QRegularExpressionValidator(QRegularExpression(regex)))

    def getData(self, **kwargs):
        """Gets text inputted in the lineEdits"""
        self.function = lambda x: eval(self.func_edit.text())
        self.tolerance = float(self.tol_edit.text())

        if "newton" in kwargs:
            self.df = lambda x: eval(self.newton_df.text())
            self.x0 = float(self.newton_guess.text())

        if "secant" in kwargs:
            self.x1 = float(self.secant_x1.text())
            self.x2 = float(self.secant_x2.text())

        if "steph" in kwargs:
            self.a = float(self.steph_guess.text())

        if "bracket" in kwargs:
            self.x_u = float(self.bracket_x2.text())
            self.x_l = float(self.bracket_x1.text())

    def checkForEmptyFields(self, function):
        """Calls a function if no error is found"""
        if not all((self.func_edit.text(), self.tol_edit.text())):
            QMessageBox.warning(self, "Empty Fields",
                                "Tolerance or Function field is empty!",
                                QMessageBox.StandardButton.Ok)
        else:
            function()

    def solveBracket(self):
        if not all((self.bracket_x1.text(), self.bracket_x2.text())):
            QMessageBox.warning(self, "Empty Fields",
                                "x-upper or x-lower field empty",
                                QMessageBox.StandardButton.Ok)
        else:
            self.getData(bracket=True)
            if self.function(self.x_l) * self.function(self.x_u) > 0:
                QMessageBox.warning(self, "Value Error",
                                    "Root is not within the interval",
                                    QMessageBox.StandardButton.Ok)
            else:
                if self.bisection_rb.isChecked():
                    answer, count = self.algorithms.bisection_algorithm(self.function, self.x_l, self.x_u,
                                                                        margin=self.tolerance)
                    self.count_label.setText(f"{count}")
                    self.solution_label.setText(f"{answer}")
                
                if self.illinois_rb.isChecked():
                    answer, count = self.algorithms.illinois_algorithm(self.function, self.x_l, self.x_u,
                                                                       margin=self.tolerance)
                    self.count_label.setText(f"{count}")
                    self.solution_label.setText(f"{answer}")
                
                if self.false_rb.isChecked():
                    answer, count = self.algorithms.regula_falsi_algorithm(self.function, self.x_l, self.x_u,
                                                                           margin=self.tolerance)
                    self.count_label.setText(f"{count}")
                    self.solution_label.setText(f"{answer}")

    def solveNewton(self):
        if not all((self.newton_df.text(), self.newton_guess.text())):
            QMessageBox.warning(self, "Empty Fields",
                                "f'(x) or Initial guess field empty",
                                QMessageBox.StandardButton.Ok)
        else:
            self.getData(newton=True)
            answer, count = self.algorithms.newton_raphson(self.function, self.df, self.x0, self.tolerance)
            self.count_label.setText(f"{count}")
            self.solution_label.setText(f"{answer}")

    def solveSecant(self):
        if not all((self.secant_x2.text(), self.secant_x1.text())):
            QMessageBox.warning(self, "Empty Fields",
                                "x_1 or x_2 field empty!",
                                QMessageBox.StandardButton.Ok)
        else:
            self.getData(secant=True)
            if self.x1 == self.x2 or (-self.x1 == self.x2):
                QMessageBox.warning(self, "Value Error",
                                    "x_1 or x_2 must not be the same!",
                                    QMessageBox.StandardButton.Ok)

            else:
                answer, count = self.algorithms.secant_algorithm(self.function, self.x1, self.x2, self.tolerance)
                self.count_label.setText(f"{count}")
                self.solution_label.setText(f"{answer}")

    def solveSteph(self):
        if self.steph_guess.text() == "":
            QMessageBox.warning(self, "Value error",
                                "Initial guess field empty",
                                QMessageBox.StandardButton.Ok)
        else:
            self.getData(steph=True)
            if self.a == 0:
                QMessageBox.warning(self, "Division by zero error",
                                    "Initial guess cannot be zero",
                                    QMessageBox.StandardButton.Ok)
            else:
                answer, count = self.algorithms.steffensen_algorithm(self.function, self.a, self.tolerance)
                self.count_label.setText(f"{count}")
                self.solution_label.setText(f"{answer}")

    def solveRoot(self):
        """Returns the computed root of the function"""
        try:
            if self.newton_rb.isChecked():
                self.checkForErrors(self.solveNewton)
            if self.secant_rb.isChecked():
                self.checkForErrors(self.solveSecant)
            if self.steph_rb.isChecked():
                self.checkForErrors(self.solveSteph)
            if any((self.bisection_rb.isChecked(), self.illinois_rb.isChecked(), self.false_rb.isChecked())):
                self.checkForErrors(self.solveBracket)

        except SyntaxError as error:
            QMessageBox.warning(self, "Syntax Error",
                                f"{error}", QMessageBox.StandardButton.Ok)
        except TypeError as error:
            QMessageBox.warning(self, "Type Error",
                                f"{error}", QMessageBox.StandardButton.Ok)
        except ValueError as error:
            QMessageBox.warning(self, "Value Error",
                                f"{error}", QMessageBox.StandardButton.Ok)
        except RuntimeError as error:
            QMessageBox.warning(self, "Runtime Error",
                                f"{error}", QMessageBox.StandardButton.Ok)
        except OverflowError as error:
            QMessageBox.warning(self, "Overflow Error",
                                f"{error}", QMessageBox.StandardButton.Ok)
        except ZeroDivisionError as error:
            QMessageBox.warning(self, "Division by zero Error",
                                f"{error}", QMessageBox.StandardButton.Ok)
        except NameError as error:
            QMessageBox.warning(self, "Name Error",
                                f"{error}", QMessageBox.StandardButton.Ok)