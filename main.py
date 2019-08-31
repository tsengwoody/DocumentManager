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
from fakedata import documents

class Model:
    def __init__(self):
        self.ori_data = {'items': documents}
        self.data = {'items': documents[0]['items'], 'index':[0], 'label':documents[0]['label'], 'type':documents[0]['type']}
        self.current_folder_layer=0

    def updateItem(self, data):
        index_array = self.data['index']
        if 'current_folder_layer' in data:
            self.current_folder_layer = data['current_folder_layer']
        index_array.insert(self.current_folder_layer,data['index'])
        del index_array[self.current_folder_layer+1:] 
        source = self.ori_data['items']
        path_str = ""
        for idx, val in enumerate(index_array):
            path_str = path_str + ('' if idx==0 else '/') + source[val]['label']
            self.data['type'] = source[val]['type']
            self.data['current_folder_layer'] = self.current_folder_layer
            if 'items' in source[val]:
                source = source[val]['items']
                self.data['items'] = source
            else:
                del self.data['items']
                self.data['content'] = source[val]['content']
                source = []
        self.data['index'] = index_array
        self.data['label'] = path_str
        current_index = data['index']
        data = self.data.copy()
        data['index'] = current_index
        pub.sendMessage("data_changed", data=data)

class Controller:
    def __init__(self):
        self.model = Model()

        self.frame = FrameView(None, title = 'math content manager', size=wx.Size(800, 400))
        self.panel = wx.Panel(self.frame)

        self.tree = TreeView(self.panel, self.model.ori_data)
        self.toolbarPanel = ToolBarView(self.panel, self.model.data)

        self.rightTopPanel = PanelView(self.panel, title=self.model.data['label'], pos=(self.frame.Size.width/4, 70), size=(self.frame.Size.width*3/4, self.frame.Size.height/3), data=self.model.data)      
  
        self.rightBottomPanel = PanelView(self.panel, title=self.model.data['label'], pos=(self.frame.Size.width/4, self.frame.Size.height/2), size=(self.frame.Size.width*3/4, self.frame.Size.height/2), data=self.model.data, is_count_total=True)
        self.frame.show(True)

        pub.subscribe(self.changeData, 'data_changing')

    def changeData(self, data):
        self.model.updateItem(data)


if __name__ == "__main__":
    app = wx.App()
    c = Controller()
    sys.stdout = sys.__stdout__
    app.MainLoop()