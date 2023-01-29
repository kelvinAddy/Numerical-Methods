# Written by Kelvin Addy

# Imports required modules
import sys, os, time

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QHBoxLayout, QWidget, QStatusBar, QSplashScreen)
from rootSolving import RootSolving
from optimization import Optimization
from integration import Integration
from graphplot import PlotGraph

style = """
        QGroupBox#main{
                color: green;
                font-size: 14px;
                font: bold;
        }
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Sets up the main program"""
        self.setMinimumSize(840, 700)
        self.setWindowTitle("Numerical Methods")
        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        """Sets the main window with the required widgets"""
        self.root_tab, self.graph_tab, self.optimum_tab, self.integral_tab = [QWidget() for _ in range(4)]
        
        self.main_tab = QTabWidget()

        # Creates a statusbar object to show a message
        statusbar = QStatusBar()
        statusbar.showMessage("Numerical Methods Version 1.00")
        self.setStatusBar(statusbar)

        # Dictionary to hold widgets for self.main_tab and their respective names
        method_dict = {self.root_tab: "Root Solving",
                       self.graph_tab: "Graph Plotting",
                       self.optimum_tab: "Unconstrained Optimization",
                       self.integral_tab: "Numerical Integration"
                       }
        for key in method_dict:
            self.main_tab.addTab(key, method_dict[key])

        self.setCentralWidget(self.main_tab)
        self.createRootWindow()
        self.createOptimumWindow()
        self.createGraphWindow()
        self.createIntegralWindow()

    def createRootWindow(self):
        """Sets up the root tab with the required widgets"""
        root_wdgt = RootSolving()
        root_wdgt_hbox = QHBoxLayout()
        root_wdgt_hbox.addWidget(root_wdgt)
        self.root_tab.setLayout(root_wdgt_hbox)

    def createOptimumWindow(self):
        """Sets up the Optimization tab with the required widgets"""
        optimum_wdgt = Optimization()
        optimum_wdgt_hbox = QHBoxLayout()
        optimum_wdgt_hbox.addWidget(optimum_wdgt)
        self.optimum_tab.setLayout(optimum_wdgt_hbox)

    def createGraphWindow(self):
        """Sets up the Graph Plotting tab with the required widgets"""
        plot_wdgt = PlotGraph()
        plot_wdgt_hbox = QHBoxLayout()
        plot_wdgt_hbox.addWidget(plot_wdgt)
        self.graph_tab.setLayout(plot_wdgt_hbox)

    def createIntegralWindow(self):
        """Sets up the Integral tab with the required widgets"""
        integral_wdgt = Integration()
        integral_wdgt_hbox = QHBoxLayout()
        integral_wdgt_hbox.addWidget(integral_wdgt)
        self.integral_tab.setLayout(integral_wdgt_hbox)

# Gets the absolute path of the current script file
basedir = os.path.dirname(__file__)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(style)
    app.setStyle("Fusion")
    app.setWindowIcon(QIcon(os.path.join(basedir, "./images/endless.png")))
    splash = QSplashScreen(QPixmap(os.path.join(basedir, "./images/endless.png")))
    splash.show()
    time.sleep(1)
    app.processEvents()
    window = MainWindow()
    splash.finish(window)
    sys.exit(app.exec())