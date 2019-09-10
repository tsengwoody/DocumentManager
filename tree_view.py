import wx
from toolbar_view import fileMenuView
from pubsub import pub
from enums import InputType

class TreeView(wx.TreeCtrl):
    id = 1
    def __init__(self, parent, data):
        self.panel = wx.Panel(parent, wx.ID_ANY, (0, 0), size=(parent.Size.width/4, parent.Size.height), style = wx.BORDER_THEME | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
        wx.TreeCtrl.__init__(self, self.panel, self.id, wx.DefaultPosition, (parent.Size.width/4, parent.Size.height), wx.TR_HIDE_ROOT|wx.TR_DEFAULT_STYLE)

        # image array
        il = wx.ImageList(36, 36, True)
        docBitmap = wx.Bitmap("./icons/documents.png", wx.BITMAP_TYPE_PNG)
        il.Add(docBitmap)
        self.AssignImageList(il)
        self.fileMenu = fileMenuView(self.panel)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftMouseDown, self)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onItemRightClick, self)
        #self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSelChanged, self)

        self.root = self.AddRoot("root") 
        self.setData(data)
        pub.subscribe(self.setData, "data_changedTree")

    def onLeftMouseDown(self, event):
        item, flags = self.HitTest(event.GetPosition())
        self.active_item(event, item)

    def onSelChanged(self, event):
        item = event.GetItem()
        self.active_item(event, item)
    
    def active_item(self, event, item):
        if item.ID is not None:
            pyData = self.GetItemData(item)
            index = pyData[1]    
            if index != wx.NOT_FOUND: 
                self.SelectItem(item)       
                label = self.GetItemText(item)
                pub.sendMessage("data_changing", data={'type': InputType.PANEL.value, 'index': index, 'label': label, 'current_folder_layer': 0})

    def onItemRightClick(self, event):
        item, flags = self.HitTest(event.GetPosition())
        if item.ID is not None:
            pyData = self.GetItemData(item)
            index = pyData[1]
            if index != wx.NOT_FOUND: 
                self.SelectItem(item)
                self.active_item(event, item)
                if self.fileMenu.Window is None:
                    self.PopupMenu(self.fileMenu, event.GetPosition())
        event.Skip()

    def setData(self, data):
        self.data = data['items']
        self.DeleteAllItems()
        print("data msg in tree view:", self.data)
        for index, item in enumerate( self.data ):
            label = item['label']
            childID = self.AppendItem(self.root, label, 0)
            self.SetPyData(childID, (label, index))
 