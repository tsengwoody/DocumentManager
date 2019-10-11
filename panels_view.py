import wx
from pubsub import pub

from enums import ImageIdEnum, InputType, PanelType
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
    def __init__(self, parent, title, data, pos=(200, 000), size=wx.Size(600, 200), event_name='data_changed'):
        wx.Panel.__init__(self, parent, wx.ID_ANY, pos, size, style = wx.BORDER_THEME | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
        self.parent = parent
        self.type = InputType.PANEL
        self.data = data
        self.is_set_eventbind = 'clickable' not in data or data['clickable']==True
        self.fileMenu = fileMenuView(self)
        self.insideItems = wx.BoxSizer(wx.HORIZONTAL)
        self.SetBackgroundColour( wx.Colour( 112, 186, 248 ) )
        pub.subscribe(self.setData, event_name)
        self.setData(self.data)

    def setData(self, data):
        print("data msg in panel view:", data)
        try:
            self.panelItem.Destroy()
        except AttributeError:
            print("there is no created panelItem")
        content = data['items'] if 'items' in data else data['content']
        self.panelItem = self.updatePanel(title=data['label'], content=content, _type=data['type'], data=data)
        self.insideItems.Add(self.panelItem, 1, wx.EXPAND|wx.ALL)
        self.panelItem.SetSize(self.Size)
        if 'clickable' not in data or data['clickable']==True:
            if hasattr(self.panelItem, "getList"):
                lst = self.panelItem.getList()
                lst.SetItemState(0, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
                self.SetFocus()
    
    def updatePanel(self, title, content, _type, data):
        if _type == PanelType.SECTION.value:
            return SectionPanel(parent=self, title=title, content=content, _type=_type, data=data, eventParent=self)
        elif _type == PanelType.TEXT.value:
            return TextPanel(parent=self, title=title, content=content, _type=_type, data=data, eventParent=self)
        elif _type == PanelType.MATH.value:
            return MathmlPanel(parent=self, title=title, content=content, _type=_type, data=data, eventParent=self)