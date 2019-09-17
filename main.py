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
from enums import InputType, ConstValue
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
        if 'index' in data:
            if isinstance(data['index'], list):
                index_array = data['index']
            else:
                index_array.insert(self.current_folder_layer,data['index'])
            del index_array[self.current_folder_layer+1:]
        source = self.ori_data['items']
        path_str = ""
        for idx, val in enumerate(index_array):
            if (len(index_array)-1 == idx):
                if val >= len(source):
                    source.append({'label': data['label'], 'type': data['type'], 'items': data['items']})
                elif 'label' in data and (source[val]['label'] != data['label']):
                    source[val]['label'] = data['label']
                elif 'del' in data and data['del'] == True:
                    del source[val]
                    val = 0
                    if len(source)==0:
                        break
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
        if ConstValue.SKIP.value in self.data:
            del self.data[ConstValue.SKIP.value]
        if ConstValue.SKIP.value in data:
            self.data[ConstValue.SKIP.value] = data[ConstValue.SKIP.value]
        if 'index' in data:
            if isinstance(data['index'], list):
                current_index = data['index'][len(data['index'])-1]
            else:
                current_index = data['index']
        else:
            current_index = index_array[len(index_array)-1]
        data = self.data.copy()
        data['index'] = current_index
        pub.sendMessage("data_changed", data=data)

class Controller:
    def __init__(self):
        self.size = wx.Size(1000, 400)
        self.model = Model()
        self.frame = FrameView(None, title = 'math content manager', size=self.size)
        self.panel = wx.Panel(self.frame, size=self.size)

        self.tree = TreeView(self.panel, self.model.ori_data)
        self.toolbarPanel = ToolBarView(self.panel, self.model.data)

        self.rightTopPanel = PanelView(self.panel, title=self.model.data['label'], pos=(self.frame.Size.width/4, 70), size=(self.frame.Size.width*3/4-15, self.frame.Size.height/3), data=self.model.data)      
  
        self.rightBottomPanel = PanelView(self.panel, title=self.model.data['label'], pos=(self.frame.Size.width/4, self.frame.Size.height/2), size=(self.frame.Size.width*3/4-15, self.frame.Size.height/2-40), data=self.model.data, is_count_total=True)
        self.frame.show(True)

        pub.subscribe(self.changeData, 'data_changing')

    def changeData(self, data):
        self.model.updateItem(data)


if __name__ == "__main__":
    app = wx.App()
    c = Controller()
    sys.stdout = sys.__stdout__
    app.MainLoop()