import wx
from pubsub import pub

from enums import ImageIdEnum, InputType
from asciimathml import parse

class fileMenuView(wx.Menu):
    def __init__(self, parent):
        wx.Menu.__init__(self)
        self.parent = parent
        self.Append(wx.ID_ANY,  "Add folder")
        self.Append(wx.ID_ANY,  "Update folder")
        
        menu_delete=self.Append(wx.ID_ANY,  "Delete folder")
        self.Bind(wx.EVT_MENU, self.OnMenuDelete, menu_delete)

        self.Append(wx.ID_ANY,  "Import")
        menu_export=self.Append(wx.ID_ANY,  "Export")
        self.Bind(wx.EVT_MENU, self.OnMenuExport, menu_export)

    def OnMenuDelete(self, event):
        parent = self.parent
        self.OnDelete(event, parent)

    def OnDelete(self, event, parent):        
        caption = "即將刪除"
        message = "確認是否刪除?"
        dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_OK:
            lst = parent.panelItem.getList()
            item = lst.GetFocusedItem()
            if item != -1:
                lst.DeleteItem(item)
                return True
            return False

    def OnMenuExport(self, event):
        parent = self.parent
        self.OnExport(event, parent)

    def OnExport(self, event, parent):
        with wx.FileDialog(parent, "Save export file", wildcard="export files (*.json)|*.json",
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w', encoding="utf-8") as file:
                    file.write(parent.content)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)        

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
        if len(self.index_array) > 2:
            self.index_array.pop()
            self.index_array.pop()
            pub.sendMessage("data_changing", data={'type': InputType.PANEL.value, 'current_folder_layer': self.data['current_folder_layer']-2,'index': self.index_array[-1]})


       
