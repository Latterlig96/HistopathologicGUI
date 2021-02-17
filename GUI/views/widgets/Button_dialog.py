from PyQt5 import QtWidgets

class Buttons(QtWidgets.QDialog):

    def __init__(self,
                main_widget = None,
                grid_model_widget = None,
                vert_model_widget = None): 
        super().__init__()
        self.main_widget = main_widget
        self.grid_model_widget = grid_model_widget
        self.vert_model_widget = vert_model_widget
        
        if main_widget:
            self.main_view_buttons()
        else:
            self.show_predicted_image()
            self.load_button()
            self.button_box()

    def main_view_buttons(self):
        # ===================================================
        self.Histo_button = QtWidgets.QPushButton(self.main_widget) 
        self.Histo_button.setText("Histopathologic Cancer Detection")
        self.Histo_button.setStatusTip("Works properly")
        self.Histo_button.setObjectName("Histo_button")
        # ===================================================
        self.Pneumonia_button = QtWidgets.QPushButton(self.main_widget) 
        self.Pneumonia_button.setText("Pneumonia Classifier")
        self.Pneumonia_button.setStatusTip("Work is in progress")
        self.Pneumonia_button.setObjectName("Pneumonia_button")
        # ===================================================
        self.EEG_button = QtWidgets.QPushButton(self.main_widget)
        self.EEG_button.setText("EEG Classifier")
        self.EEG_button.setStatusTip("Work is in progress")
        self.EEG_button.setObjectName("EEG_button")
        # ===================================================
        self.Histo_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Expanding)
        self.Pneumonia_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Expanding)
        self.EEG_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Expanding)         
    def show_predicted_image(self):
        self.show_button = QtWidgets.QPushButton(self.grid_model_widget)
        self.show_button.setText("Show predicted image")
        self.show_button.setObjectName("show_button")
        self.show_button.setEnabled(True)

    def load_button(self):
        self.load = QtWidgets.QPushButton(self.grid_model_widget)
        self.load.setText("Load")
        self.load.setObjectName("Load")
    
    def button_box(self):
        self.buttonbox = QtWidgets.QDialogButtonBox(self.vert_model_widget)
        self.buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonbox.setCenterButtons(False)
        self.buttonbox.setObjectName("buttonbox")