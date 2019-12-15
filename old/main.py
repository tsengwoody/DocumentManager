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

# the following modules don't know about each other yet will
# exchange data via pubsub:
from View.frame_view import FrameView
from View.panels_view import PanelView
from View.toolbar_view import ToolBarView
from View.tree_view import TreeView
from Model.model import Model
from enums import InputType, PanelType, ActionType

class Controller:
    def __init__(self):
        self.size = wx.Size(1000, 400)
        self.model = Model(self)
        self.frame = FrameView(None, title = 'math content manager', size=self.size)
        self.panel = wx.Panel(self.frame, size=self.size)

        pub.subscribe(self.changeData, 'data_changing')
        
        self.tree = TreeView(self.panel, self.model.ori_data)
        self.toolbarPanel = ToolBarView(self.panel, self.model.data)

        ori_data = self.model.data.copy()
        counting_data = self.model.data.copy()
        counting_data['items'] = []
        counting_data['clickable'] = False

        self.rightTopPanel = PanelView(self.panel, title=self.model.data['label'], pos=(self.frame.Size.width/4, 70), size=(self.frame.Size.width*3/4-15, self.frame.Size.height/3), data=self.model.data, event_name=self.model.event_name[0])
        
        self.rightBottomPanel = PanelView(self.panel, title=self.model.data['label'], pos=(self.frame.Size.width/4, self.frame.Size.height/2), size=(self.frame.Size.width*3/4-15, self.frame.Size.height/2-40), data=counting_data, event_name=self.model.event_name[1])
        self.frame.show(True)

        self.rightTopPanel.setData(ori_data)

    def changeData(self, data):
        self.model.updateItem(data)
    
    def sendMessage(self, event, data):
        pub.sendMessage(event, data=data)


if __name__ == "__main__":
    app = wx.App()
    c = Controller()
    sys.stdout = sys.__stdout__
    app.MainLoop()