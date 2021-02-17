import numpy as np 
import os
import cv2
from PIL import Image,ImageQt
from lime import lime_image
from lime.wrappers.scikit_image import SegmentationAlgorithm
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtGui, QtWidgets
from tensorflow.keras.applications.nasnet import preprocess_input
from tensorflow.keras.models import load_model
from skimage.segmentation import mark_boundaries
from views.widgets.Label_dialog import Labels,Line_Date_Edit
from views.widgets.Graphic_dialog import Graphics
from views.widgets.Button_dialog import Buttons
from views.widgets.List_dialog import List
from utils import addActions,newAction

class Model_MainWindow(QtWidgets.QMainWindow):
    def __init__(self,config):
        super().__init__()
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling,
                                            True)
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps,
                                            True)
        self.config = config
        self.model_view()
        self.MODEL_DIR = os.path.join(os.getcwd(),
                                 'resources',
                                 'models',
                                 'model_pierwszy_adam.h5')
        with open('./resources/css/qt.css') as css: 
            self.setStyleSheet(css.read())
            
    def model_view(self):
        # Initialize Main_Window and main_widgets properties
        self.setWindowTitle(self.config['model_view']['appTitle'])
        self.resize(self.config['model_view']['width'],
                    self.config['model_view']['height'])
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.grid_widget = QtWidgets.QWidget(self.centralwidget)
        self.grid_widget.setGeometry(QtCore.QRect(self.config['model_view']['grid_widget_x_cor'],
                                                  self.config['model_view']['grid_widget_y_cor'],
                                                  self.config['model_view']['grid_widget_width'],
                                                  self.config['model_view']['grid_widget_height']))
        self.vert_widget = QtWidgets.QWidget(self.centralwidget)
        self.vert_widget.setGeometry(QtCore.QRect(self.config['model_view']['vert_widget_x_cor'],
                                                  self.config['model_view']['vert_widget_y_cor'],
                                                  self.config['model_view']['vert_widget_width'],
                                                  self.config['model_view']['vert_widget_height']))
        # Initialize widgets responsible for GUI functionality
        self.Button = Buttons(main_widget = None,
                              grid_model_widget = self.grid_widget,
                              vert_model_widget = self.vert_widget)

        self.Label = Labels(main_widget = None,
                            grid_model_widget = self.grid_widget,
                            vert_model_widget = self.vert_widget)

        self.Graphic = Graphics(widget = self.grid_widget)

        self.Line_Dat_Edit = Line_Date_Edit(grid_model_widget = self.grid_widget,
                                            vert_model_widget = self.vert_widget)

        self.Listed = List(vert_model_widget = self.vert_widget)

        # Making grid layout functionality
        self.gridLayout = QtWidgets.QGridLayout(self.grid_widget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.addWidget(self.Graphic.org_image_graphic, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.Label.negative_sample_label, 7, 1, 1, 1)
        self.gridLayout.addWidget(self.Line_Dat_Edit.img_path_ledit, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.Line_Dat_Edit.pos_sample_ledit, 6, 1, 1, 1)
        self.gridLayout.addWidget(self.Label.out_mod_img, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.Button.load, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.Label.positive_sample_label, 5, 1, 1, 1)
        self.gridLayout.addWidget(self.Label.org_img, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.Label.model_predict_label, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.Line_Dat_Edit.neg_sample_ledit, 8, 1, 1, 1)
        self.gridLayout.addWidget(self.Graphic.output_model_graphic, 3, 1, 1, 2)
        self.gridLayout.addWidget(self.Label.img_path_label, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.Button.show_button, 8, 0, 1, 1)
        # Adding widgets to vertical layout
        self.verticalLayout = QtWidgets.QVBoxLayout(self.vert_widget)
        self.verticalLayout.addWidget(self.Line_Dat_Edit.DateEdit)
        self.verticalLayout.addWidget(self.Label.name_label)
        self.verticalLayout.addWidget(self.Line_Dat_Edit.name_ledit)
        self.verticalLayout.addWidget(self.Label.surname_label)
        self.verticalLayout.addWidget(self.Line_Dat_Edit.surname_ledit)
        self.verticalLayout.addWidget(self.Label.area_of_occ_label)
        self.verticalLayout.addWidget(self.Listed.listing)
        self.verticalLayout.addWidget(self.Label.notes_label)
        self.verticalLayout.addWidget(self.Line_Dat_Edit.text_edit)
        self.verticalLayout.addWidget(self.Button.buttonbox)

        # Set window additional properties 
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(os.getcwd()+'/resources/icons/Handshake.png')))
        self.setFont(QtGui.QFont(self.config['model_view']['font'],
                                self.config['model_view']['font-size']))

        #Signals 
        self.Button.load.clicked.connect(self.openFile)
        self.Listed.listing.itemClicked.connect(self.store_occurence_item)
        self.Line_Dat_Edit.neg_sample_ledit.textChanged.connect(self.store_sample_info)
        self.Button.show_button.clicked.connect(self.get_model_image)
        self.Button.buttonbox.accepted.connect(self.saveFile)
        self.Button.buttonbox.rejected.connect(self.closingApp)

        #Menubar and actions 
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        aboutmenu = menubar.addMenu("&About")
        editmenu = menubar.addMenu("&Edit")

        loadFile = newAction(parent=self,
                            text='Load File',
                            slot=self.openFile,
                            shortcut=self.config['Shortcuts']['load_file'],
                            icon=None,
                            tip='Load .tif file',
                            enabled=True)

        saveFile = newAction(parent=self,
                            text="Save As",
                            slot=self.saveFile,
                            shortcut=self.config['Shortcuts']['save_file'],
                            icon = None,
                            tip='Save file into given directory',
                            enabled=True)

        readme = newAction(parent=self,
                           text="Readme",
                           slot=self.readme_text,
                           shortcut=self.config['Shortcuts']['readme'],
                           icon=None,
                           tip="Show readme",
                           enabled=True)
        
        resize = newAction(parent=self,
                           text="Resize window",
                           slot=self.resize_window_to_support_ImageMasker,
                           shortcut=self.config['Shortcuts']['resize'],
                           icon=None,
                           tip="Resize window to support bigger images",
                           enabled=True)
        reset = newAction(parent=self,
                          text="Reset window",
                          slot=self.reset_window,
                          shortcut=self.config['Shortcuts']['reset'],
                          icon=None,
                          tip="Reset window to work on new image",
                          enabled=True)

        addActions(filemenu,(loadFile,saveFile))
        addActions(aboutmenu,(readme,))
        addActions(editmenu,(resize,None,reset))
    
    def readme_text(self):
        """ Readme text to help user to understand what is happening
            in terms of model predictions and visualization
            (what is excatly happening and how LIME works)
        """
        pass

    def resize_window_to_support_ImageMasker(self):
        """ Here i would like to create a function that will resize 
            GUI window and GraphicViews to support ImageMasker on bigger
            images... If it wont work i think about creating a new window
            that will plot subplots with each predicted chunk.
        """
        pass

    def reset_window(self):
        """ Reset window to work on new image """
        pass

    def openFile(self): 
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.raw_file,_ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                self.config['model_view']['appTitle'], 
                                                                "",
                                                                "All Files (*);;Python Files (*.py)",
                                                                options=options)
        if self.raw_file:
            filename = self.raw_file.split('/')[-1].replace('.tif','')
            self.Line_Dat_Edit.img_path_ledit.setText(filename)
            self.model_evaluate(self.raw_file)
            self.get_input_image(self.raw_file)


    def saveFile(self): 
        options = QtWidgets.QFileDialog.Options() 
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        save_name,_ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                            self.config['model_view']['appTitle'],
                                                            "All Files (*)",
                                                            options=options)
        if save_name == '':
            return None
        
        date = self.stored_date() 
        name = self.stored_name() 
        surname = self.stored_surname()
        occurence = self.store_occurence_item()
        text = self.store_text() 
        neg_sample,pos_sample = self.store_sample_info()

        with open(save_name,'w+') as save_file: 
            save_file.write("Date:" + " " + date+'\n')
            save_file.write("Name:" + " " + name+'\n')
            save_file.write("Surname:" + " " + surname+'\n')
            save_file.write("Occurence:" + " " + occurence+'\n')
            save_file.write("Additional Notes:" + " " + text+'\n')
            save_file.write("Negative Sample:" + " " + neg_sample+'\n')
            save_file.write("Positive Sample:" + " " + pos_sample+'\n')
        
        path = os.path.abspath(save_name)
        cv2.imwrite(path+'.tif',self.input_image)
        #TODO:save lime image into given directory
        #plt.imsave(path,self.temp_image)
        self.closingApp('Do you want to continue or close the application ?')

        
    def get_input_image(self,file):
        self.input_image = cv2.imread(file)
        self.input_image = cv2.cvtColor(self.input_image,cv2.COLOR_BGR2RGB)
        self.input_image = cv2.resize(self.input_image,(self.Graphic.org_image_graphic.width(),
                                            self.Graphic.org_image_graphic.height()),
                                            interpolation=cv2.INTER_NEAREST)
        image = Image.fromarray(self.input_image)
        scene = QtWidgets.QGraphicsScene()
        converted_image = QtGui.QPixmap.fromImage(QtGui.QImage(ImageQt.ImageQt(image)))
        pixmap = QtWidgets.QGraphicsPixmapItem(converted_image)
        scene.addItem(pixmap)
        self.Graphic.org_image_graphic.setScene(scene)
        

    def get_model_image(self):
        read_image = cv2.imread(self.raw_file)
        read_image = cv2.cvtColor(read_image,cv2.COLOR_BGR2RGB)
        process_image = preprocess_input(read_image)
        explainer = lime_image.LimeImageExplainer()
        explanation = explainer.explain_instance(np.array(process_image),
                                                self.model.predict,
                                                top_labels=10,
                                                hide_color=0,
                                                num_samples = 10,
                                                segmentation_fn=SegmentationAlgorithm('felzenszwalb'))
        temp,mask = explanation.get_image_and_mask(explanation.top_labels[0],
                                                   positive_only=False,
                                                   num_features =10,
                                                   hide_rest = True)
        model_image = mark_boundaries(temp/2 + 0.5,mask)
        self.getCanvas(model_image)
    

    def getCanvas(self,array_image): 
        figure = Figure()
        axes = figure.gca()
        axes.set_axis_off()
        axes.imshow(array_image)
        canvas = FigureCanvas(figure)
        canvas.setGeometry(0,0,self.Graphic.org_image_graphic.width(),
                               self.Graphic.org_image_graphic.height())
        scene = QtWidgets.QGraphicsScene()
        scene.addWidget(canvas)
        self.Graphic.output_model_graphic.setScene(scene)

    def model_evaluate(self,img_path):
        self.model = load_model(self.MODEL_DIR,compile=False)
        process_image = preprocess_input(cv2.imread(img_path))
        prediction = self.model.predict(np.expand_dims(process_image,axis=0))
        self.Line_Dat_Edit.neg_sample_ledit.setText(str(round(np.around(prediction,2)[0][0]*100,2))+'%')
        self.Line_Dat_Edit.pos_sample_ledit.setText(str(round(np.around(1-prediction,2)[0][0]*100,2))+'%')
    
    def stored_date(self): 
        return self.Line_Dat_Edit.DateEdit.date().toString()

    def stored_name(self): 
        return self.Line_Dat_Edit.name_ledit.text()

    def stored_surname(self): 
        return self.Line_Dat_Edit.surname_ledit.text()
    
    def store_occurence_item(self):
        return self.Listed.listing.currentItem().text()
    
    def store_text(self): 
        return self.Line_Dat_Edit.text_edit.toPlainText()

    def store_sample_info(self): 
        return (self.Line_Dat_Edit.neg_sample_ledit.text(),
                self.Line_Dat_Edit.pos_sample_ledit.text())
    
    # Here are events are defined 
    def resizeEvent(self,event): 
        """
           Scale Window with Mouse event
        """ 
        pass

    def closingApp(self,
                  question='Are you sure want to close the application ? any unsaved changes will be lost'):
        reply = QtWidgets.QMessageBox.question(self,
                                               self.config['model_view']['appTitle'],
                                               question,
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            QtWidgets.QApplication.quit()
        else: 
            pass
    
    def closeEvent(self,event):
        reply = QtWidgets.QMessageBox.question(self,
                                               self.config['model_view']['appTitle'],
                                               "Are you sure want to close the window ?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            QtWidgets.QApplication.quit()
        else: 
            event.ignore()
    
    def keyPressEvent(self,event): 
        if event.key() == QtCore.Qt.Key_Escape: 
            QtWidgets.QApplication.quit()