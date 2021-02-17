import sys
import yaml
import os 
from PyQt5 import QtCore, QtGui, QtWidgets
from views.widgets.Button_dialog import Buttons
from views.widgets.Label_dialog import Labels
from model_view import Model_MainWindow

class Main_Window(QtWidgets.QMainWindow):
    def __init__(self,config):
        super().__init__()
        self.config = config 
        self.main_view()
        with open('./resources/css/qt.css','r') as css: 
            self.setStyleSheet(css.read())    
            
    def main_view(self):
        self.resize(self.config['main_window']['width'],
                    self.config['main_window']['height'])
        self.centralwidget = QtWidgets.QWidget(self)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(self.config['main_window']['widget_x_cor'],
                                             self.config['main_window']['widget_y_cor'],
                                             self.config['main_window']['widget_width'],
                                             self.config['main_window']['widget_height']))
        # Initialize class for Labels and Buttons
        self.Label = Labels(main_widget=self.widget)
        self.Button = Buttons(main_widget=self.widget)
        # ================== Vertical Layout ==================
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.addWidget(self.Label.main_image_label)
        self.verticalLayout.addWidget(self.Label.main_text_label)
        # ================== Horizontal Layout ================
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.addWidget(self.Button.Histo_button)
        self.horizontalLayout.addWidget(self.Button.Pneumonia_button)
        self.horizontalLayout.addWidget(self.Button.EEG_button)
        # =====================================================
        self.verticalLayout.addLayout(self.horizontalLayout)
        # Status Bar - initializes status tips for objects
        # Set Window Icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.getcwd()+'/resources/icons/Handshake.png'),
                                     QtGui.QIcon.Normal,
                                     QtGui.QIcon.Off)
        # Set MainWindow properties
        self.setCentralWidget(self.centralwidget)
        self.setFont(QtGui.QFont(self.config['main_window']['font'],
                                 self.config['main_window']['font-size']))
        self.setWindowIcon(icon)
        self.setWindowTitle(self.config['main_window']['appTitle'])
        self.setCentralWidget(self.centralwidget)
        #Signals
        self.Button.Histo_button.clicked.connect(self.initialize)
        self.Button.Pneumonia_button.clicked.connect(self.show_popup_error)
        self.Button.EEG_button.clicked.connect(self.show_popup_error)
        
    def initialize(self):
        self.hide()
        self.main_window = Model_MainWindow(self.config)
        self.main_window.show()

    def show_popup_error(self):
        # Error_msg functionality
        error_msg = QtWidgets.QMessageBox() 
        error_msg.setWindowTitle(self.config['main_window']['appTitle'])
        error_msg.setFont(QtGui.QFont(self.config['main_window']['font'],
                                      self.config['main_window']['font-size']))
        error_msg.setText("Sorry,work is in progress,could not proceed")
        error_msg.setIcon(QtWidgets.QMessageBox.Critical)
        # Execution - important
        execute = error_msg.exec_()
    
    # Here events are defined
    def closeEvent(self,event):
        reply = QtWidgets.QMessageBox.question(self,
                                               self.config['model_view']['appTitle'],
                                               "Are you sure want to close the window ?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            QtWidgets.QApplication.quit()
        else: 
            pass
    
    def keyPressEvent(self,event): 
        if event.key() == QtCore.Qt.Key_Escape: 
            QtWidgets.QApplication.quit()
        else:
            event.ignore()

if __name__ == "__main__":
    #Temporary config loading, until main script will be done.
    with open('./config/config.yaml','r') as f: 
        config = yaml.safe_load(f)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling,
                                        True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps,
                                        True)
    app = QtWidgets.QApplication(sys.argv)
    main_view = Main_Window(config=config)
    main_view.show()
    sys.exit(app.exec_())