"""
Adapted from wxPython website at http://wiki.wxpython.org/ModelViewController/.
"""

import wx
from pubsub import pub

print('pubsub API version', pub.VERSION_API)

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

useNotifyByWriteFile(sys.stdout)

# the following two modules don't know about each other yet will
# exchange data via pubsub:
from frame_view import FrameView
from panels_view import PanelView
from toolbar_view import ToolBarView
from tree_view import TreeView
from dm_enum import InputType
from fakedata import documents_obj

class Model:
    def __init__(self):
        self.data = {'items': documents_obj, 'index':0, 'label': documents_obj[0].label}

    def updatePanel(self, data):
        self.data['label'] = data['label']
        self.data['index'] = data['index']
        pub.sendMessage("data_changed", data=self.data)

    def updateItem(self, data):
        self.data['label'] = data['label']
        self.data['index'] = data['index']
        pub.sendMessage("data_changed", data=self.data)

class Controller:
    def __init__(self):
        self.model = Model()

        self.frame = FrameView(None, title = 'math content manager', size=wx.Size(800, 400))
        self.tree = TreeView(self.frame, self.model.data)
        self.toolbarPanel = ToolBarView(self.frame, self.model.data)

        self.rightTopPanel = PanelView(self.frame, title=self.model.data['label'], pos=(self.frame.Size.width/4, 70), size=(self.frame.Size.width*3/4, self.frame.Size.height/2), data=self.model.data)      
  
        self.rightBottomPanel = PanelView(self.frame, title=self.model.data['label'], pos=(self.frame.Size.width/4, self.frame.Size.height/2), size=(self.frame.Size.width*3/4, self.frame.Size.height/2), data=self.model.data, is_count_total=True)
        self.frame.show(True)

        pub.subscribe(self.changeData, 'data_changing')

    def changeData(self, data):
        if data['type'].value & InputType.PANEL.value:
            self.model.updatePanel(data)
        if data['type'].value & InputType.ITEM.value:
            self.model.updateItem(data)


if __name__ == "__main__":
    app = wx.App()
    c = Controller()
    sys.stdout = sys.__stdout__
    app.MainLoop()