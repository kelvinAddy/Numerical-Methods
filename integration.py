# Written by Kelvin Addy

# imports the required widgets
import os
from numpy import sin, cos, tan, arange, sqrt
from PyQt6.QtWidgets import (QWidget, QPushButton, QRadioButton,
                             QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QGroupBox, QButtonGroup,
                             QCheckBox, QFormLayout, QMessageBox,
                             QTableView, QHeaderView)

from PyQt6.QtGui import QIcon, QRegularExpressionValidator, QStandardItemModel, QStandardItem
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

        # Creates fill_table and input-manually checkboxes and their layout
        self.fill_table = QCheckBox("Fill table")
        self.fill_table.clicked.connect(self.fillTable)
        self.enable_table = QCheckBox("Enable")
        self.enable_table.clicked.connect(lambda state: self.table.setEnabled(state))

        chkbx_hbox = QHBoxLayout()
        chkbx_hbox.addWidget(self.fill_table)
        chkbx_hbox.addWidget(self.enable_table)
        
        # Creates a QTableView, QStandardItemModel objects and its layout
        self.table_model = QStandardItemModel()
        self.table_model.setRowCount(500)
        self.table_model.setColumnCount(2)
        self.table_model.setHorizontalHeaderLabels(["x", "f(x)"])

        self.table = QTableView()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setModel(self.table_model)
        self.table.setDisabled(True)
        
        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table)
        table_layout.addLayout(chkbx_hbox)

        # Sets the table_layout to a groupbox
        table_grpbox = QGroupBox("Table of values")
        table_grpbox.setObjectName("main")
        table_grpbox.setLayout(table_layout)

        self.solve_integral = QPushButton("Calculate Integral")
        self.solve_integral.clicked.connect(self.solveIntegral)

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

        self.validateFields()
        self.algo = Algorithms()

    def validateFields(self):
        """Allows input of text which match a given pattern"""
        float_regex = QRegularExpression(r"-?[0-9]+.?[0-9]+")
        expression_regex = QRegularExpression(r"[\s\w 0-9 /()*+.-]+")
        int_regex = QRegularExpression(r"[0-9]+")

        for i in self.func_edit, self.upper_limit, self.lower_limit, self.intervals:
            if i is self.func_edit:
                i.setValidator(QRegularExpressionValidator(QRegularExpression(expression_regex)))
            elif i in (self.upper_limit, self.lower_limit):
                i.setValidator(QRegularExpressionValidator(QRegularExpression(float_regex)))
            else:
                i.setValidator(QRegularExpressionValidator(QRegularExpression(int_regex)))

    
    def checkForEmptyFields(self, function, *args):
        """Returns a warning message if empty fields exist else, calls a function"""
        if not all((self.func_edit.text(), self.upper_limit.text(), self.lower_limit.text(), self.intervals.text())):
            QMessageBox.warning(self, "Empty Fields",
                                "Empty Fields exist in function data, ensure required data is entered in every field.",
                                QMessageBox.StandardButton.Ok)
        else:
            return function(*args)
    
    def getFuncData(self):
        """Gets data from the QLineEdits in the function data groupbox"""
        # Gets function data
        function = lambda x: eval(self.func_edit.text())
        x_lower_num = float(self.lower_limit.text())
        x_upper_num = float(self.upper_limit.text())
        x_interval_num = int(self.intervals.text())

        # Returns x values and function to be integrated
        h = (x_upper_num - x_lower_num)/(x_interval_num)
        self.x_values = arange(x_lower_num, x_upper_num + h, h)
        return function, x_lower_num, x_upper_num, x_interval_num
    
    def getTableData(self):
        """Gets data from the table widget"""
        # List to hold x and y axis data
        list_x, list_y = [], []
        for index in range(self.table_model.rowCount()):
            item_x = self.table_model.item(index , 0)
            item_y = self.table_model.item(index, 1)

            if item_x and item_y:
                list_x.append(float(item_x.text()))
                list_y.append(float(item_y.text()))

        return list_x, list_y
    
    def enableTable(self, state):
        """Enables the table or function data groupbox widgets based on the state of the enable checkbox"""
        if state:
            self.table.setEnabled(True)
            for widget in (self.func_edit, self.upper_limit, self.lower_limit, self.intervals):
                widget.setDisabled(True)
        else:
            self.table.setDisabled(True)
            for widget in (self.func_edit, self.upper_limit, self.lower_limit, self.intervals):
                widget.setDisabled(False)

    def fillTable(self):
        """fills each table widget cell with x and y values"""
        if self.enable_table.isChecked():
            table_data = self.checkForEmptyFields(self.getFuncData)
            if table_data:
                func, *_ = table_data
                for index, num in enumerate(zip(self.x_values, func(self.x_values))):
                    item = [QStandardItem(str(i)) for i in num]
                    self.table_model.insertRow(index, item)
            else:
                self.fill_table.setChecked(False)
        else:
            self.fill_table.setChecked(False)
            QMessageBox.warning(self, "Error", "Table must be enabled to fill table.", QMessageBox.StandardButton.Ok)

    def solveSimps3rd(self):
        function, x_lower_num, x_upper_num, x_interval_num  = self.getFuncData()
        answer = self.algo.simpsons_3rd_rule(function, x_lower_num, x_upper_num, x_interval_num)
        self.integral_found.setText(f"{answer}")

    def solveSimps8th(self):
        function, x_lower_num, x_upper_num, x_interval_num  = self.getFuncData()
        answer = self.algo.simpsons_8th_rule(function, x_lower_num, x_upper_num, x_interval_num)
        self.integral_found.setText(f"{answer}")
    
    def solveTrapzoid(self):
        function, x_lower_num, x_upper_num, x_interval_num  = self.getFuncData()
        answer = self.algo.trapazoidal_rule(function, x_lower_num, x_upper_num, x_interval_num)
        self.integral_found.setText(f"{answer}")
    
    def solveMonteCarlo(self):
        function, x_lower_num, x_upper_num, x_interval_num  = self.getFuncData()
        answer = self.algo.monte_carlo(function, x_lower_num, x_upper_num, x_interval_num)
        self.integral_found.setText(f"{answer}")
    
    def solveIntegral(self):
        """Calculates the required integral using the selected method"""
        try:
            
            if self.simp8th_rb.isChecked():
                self.checkForEmptyFields(self.solveSimps8th)
            
            if self.simps3rd_rb.isChecked():
                self.checkForEmptyFields(self.solveSimps3rd)
            
            if self.trapezium_rb.isChecked():
                self.checkForEmptyFields(self.solveTrapzoid)
            
            if self.montecarlo_rb.isChecked():
                self.checkForEmptyFields(self.solveMonteCarlo)

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