import wx
from pubsub import pub

from enums import ImageIdEnum
from dm_enum import InputType
from asciimathml import parse

class ToolBarView(wx.Panel):
    def __init__(self, parent, data):
        wx.Panel.__init__(self, parent, wx.ID_ANY, pos=(parent.Size.width/4, 0), size=(parent.Size.width*3/4, 69), style = wx.TAB_TRAVERSAL|wx.EXPAND)
        self.parent = parent
        self.data = data
        self.index_array = data['index']
        self.current_folder_layer = 0
        backPathBitmap = wx.Bitmap("./icons/backPath.png", wx.BITMAP_TYPE_PNG)
        self.backPathbtn = wx.Button(self, -1, style=wx.BU_BOTTOM | wx.BU_NOTEXT)
        self.backPathbtn.SetBitmap(backPathBitmap, wx.BOTTOM)
        self.backPathbtn.SetLabel("上一層")
        self.toolbar = wx.BoxSizer(wx.VERTICAL)
        self.toolbar.Add(self.backPathbtn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)                   
        self.pathText = wx.StaticText(self, -1, data['label'], size=(-1, -1), style=wx.ALIGN_CENTRE_HORIZONTAL | wx.BU_NOTEXT)
        self.toolbar.Add(self.pathText, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL)
        self.SetSizer(self.toolbar)
        self.Fit()
        self.backPathbtn.Bind(wx.EVT_BUTTON, self.backPath)
        pub.subscribe(self.setData, "data_changed")

    def setData(self, data):
        try:
            self.current_folder_layer = data['current_folder_layer']
            self.index_array.insert(self.current_folder_layer,data['index'])
            del self.index_array[self.current_folder_layer+1:] 
            self.pathText.SetLabel(data['label'])
        except AttributeError:
            print("there is no created pathText")

    def backPath(self, event):
        print("back to previous path")
        if len(self.index_array) > 1:
            self.index_array.pop()
            pub.sendMessage("data_changing", data={'type': InputType.PANEL.value, 'current_folder_layer': self.data['current_folder_layer']-1,'index': self.index_array[-1]})


       
