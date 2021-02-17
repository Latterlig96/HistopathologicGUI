from PyQt5 import QtWidgets

Area_of_occurrence = ['Jama brzuszna',
                      'Górne drogi oddechowe',
                      'Inne ogólne umiejscowienia',
                      'Mózg']

class List(QtWidgets.QDialog): 
    def __init__(self,
                vert_model_widget = None):
            super().__init__()
            self.vert_model_widget = vert_model_widget
            self.list_define()

    def list_define(self,items = len(Area_of_occurrence)): 
        self.listing = QtWidgets.QListWidget(self.vert_model_widget,
                                            selectionMode=QtWidgets.QAbstractItemView.MultiSelection)
        sorting_enabled = self.listing.isSortingEnabled() 
        self.listing.setSortingEnabled(False)
        for i,occurrence in zip(range(items),Area_of_occurrence): 
            item = QtWidgets.QListWidgetItem()
            item = self.listing.addItem(item)
            item = self.listing.item(i)
            item.setText(occurrence)
        self.listing.setSortingEnabled(sorting_enabled)