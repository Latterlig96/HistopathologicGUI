from PyQt5 import QtWidgets


class Graphics(QtWidgets.QDialog): 
    def __init__(self,widget):
        super().__init__()
        self.widget = widget
        self.define_view()
    
    def define_view(self):
        self.org_image_graphic = QtWidgets.QGraphicsView(self.widget)
        org_img_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        org_img_sizePolicy.setHorizontalStretch(0)
        org_img_sizePolicy.setVerticalStretch(0)
        org_img_sizePolicy.setHeightForWidth(self.org_image_graphic.sizePolicy().hasHeightForWidth())
        self.org_image_graphic.setSizePolicy(org_img_sizePolicy)
        # ================================================
        self.output_model_graphic = QtWidgets.QGraphicsView(self.widget)
        out_img_sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        out_img_sizePolicy.setHorizontalStretch(0) 
        out_img_sizePolicy.setVerticalStretch(0)
        out_img_sizePolicy.setHeightForWidth(self.output_model_graphic.sizePolicy().hasHeightForWidth())
        self.output_model_graphic.setSizePolicy(out_img_sizePolicy)