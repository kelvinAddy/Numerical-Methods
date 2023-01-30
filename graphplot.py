from PyQt6.QtWidgets import (QLabel, QTableWidget, QWidget,
                            QFormLayout, QGroupBox, QPushButton,
                            QLineEdit, QHBoxLayout, QVBoxLayout,
                            QCheckBox, QFileDialog, QMessageBox,
                            QTableView)
                            
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QRegularExpressionValidator
from numpy import tan, cos, sin, sqrt, arange
import csv
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

class CreateCanvas(FigureCanvasQTAgg):
    def __init__(self, parent = None, nrows = 1, ncols = 1):
        # Create matplotlib figure object
        self.fig = Figure(figsize=(17,17))

        self.add_subplot()
        super().__init__(self.fig)

    def add_subplot(self):
        # Create axes and set the number of subplots 
        self.axes = self.fig.add_subplot(111)

class PlotGraph(QWidget):
    def __init__(self):
        super().__init__()  
        self.initUI()
    
    def initUI(self):
        """Sets up the graph plot window"""
        self.setUpMainWindow()
    
    def setUpMainWindow(self):
        """Creates and arranges widgets in the graph plot window"""
        # Creates required QlineEdits and their layouts
        self.func_edit  = QLineEdit()
        self.x_lower = QLineEdit()
        self.x_upper = QLineEdit()
        self.step_size = QLineEdit()

        func_form  = QFormLayout()
        func_form.addRow(QLabel("Function"), self.func_edit)

        x_data = QHBoxLayout()
        x_data.addWidget(QLabel("x-lower:"))
        x_data.addWidget(self.x_lower)
        x_data.addWidget(QLabel("x-upper:"))
        x_data.addWidget(self.x_upper)
        x_data.addWidget(QLabel("step:"))
        x_data.addWidget(self.step_size)

        # Adds func_form and x_data layouts to a QVBoxLayout
        func_data_layout = QVBoxLayout()
        func_data_layout.addLayout(func_form)
        func_data_layout.addLayout(x_data)

        # Sets the func_data_layout to a groupbox
        func_data_grpbox = QGroupBox("Function Data")
        func_data_grpbox.setObjectName("main")
        func_data_grpbox.setLayout(func_data_layout)

        # Creates a table model, tableview widget, QPushButton and its layout
        self.table_model = QStandardItemModel()
        self.table_model.setRowCount(200)
        self.table_model.setColumnCount(2)
        
        self.table = QTableView()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setModel(self.table_model)
        self.table.setDisabled(True)

        # Creates enable checkbox, load data QPushButton and their layout
        self.enable_table = QCheckBox("Enable")
        self.enable_table.clicked.connect(self.enableTable)
        self.load_data = QPushButton("Load Data")
        self.load_data.clicked.connect(self.loadCSV)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.enable_table)
        buttons_layout.addWidget(self.load_data)

        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table)
        table_layout.addLayout(buttons_layout)

        # Sets table_layout to a groupbox
        table_groupbox = QGroupBox("Table of values")
        table_groupbox.setObjectName("main")
        table_groupbox.setLayout(table_layout)

        # Adds func_data_grpbox and table_groupbox to a QVBoxLayout
        data_layout = QVBoxLayout()
        data_layout.addWidget(func_data_grpbox)
        data_layout.addWidget(table_groupbox)

        # Adds the table groupbox to graph_main_layout
        self.graph_main_layout = QHBoxLayout()
        self.graph_main_layout.addLayout(data_layout)

        self.plot_func = QPushButton("Plot")
        self.plot_func.clicked.connect(self.plotFunc)
        # Creates an instance of the CreateCanvas, NavigationToolbar2QT class and layouts
        self.canvas = CreateCanvas()
        navigation_toolbar = NavigationToolbar2QT(self.canvas)

        canvas_layout = QVBoxLayout()
        canvas_layout.addWidget(navigation_toolbar)
        canvas_layout.addWidget(self.canvas)
        canvas_layout.addWidget(self.plot_func)
        
        # Sets the canvas_layout to a groupbox
        canvas_groupbox = QGroupBox("Plot Area")
        canvas_groupbox.setObjectName("main")
        canvas_groupbox.setLayout(canvas_layout)
        canvas_groupbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Adds the canvaslayout to the graph_main_layout
        self.graph_main_layout.addWidget(canvas_groupbox)
        self.setLayout(self.graph_main_layout)

        self.validateFields()

    def validateFields(self):
        """Allows input of text which match a given pattern"""
        number_regex = QRegularExpression(r"-?[0-9-]+.?[0-9]+")
        expression_regex = QRegularExpression(r"[\s\w 0-9 /()*+.-]+")

        for i in self.func_edit, self.x_lower, self.x_upper, self.step_size:
            if i is self.func_edit:
                i.setValidator(QRegularExpressionValidator(QRegularExpression(expression_regex)))
            else:
                i.setValidator(QRegularExpressionValidator(QRegularExpression(number_regex)))

    def getFuncData(self):
        """Gets data from the QlinEdits in the function data groupbox"""
        # Gets function data
        function = lambda x: eval(self.func_edit.text())
        x_lower_num = float(self.x_lower.text())
        x_upper_num = float(self.x_upper.text())
        x_step_num = float(self.step_size.text())

        # variables to hold x and y axis data
        x_values = arange(x_lower_num, x_upper_num + x_step_num, x_step_num)
        y_values = function(x_values)
        return x_values, y_values

    def enableTable(self, state):
        """Enables the table or function data groupbox widgets based on the state of the enable checkbox"""
        if state:
            self.table.setEnabled(True)
            for widget in (self.func_edit, self.x_upper, self.x_lower, self.step_size):
                widget.setDisabled(True)
        else:
            self.table.setDisabled(True)
            for widget in (self.func_edit, self.x_upper, self.x_lower, self.step_size):
                widget.setDisabled(False)


    def getTableData(self):
        """Gets table data about the function to be plotted"""
        # List to hold x and y axis data
        list_x, list_y = [], []
        for index in range(self.table_model.rowCount()):
            item_x = self.table_model.item(index , 0)
            item_y = self.table_model.item(index, 1)

            if item_x and item_y:
                list_x.append(float(item_x.text()))
                list_y.append(float(item_y.text()))

        return list_x, list_y

    def drawOnCanvas(self, x, y):
        """Embeds a matplotlib plot figure onto the canvas"""
        # Clears the canvas and embeds a plot figure on it
        self.canvas.fig.clear()
        self.canvas.add_subplot()
        self.canvas.axes.plot(x, y, color="green")
        self.canvas.draw()

    def checkForEmptyFields(self, function, *args):
        """Returns a warning message if empty fields exist else, calls a function"""
        if not all((self.func_edit.text(), self.x_upper.text(), self.x_lower.text(), self.step_size.text())):
            QMessageBox.warning(self, "Empty Fields",
                                "Empty Fields exist in function data, ensure required data is entered in every field.",
                                QMessageBox.StandardButton.Ok)
        else:
            return function(*args)
    
    
    def plotFunc(self):
        """Plots the function based on the state of the enable checkbutton"""
        try:
            if self.enable_table.isChecked():
                plot_data = self.getTableData()
                if plot_data:
                    self.x_values, self.y_values = plot_data
                    self.drawOnCanvas(self.x_values, self.y_values)
            else:
                plot_data = self.checkForEmptyFields(self.getFuncData)
                if plot_data:
                    self.x_values, self.y_values = plot_data
                    self.drawOnCanvas(self.x_values, self.y_values)

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
    
    def loadCSV(self):
        """Loads csv data into the table widget"""
        if self.enable_table.isChecked():
            file_name, _ = QFileDialog.getOpenFileName(self, "Open file",".","CSV file(*.csv)")
            if file_name:
                self.table_model.clear()
                with open(file_name, "r") as file:
                    csv_file = csv.reader(file)
                    self.table_model.setHorizontalHeaderLabels(next(csv_file))

                    for index, items in enumerate(csv.reader(file)):
                        item = [QStandardItem(i) for i in items]
                        self.table_model.insertRow(index, item)
        else:
            QMessageBox.warning(self,"Error","Table must be enabled to load csv file",QMessageBox.StandardButton.Ok)