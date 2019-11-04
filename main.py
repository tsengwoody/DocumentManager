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
from View.frame_view import FrameView
from View.panels_view import PanelView
from View.toolbar_view import ToolBarView
from View.tree_view import TreeView
from enums import InputType, PanelType, ActionType
from fakedata import documents

# layer: current folder layer number in data
# index: current item index number in a layer
class Model:
    def __init__(self):
        self.ori_data = {'items': documents}
        self.data = {'items': documents[0]['items'], 'index':[0], 'layer': 0, 'label':documents[0]['label'], 'type':documents[0]['type']}
        self.event_name = ['data_changed', 'count_changed']

    def updateItem(self, data):
        index_array = self.data['index']
        layer = data['layer'] if 'layer' in data else self.data['layer']
        if 'action' in data:
            self.data['action'] = data['action']
        elif 'action' in self.data:
            del self.data['action'] 
        count_data_items = []
        if 'index' in data:
            # from tree_view.py
            if isinstance(data['index'], list):
                index_array = data['index']
            # from panels_view.py
            else:
                index_array.insert(layer, data['index'])
            del index_array[layer+1:]
        source = self.ori_data['items']
        path_str = ""
        for idx, val in enumerate(index_array):
            if (len(index_array)-1 == idx):
                if val >= len(source):
                    source.append({'label': data['label'], 'type': data['type'], 'items': data['items'] if 'items' in data else []})
                elif 'label' in data and (source[val]['label'] != data['label']):
                    source[val]['label'] = data['label']
                elif 'action' in data and data['action'] == ActionType.DEL.value:
                    del source[val]
                    val = 0
                    index_array[-1] = val
                    if len(source)==0:
                        break
            path_str = path_str + ('' if idx==0 else '/') + source[val]['label']
            self.data['type'] = source[val]['type']
            if 'items' in source[val]:
                source = source[val]['items']
                self.data['items'] = source
                list_item = {}
                for idy, item in enumerate(self.data['items']):
                    if item['type'] in list_item:
                        list_item[item['type']] = list_item[item['type']] + 1
                    else:
                        list_item[item['type']] = 1
                    self.data['items'][idy]['layer'] = layer + 1
                count_data_items = [{'type':k, 'label':v} for k, v in list_item.items()]
            else:
                del self.data['items']
                self.data['content'] = source[val]['content']
                source = []
        self.data['index'] = index_array
        self.data['index_array'] = index_array
        self.data['label'] = path_str
        self.data['layer'] = layer
        if 'index' in data:
            if isinstance(data['index'], list):
                current_index = data['index'][-1]
            else:
                current_index = data['index']
        else:
            current_index = index_array[-1]
        data = self.data.copy()
        data['index'] = current_index
        count_data = data.copy()
        if 'action' not in data or data['action'] == ActionType.NONE.value:
            if 'items' in data:
                pub.sendMessage(self.event_name[0], data=data)
        if 'action' in data:
            if data['action'] == ActionType.COUNTING.value:
                if data['type'] == PanelType.SECTION.value:
                    count_data['items'] = count_data_items
            elif data['action'] == ActionType.DEL.value:
                pub.sendMessage('data_changedTree', data=self.ori_data)
            count_data['clickable'] = False
            pub.sendMessage(self.event_name[1], data=count_data)

class Controller:
    def __init__(self):
        self.size = wx.Size(1000, 400)
        self.model = Model()
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


if __name__ == "__main__":
    app = wx.App()
    c = Controller()
    sys.stdout = sys.__stdout__
    app.MainLoop()