# Written by Kelvin Addy

# imports the required widgets
import os

from PyQt6.QtWidgets import (QWidget, QPushButton, QRadioButton,
                             QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QGroupBox, QButtonGroup,
                             QCheckBox, QFormLayout, QMessageBox)

from PyQt6.QtGui import QIcon, QRegularExpressionValidator
from PyQt6.QtCore import Qt, QSize, QRegularExpression
from algorithms import Algorithms

basedir = os.path.dirname(__file__)

class Optimization(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Sets up the root window widget"""
        self.optimum_main_hbox = QHBoxLayout()
        self.algorithms = Algorithms()
        self.createLeftSide()
        self.createMiddleSide()
        self.createRightSide()
        self.disableField(self.line_edit_list)
        self.validateFields()

    def createLeftSide(self):
        """Sets up the left side of the optimization window"""
        self.newton_rb = QRadioButton("Newton's Method")
        self.golden_rb = QRadioButton("Golden-Section Search Method")
        self.parabolic_rb = QRadioButton("Parabolic Interpolation Method")

        self.methods_rb_list = [self.newton_rb, self.golden_rb, self.parabolic_rb]

        button_tooltips = []
        for i in range(3):
            buttons = QPushButton()
            buttons.setIcon(QIcon(os.path.join(basedir,"./images/information.png")))
            buttons.setStyleSheet("border-style:solid; border-width:0px")
            buttons.setIconSize(QSize(16, 16))
            button_tooltips.append(buttons)

        # GroupBox for QPushButtons
        optimum_mthds_frm = QFormLayout()
        for button, tip in zip(self.methods_rb_list, button_tooltips):
            optimum_mthds_frm.addRow(button, tip)

        self.methods_btn_grp = QButtonGroup(self)
        for button in self.methods_rb_list:
            self.methods_btn_grp.addButton(button)
        self.methods_btn_grp.buttonClicked.connect(self.enableField)

        # Adds the GroupBoxes to the main optimization window layout
        optimum_mthds_grpbx = QGroupBox("Methods")
        optimum_mthds_grpbx.setObjectName("main")
        optimum_mthds_grpbx.setLayout(optimum_mthds_frm)
        optimum_mthds_grpbx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.optimum_main_hbox.addWidget(optimum_mthds_grpbx)
        self.setLayout(self.optimum_main_hbox)

    def createMiddleSide(self):
        """Sets up the middle section of the optimization window"""

        # Needed QlineEdits
        self.opti_func_edit = QLineEdit()
        self.opti_func_edit.setClearButtonEnabled(True)
        self.opti_func_edit.setPlaceholderText("Enter Function in Python Syntax, Eg: x**2 - 4*x")
        self.opti_tol_edit = QLineEdit()
        self.opti_tol_edit.setClearButtonEnabled(True)

        self.opti_newton_df = QLineEdit()
        self.opti_newton_df.setPlaceholderText("Enter Function's first derivative")
        self.opti_newton_dff = QLineEdit()
        self.opti_newton_dff.setPlaceholderText("Enter Function's Second derivative")
        self.opti_newton_guess = QLineEdit()

        self.opti_golden_a = QLineEdit()
        self.opti_golden_b = QLineEdit()

        self.opti_parabolic_1 = QLineEdit()
        self.opti_parabolic_2 = QLineEdit()
        self.opti_parabolic_3 = QLineEdit()

        self.line_edit_list = [self.opti_func_edit, self.opti_tol_edit,
                               self.opti_newton_dff, self.opti_newton_df,
                               self.opti_newton_guess, self.opti_parabolic_1,
                               self.opti_parabolic_3, self.opti_parabolic_2,
                               self.opti_golden_a, self.opti_golden_b]

        # GroupBox for the QlineEdits
        opti_func_data_frm = QFormLayout()
        opti_func_data_frm.addRow(QLabel("Function:"), self.opti_func_edit)
        opti_func_data_frm.addRow(QLabel("Tolerance:"), self.opti_tol_edit)
        opti_func_data_grpbx = QGroupBox("Function Data")
        opti_func_data_grpbx.setObjectName("main")
        opti_func_data_grpbx.setLayout(opti_func_data_frm)

        opti_newton_frm = QFormLayout()
        opti_newton_frm.addRow(QLabel("f'(x):"), self.opti_newton_df)
        opti_newton_frm.addRow(QLabel("f''(x):"), self.opti_newton_dff)
        opti_newton_frm.addRow(QLabel("Initial guess:"), self.opti_newton_guess)
        opti_newton_grpbx = QGroupBox("Newton's Method")
        opti_newton_grpbx.setObjectName("main")
        opti_newton_grpbx.setLayout(opti_newton_frm)

        opti_golden_frm = QFormLayout()
        opti_golden_frm.addRow(QLabel("a:"), self.opti_golden_a)
        opti_golden_frm.addRow(QLabel("b:"), self.opti_golden_b)
        opti_golden_grpbx = QGroupBox("Golden-Section Search Method")
        opti_golden_grpbx.setObjectName("main")
        opti_golden_grpbx.setLayout(opti_golden_frm)

        opti_parabolic_frm = QFormLayout()
        opti_parabolic_frm.addRow(QLabel("x_1:"), self.opti_parabolic_1)
        opti_parabolic_frm.addRow(QLabel("x_2:"), self.opti_parabolic_2)
        opti_parabolic_frm.addRow(QLabel("x_3:"), self.opti_parabolic_3)
        opti_parabolic_grpbx = QGroupBox("Parabolic Interpolation Method")
        opti_parabolic_grpbx.setObjectName("main")
        opti_parabolic_grpbx.setLayout(opti_parabolic_frm)

        self.solvebtn = QPushButton("Calculate")
        self.solvebtn.clicked.connect(self.solveOptimum)
        self.minima = QCheckBox("Minimum")
        self.minima.setChecked(True)
        self.maxima = QCheckBox("Maximum")

        # layout for button and checkbox
        btn_chkbx_hbox = QHBoxLayout()
        btn_chkbx_hbox.addWidget(self.solvebtn, stretch=1)
        btn_chkbx_hbox.addWidget(self.minima)
        btn_chkbx_hbox.addWidget(self.maxima)

        btn_chkbx_bg = QButtonGroup(self)
        btn_chkbx_bg.addButton(self.minima)
        btn_chkbx_bg.addButton(self.maxima)
        btn_chkbx_bg.buttonClicked.connect(lambda button: self.minima_label.setText(f"{button.text()}:"))

        # layout for all the GroupBox
        grp_bx_vbox = QVBoxLayout()
        grp_bx_vbox.addWidget(opti_func_data_grpbx)
        grp_bx_vbox.addWidget(opti_golden_grpbx)
        grp_bx_vbox.addWidget(opti_parabolic_grpbx)
        grp_bx_vbox.addWidget(opti_newton_grpbx)
        grp_bx_vbox.addLayout(btn_chkbx_hbox)

        # Adds the Groupboxes to the main layout
        self.optimum_main_hbox.addLayout(grp_bx_vbox)
        self.setLayout(self.optimum_main_hbox)

    def createRightSide(self):
        """Sets up the right side of the root window"""
        self.optimum_label = QLabel("")
        self.count_label = QLabel("")
        self.optimum_x = QLabel("")
        self.minima_label = QLabel("Minimum:")

        # GroupBox for QlineEdits
        results_grpbx = QGroupBox("Results")
        results_grpbx.setObjectName("main")
        results_frm = QFormLayout()
        results_frm.addRow(self.minima_label, self.optimum_label)
        results_frm.addRow(QLabel("Occurs at: x ="), self.optimum_x)
        results_frm.addRow(QLabel("Iterations:"), self.count_label)
        results_grpbx.setLayout(results_frm)

        # Adds the groupBoxes to the main layout
        results_vbox = QVBoxLayout()
        results_vbox.addWidget(results_grpbx)
        results_vbox.addStretch()
        self.optimum_main_hbox.addLayout(results_vbox)
        self.setLayout(self.optimum_main_hbox)

    def disableField(self, line_edits):
        """Disables line edits"""
        for field in line_edits[2:]:
            field.setEnabled(False)
            field.setClearButtonEnabled(True)

    def enableField(self, button):
        if button == self.newton_rb:
            self.disableField(self.line_edit_list)
            self.opti_newton_df.setEnabled(True)
            self.opti_newton_guess.setEnabled(True)
            self.opti_newton_dff.setEnabled(True)
        elif button == self.golden_rb:
            self.disableField(self.line_edit_list)
            self.opti_golden_b.setEnabled(True)
            self.opti_golden_a.setEnabled(True)

        elif button == self.parabolic_rb:
            self.disableField(self.line_edit_list)
            self.opti_parabolic_1.setEnabled(True)
            self.opti_parabolic_2.setEnabled(True)
            self.opti_parabolic_3.setEnabled(True)

    def validateFields(self):
        """Allows input of text which match a given pattern"""
        number_regex = QRegularExpression(r"[0-9-]+.?[0-9]+")
        expression_regex = QRegularExpression(r"[\s\w 0-9 /()*+.-]+")

        for i in self.line_edit_list:
            if i in (self.opti_func_edit, self.opti_newton_df, self.opti_newton_dff):
                i.setValidator(QRegularExpressionValidator(QRegularExpression(expression_regex)))
            else:
                i.setValidator(QRegularExpressionValidator(QRegularExpression(number_regex)))

    def getData(self,**kwargs):
        """Gets text inputted in the lineEdits"""
        self.tolerance = float(self.opti_tol_edit.text())
        if self.maxima.isChecked():
            self.function = lambda x: -eval(self.opti_func_edit.text())
        else:
            self.function = lambda x: eval(self.opti_func_edit.text())

        if "newton" in kwargs:
            self.dff = lambda x: eval(self.opti_newton_dff.text())
            self.df = lambda x: eval(self.opti_newton_df.text())
            self.x0 = float(self.opti_newton_guess.text())

        if "golden" in kwargs:
            self.a = float(self.opti_golden_a.text())
            self.b = float(self.opti_golden_b.text())

        if "parabolic" in kwargs:
            self.x1 = float(self.opti_parabolic_1.text())
            self.x2 = float(self.opti_parabolic_2.text())
            self.x3 = float(self.opti_parabolic_3.text())

    def checkForErrors(self, function):
        """Calls a function if no error is found"""
        if not any((self.opti_func_edit.text(), self.opti_tol_edit.text())):
            QMessageBox.warning(self, "Empty Fields",
                                "Tolerance or Function field is empty!",
                                QMessageBox.StandardButton.Ok)
        else:
            function()

    def checkMaxima(self, answer):
        if self.maxima.isChecked():
            self.optimum_label.setText(f"{-self.function(answer)}")
        else:
            self.optimum_label.setText(f"{self.function(answer)}")

    def solveNewton(self):
        if not any((self.opti_newton_df.text(), self.opti_newton_guess.text(), self.opti_newton_dff.text())):
            QMessageBox.warning(self, "Empty Fields",
                                "f'(x),f''(x) or Initial guess field empty",
                                QMessageBox.StandardButton.Ok)
        else:
            self.getData(newton=True)
            answer, count = self.algorithms.newtons_method(self.df, self.dff, self.x0, self.tolerance)
            self.checkMaxima(answer)
            self.count_label.setText(f"{count}")
            self.optimum_x.setText(f"{answer}")

    def solveGolden(self):
        if not any((self.opti_golden_b.text(), self.opti_golden_a.text())):
            QMessageBox.warning(self, "Empty Fields",
                                "a or b field empty!",
                                QMessageBox.StandardButton.Ok)
        else:
            self.getData(golden=True)
            if self.a == self.b:
                QMessageBox.warning(self, "Value Error",
                                    "a or b must not be the same!",
                                    QMessageBox.StandardButton.Ok)

            else:
                answer, count = self.algorithms.golden_section_search(self.function, self.a, self.b, self.tolerance)
                self.checkMaxima(answer)
                self.count_label.setText(f"{count}")
                self.optimum_x.setText(f"{answer}")

    def solveParabolic(self):
        if not any((self.opti_parabolic_2.text(), self.opti_parabolic_1.text(), self.opti_parabolic_3.text())):
            QMessageBox.warning(self, "Empty error",
                                "x_1,x_2 or x_3 field empty",
                                QMessageBox.StandardButton.Ok)
        else:
            self.getData(parabolic=True)
            answer, count = self.algorithms.parabolic_interpolation(self.function, self.x1, self.x2, self.x3,
                                                                    self.tolerance)
            self.checkMaxima(answer)
            self.count_label.setText(f"{count}")
            self.optimum_x.setText(f"{answer}")

    def solveOptimum(self):
        """Returns the computed root of the function"""
        try:
            if self.newton_rb.isChecked():
                    self.checkForErrors(self.solveNewton)
            if self.golden_rb.isChecked():
                    self.checkForErrors(self.solveGolden)
            if self.parabolic_rb.isChecked():
                    self.checkForErrors(self.solveParabolic)

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