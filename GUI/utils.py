from PyQt5 import QtWidgets,QtGui

def newAction(parent=None,text = None,
              slot = None,shortcut = None,
              icon = None,tip = None,
              enabled = None):
    action = QtWidgets.QAction(text,parent)
    if icon is not None:
        action.setIcon(QtGui.QIcon(icon))
    if shortcut is not None:
        if isinstance(shortcut,(list,tuple)):
            action.setShortcut(shortcut)
        else: 
            action.setShortcut(shortcut)
    if tip is not None:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    if slot is not None:
        action.triggered.connect(slot)
    action.setEnabled(enabled)
    return action

def addActions(widget,actions):
    for action in actions:
        if action is None:
            widget.addSeparator() 
        elif isinstance(action,QtWidgets.QMenu):
            widget.addMenu(action)
        else: 
            widget.addAction(action)
