# Written by Kelvin Addy

# imports the required widgets
import os

from PyQt6.QtWidgets import (QWidget, QPushButton, QRadioButton,
                             QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QGroupBox, QButtonGroup,
                             QCheckBox, QFormLayout, QMessageBox,
                             QTableWidget)

from PyQt6.QtGui import QIcon, QRegularExpressionValidator
from PyQt6.QtCore import Qt, QSize, QRegularExpression
from algorithms import Algorithms

basedir = os.path.dirname(__file__)

class Integration(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        """Sets up the integration window"""
        self.setUpMainWindow()
    
    def setUpMainWindow(self):
        """Creates and arranges widgets in the integration window"""
        # Creates radiobuttons for integration methods
        self.simps3rd_rb = QRadioButton("Simpsons 1/3")
        self.simp8th_rb = QRadioButton("Simpsons 3/8")
        self.trapezium_rb = QRadioButton("Trapezium")
        self.montecarlo_rb = QRadioButton("Monte Carlo")

        self.methods_rb_list = [self.simp8th_rb, self.simps3rd_rb, self.trapezium_rb, self.montecarlo_rb]

        button_tooltips = []
        for _ in range(4):
            buttons = QPushButton()
            buttons.setIcon(QIcon(os.path.join(basedir,"./images/information.png")))
            buttons.setStyleSheet("border-style:solid; border-width:0px")
            buttons.setIconSize(QSize(16, 16))
            button_tooltips.append(buttons)

        # QFormLayout for radiobuttons and button_tooltips
        integral_mthds_frm = QFormLayout()
        for button, tip in zip(self.methods_rb_list, button_tooltips):
            integral_mthds_frm.addRow(button, tip)

        # Adds the radiobuttons to a buttongroup
        self.methods_btn_grp = QButtonGroup(self)
        
        for button in self.methods_rb_list:
            self.methods_btn_grp.addButton(button)
        #self.methods_btn_grp.buttonClicked.connect(self.enableField)

        # Sets the QFormLayout to a groupbox
        integral_mthds_grpbx = QGroupBox("Methods")
        integral_mthds_grpbx.setObjectName("main")
        integral_mthds_grpbx.setLayout(integral_mthds_frm)
        integral_mthds_grpbx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.integral_main_hbox = QHBoxLayout()
        self.integral_main_hbox.addWidget(integral_mthds_grpbx)
        self.setLayout(self.integral_main_hbox)
        
        # Creates QlineEdits needed to retrieve function data
        self.func_edit = QLineEdit()
        self.func_edit.setPlaceholderText("Enter Function in python syntax. Eg: x**2 - 4*x")
        self.func_edit.setClearButtonEnabled(True)

        self.upper_limit = QLineEdit()
        self.upper_limit.setClearButtonEnabled(True)

        self.lower_limit = QLineEdit()
        self.lower_limit.setClearButtonEnabled(True)

        self.intervals = QLineEdit()
        self.intervals.setPlaceholderText("Enter number of intervals")
        self.intervals.setClearButtonEnabled(True)

        # QFormlayout containing a label and corresponding QlineEdit
        func_data_form = QFormLayout()
        func_data_form.addRow(QLabel("Function:"), self.func_edit)
        func_data_form.addRow(QLabel("Intervals:"), self.intervals)
        func_data_form.addRow(QLabel("Upper-limit:"), self.upper_limit)
        func_data_form.addRow(QLabel("Lower-limit:"), self.lower_limit)

        # Sets the func_data_form to a groupbox
        func_data_grpbox = QGroupBox("Function Data")
        func_data_grpbox.setLayout(func_data_form)
        func_data_grpbox.setObjectName("main")

        # Creates filltable and input-manually checkboxes and their layout
        self.filltable = QCheckBox("Fill table")
        self.input_manually = QCheckBox("Input Manually")

        chkbx_hbox = QHBoxLayout()
        chkbx_hbox.addWidget(self.filltable)
        chkbx_hbox.addWidget(self.input_manually)

        chkbx_bg = QButtonGroup(self)
        chkbx_bg.addButton(self.filltable)
        chkbx_bg.addButton(self.input_manually)
        
        # Creates a QTableWidget and its layout
        self.table = QTableWidget()
        self.table.setRowCount(500)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["x", "f(x)"])
        
        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table)
        table_layout.addLayout(chkbx_hbox)

        # Sets the table_layout to a groupbox
        table_grpbox = QGroupBox("Table of values")
        table_grpbox.setObjectName("main")
        table_grpbox.setLayout(table_layout)

        self.solve_integral = QPushButton("Calculate Integral")

        
        
        # Vertical layout for the func_data_grpbox and table_grpbox
        groupbox_layout = QVBoxLayout()
        groupbox_layout.addWidget(func_data_grpbox)
        groupbox_layout.addWidget(table_grpbox)
        groupbox_layout.addWidget(self.solve_integral, stretch= 5)

        # Adds the groupbox_layout to the integral_main_hbox layout
        self.integral_main_hbox.addLayout(groupbox_layout)

        # Creates the results label and its layout
        self.integral_found = QLabel("")
        results_form = QFormLayout()
        results_form.addRow(QLabel("Integral:"), self.integral_found)

        # Sets the results_form to a groupbox
        results_grpbox = QGroupBox("Results")
        results_grpbox.setObjectName("main")
        results_grpbox.setLayout(results_form)

        results_layout = QVBoxLayout()
        results_layout.addWidget(results_grpbox)
        results_layout.addStretch()

        # Adds the results_grpbox to the integral_main_hbox
        self.integral_main_hbox.addLayout(results_layout)