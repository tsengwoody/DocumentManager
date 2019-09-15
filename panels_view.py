import wx
from pubsub import pub

from enums import ImageIdEnum, InputType, PanelType, ConstValue
from toolbar_view import fileMenuView
from component_view import SectionPanel, TextPanel, MathmlPanel

# Debug
import pprint
import json
import logging

logging.basicConfig(
    handlers=[logging.FileHandler("./execute.log", 'a+', 'utf-8'), ],
    level=logging.DEBUG,
    format="[%(filename)15s:%(lineno)3s - %(funcName)20s() ] %(levelno)s%(asctime)15s %(threadName)5s %(message)s",
    datefmt='%Y/%m/%d %I:%M:%S %p'
)

class PanelView(wx.Panel):
    def __init__(self, parent, title, data, pos=(200, 000), size=wx.Size(600, 200), is_count_total=False):
        wx.Panel.__init__(self, parent, wx.ID_ANY, pos, size, style = wx.BORDER_THEME | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
        self.parent = parent
        self.type = InputType.PANEL
        self.data = data
        self.fileMenu = fileMenuView(self)
        self.is_count_total = is_count_total
        self.insideItems = wx.BoxSizer(wx.HORIZONTAL)
        self.SetBackgroundColour( wx.Colour( 112, 186, 248 ) )
        self.setData(self.data)
        pub.subscribe(self.setData, "data_changed")

    def setData(self, data):
        print("data msg in panel view:", data)
        self.label = data['label']
        self.type = data['type']
        if self.is_count_total==True:
            if 'items' in data:
                list_item = {}
                for item in data['items']:
                    if item['type'] in list_item:
                        list_item[item['type']] = list_item[item['type']] + 1
                    else:
                        list_item[item['type']] = 1
                self.contents = [{'type':k, 'label':v} for k, v in list_item.items()]
                self.data = data
            elif 'content' in data:
                self.contents = data['content']
        else:
            if 'items' not in data:
                return
            elif ConstValue.SKIP.value in data and data[ConstValue.SKIP.value]==ConstValue.SKIP.value:
                return
            self.contents = data['items']
            if 'current_folder_layer' not in data:
                data['current_folder_layer'] = 0
            for idx, val in enumerate(self.contents):
                data['items'][idx]['current_folder_layer'] = data['current_folder_layer'] + 1
            self.data = data
        try:
            self.panelItem.Destroy()
        except AttributeError:
            print("there is no created panelItem")
        self.panelItem = self.updatePanel(title=self.label, content=self.contents, _type=self.type, data=self.data)
        self.insideItems.Add(self.panelItem, 1, wx.EXPAND|wx.ALL)
        self.panelItem.SetSize(self.Size)
        if self.is_count_total==False:
            if hasattr(self.panelItem, "getList"):
                lst = self.panelItem.getList()
                lst.SetItemState(0, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
                self.SetFocus()
    
    def updatePanel(self, title, content, _type, data):
        self.is_set_eventbind = not self.is_count_total
        if _type == PanelType.SECTION.value:
            return SectionPanel(parent=self, title=title, content=content, _type=_type, data=data, eventParent=self)
        elif _type == PanelType.TEXT.value:
            return TextPanel(parent=self, title=title, content=content, _type=_type, data=data, eventParent=self)
        elif _type == PanelType.MATH.value:
            return MathmlPanel(parent=self, title=title, content=content, _type=_type, data=data, eventParent=self)