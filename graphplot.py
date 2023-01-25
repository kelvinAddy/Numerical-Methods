from PyQt6.QtWidgets import (QLabel, QTableWidget, QWidget,
                            QFormLayout, QGroupBox, QPushButton,
                            QLineEdit, QHBoxLayout, QVBoxLayout,
                            QCheckBox)
from PyQt6.QtCore import Qt
import numpy as np
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
        self.func_edit.setPlaceholderText("Enter function in python synthax. Eg: x**2 - 4*x")
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

        # Creates a table widget, QPushButton and its layout
        self.table = QTableWidget()
        self.table.setRowCount(500)
        self.table.setColumnCount(2)
        self.table.setDisabled(True)

        # Creates enable checkbox, load data QPushButton and their layout
        self.enable_table = QCheckBox("Enable")
        self.enable_table.clicked.connect(lambda state: self.table.setEnabled(state))
        self.load_data = QPushButton("Load Data")

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

    
    def getData(self):
        """gets required data for plotting"""
        if self.enable_table.isChecked:
            self.function = lambda x: eval(self.func_edit.text())
            x_lower_num = float(self.x_lower.text())
            x_upper_num = float(self.x_upper.text())
            x_step_num = float(self.step_size.text())

            self.x_values = np.arange(x_lower_num, x_upper_num + x_step_num, x_step_num)
            self.y_values = self.function(self.x_values)
        else:
            pass

    def plotFunc(self):
        """Embeds a matplotlib plot onto the canvas"""
        self.getData()
        self.canvas.fig.clear()
        self.canvas.add_subplot()
        self.canvas.axes.plot(self.x_values, self.y_values, color="green")
        self.canvas.draw()

