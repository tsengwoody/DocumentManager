import wx
from pubsub import pub
from dm_enum import InputType

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
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.activeItem, self)

        self.root = self.AddRoot("root") 
        self.setData(data)
        pub.subscribe(self.setData, "data_changedTree")

    def activeItem(self, evt):
        item = evt.GetItem()
        pyData = self.GetItemData(item)
        index = pyData[1]
        label = self.GetItemText(item)
        pub.sendMessage("data_changing", data={'type': InputType.PANEL, 'index': index, 'label': label})


    def setData(self, data):
        self.data = data['obj']
        self.DeleteAllItems()
        print("data msg in tree view:", self.data)
        for index, item in enumerate( self.data ):
            # 加入左邊 tree 的 Item 中
            childID = self.AppendItem(self.root, item.label, 0)
            self.SetPyData(childID, (item.label, index))
 