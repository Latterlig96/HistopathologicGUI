from PyQt5 import QtCore, QtGui, QtWidgets
import codecs

class Labels(QtWidgets.QDialog): 
    def __init__(self,
                main_widget = None,
                grid_model_widget = None,
                vert_model_widget = None):
        super().__init__() 
        self.main_widget = main_widget
        self.grid_model_widget = grid_model_widget
        self.vert_model_widget = vert_model_widget
        if self.main_widget: 
            self.main_view_labels() 
        else: 
            self.model_view_labels()
    
    def main_view_labels(self): 
        #=========================================
        self.main_image_label = QtWidgets.QLabel(self.main_widget)
        self.main_image_label.setPixmap(QtGui.QPixmap('./resources/images/Medical'))
        #=========================================
        self.main_text_label = QtWidgets.QLabel(self.main_widget)
        self.main_text_label.setText(codecs.open('./resources/templates/main_text.html','r').read())
        
    def model_view_labels(self):
        # ================== Grid layout labels =======
        self.negative_sample_label = QtWidgets.QLabel(self.grid_model_widget) 
        self.negative_sample_label.setText("Negative sample:")
        # ========================================
        self.out_mod_img = QtWidgets.QLabel(self.grid_model_widget)
        self.out_mod_img.setText("Output model image")
        self.out_mod_img.setAlignment(QtCore.Qt.AlignCenter)
        # ========================================
        self.positive_sample_label = QtWidgets.QLabel(self.grid_model_widget) 
        self.positive_sample_label.setText("Positive sample:")
        # ========================================
        self.org_img = QtWidgets.QLabel(self.grid_model_widget) 
        self.org_img.setText("Original image")
        self.org_img.setAlignment(QtCore.Qt.AlignCenter)
        # ========================================
        self.model_predict_label = QtWidgets.QLabel(self.grid_model_widget)
        self.model_predict_label.setText("Model predictions")
        self.model_predict_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        # ========================================
        self.img_path_label = QtWidgets.QLabel(self.grid_model_widget) 
        self.img_path_label.setText("Image name")
        self.img_path_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        # ================= Horizontal layout labels =====
        self.name_label = QtWidgets.QLabel(self.vert_model_widget)
        self.name_label.setText("Name")
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        # ========================================
        self.surname_label = QtWidgets.QLabel(self.vert_model_widget)
        self.surname_label.setText("Surname")
        self.surname_label.setAlignment(QtCore.Qt.AlignCenter) 
        # ========================================
        self.area_of_occ_label = QtWidgets.QLabel(self.vert_model_widget)
        self.area_of_occ_label.setText("Area of occurrence")
        self.area_of_occ_label.setAlignment(QtCore.Qt.AlignCenter)
        # ========================================
        self.notes_label = QtWidgets.QLabel(self.vert_model_widget)
        self.notes_label.setText("Additional notes")
        self.notes_label.setAlignment(QtCore.Qt.AlignCenter)

class Line_Date_Edit(QtWidgets.QDialog): 
    def __init__(self,
                grid_model_widget = None,
                vert_model_widget = None):
        super().__init__()
        self.grid_model_widget = grid_model_widget
        self.vert_model_widget = vert_model_widget
        
        self.model_date_line_edit()
    
    def model_date_line_edit(self):
        self.img_path_ledit = QtWidgets.QLineEdit(self.grid_model_widget)
        # =========================
        self.pos_sample_ledit = QtWidgets.QLineEdit(self.grid_model_widget) 
        self.pos_sample_ledit.setPlaceholderText("Certainty in percentage")
        # =========================
        self.neg_sample_ledit = QtWidgets.QLineEdit(self.grid_model_widget) 
        self.neg_sample_ledit.setPlaceholderText("Certainty in percentage")
        # =========================
        self.DateEdit = QtWidgets.QDateEdit(self.vert_model_widget)
        # =========================
        self.name_ledit = QtWidgets.QLineEdit(self.vert_model_widget)
        self.name_ledit.setPlaceholderText("Write name...")
        # =========================
        self.surname_ledit = QtWidgets.QLineEdit(self.vert_model_widget)
        self.surname_ledit.setPlaceholderText("Write surname...")
        # =========================
        self.text_edit = QtWidgets.QTextEdit(self.vert_model_widget)