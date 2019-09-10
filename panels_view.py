import wx
from pubsub import pub

from enums import ImageIdEnum, InputType, PanelType, ConstValue
from asciimathml import parse
from toolbar_view import fileMenuView

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
           

# ==========================================================================================
# SectionPanel
# 這邊需要顯示 這個 section 底下有多少的各種物件
# 例如: 有3個Section物件 、 有2個 Mathml 物件 等等
# enter 按鍵按下去時 需要 postEvent 到 parent 去更新 FolderPanel 的 PathText
# ==========================================================================================
class SectionPanel(wx.Panel):

    def __repr__(self):
        return f"<SectionPanel Name: {self.name}  Type: {self.type}>"

    def __init__(self, parent, title, content, _type, data, eventParent):
        wx.Panel.__init__(self, parent, wx.ID_ANY, (0, 0), (0, 0))
        self.name = title
        self.content = content
        self.type = _type
        self.data = data.copy()
        self.eventPanent = eventParent
        self.fileMenu = eventParent.fileMenu
        self.buttons = []

        
        # ======================================================================
        # 我的UI創建方法
        # ======================================================================
        # 檔案圖片列表
        il = wx.ImageList(36, 36, True)
        # 檔案圖片
        docBitmap = wx.Bitmap("./icons/documents.png", wx.BITMAP_TYPE_PNG)
        sectionBitmap = wx.Bitmap("./icons/documents.png", wx.BITMAP_TYPE_PNG)
        textBitmap = wx.Bitmap("./icons/text.png", wx.BITMAP_TYPE_PNG)
        mathBitmap = wx.Bitmap("./icons/math.png", wx.BITMAP_TYPE_PNG)
        # 檔案圖片 加入 圖片陣列
        # 這邊要照 ImageIdEnum 的順序加入
        il.Add(docBitmap)
        il.Add(sectionBitmap)
        il.Add(textBitmap)
        il.Add(mathBitmap)

        self.lst = wx.ListCtrl(self, -1, size=(300,600), style=wx.LC_ICON | wx.LC_AUTOARRANGE)
        # 將剛剛的圖片陣列放入 左邊的 ListCtrl 中，這樣新增 item 時就可以直接說我要加入第幾種圖片就可以了
        self.lst.AssignImageList(il, wx.IMAGE_LIST_NORMAL)


        for item in self.content:
            index = self.content.index(item)
            self.lst.InsertItem(index, f"{item['label']}", ImageIdEnum.typeToEnum(item['type']))
    
        # ==============================================================
        # SectionPanel 的按鈕們
        # ==============================================================
        self.button_panel = wx.Panel(self)
        # self.createButtonBar(self.button_panel, xPos = 0)
        self.modelBindView()

        self.bsizer_btn = wx.BoxSizer(wx.VERTICAL)
        for btn in self.buttons:
            self.bsizer_btn.Add(btn, proportion=1, flag=wx.EXPAND|wx.ALL, border=1)

        self.button_panel.SetSizer(self.bsizer_btn)
        self.button_panel.Fit()

        self.bsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bsizer.Add(self.lst, 1, wx.EXPAND|wx.ALL, border=5)
        self.bsizer.Add(self.button_panel, 0, wx.EXPAND|wx.ALL)

        self.SetSizer(self.bsizer)

        if self.eventPanent and self.eventPanent.is_set_eventbind == True:
            self.lst.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDBClickItem)
            self.lst.Bind(wx.EVT_TEXT_ENTER,self.onDBClickItem)  
            self.lst.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelectedItem)
            self.lst.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onItemRightClick)

        print(f"SectionPanel name: {self.name}")#, content: {self.content}")

    def getList(self):
        return self.lst

    def onDBClickItem(self, event):
        item = event.GetItem()
        index = item.GetId()
        if index != wx.NOT_FOUND:         
            self.sendItemMsg(index, custom_arg=ConstValue.CONTINUE.value)

    def onSelectedItem(self, event):
        item = event.GetItem()
        index = item.GetId()
        self.sendItemMsg(index)

    def onItemRightClick(self, event):
        item = event.GetItem()
        index = item.GetId()
        if index != wx.NOT_FOUND: 
            self.lst.Select(index)
            self.sendItemMsg(index)
            rect = self.lst.GetItemRect(index)
            if self.fileMenu.Window is None:
                self.PopupMenu(self.fileMenu, wx.Point(rect.Left+rect.Width/2, rect.Top+rect.Height/2))
        event.Skip()        

    def sendItemMsg(self, index, custom_arg=ConstValue.SKIP.value):
        data = self.data['items'][index]
        _type = data['type']
        label = data['label']
        if custom_arg==ConstValue.CONTINUE.value and _type == PanelType.SECTION.value:
            pub.sendMessage("data_changing", data={'type': InputType.PANEL.value, 'current_folder_layer': data['current_folder_layer'],'index': index, 'label': label})
        else:
            pub.sendMessage("data_changing", data={'type': InputType.PANEL.value, 'current_folder_layer': data['current_folder_layer'],'index': index, 'label': label, ConstValue.SKIP.value:ConstValue.SKIP.value})            

    def onPanelActivated(self, newdata=None):
        self.modelBindView(newdata)
        self.Show()

    def onPanelDeactivated(self):
        self.Hide()

    def modelBindView(self, newdata=None):
        # 有傳送新的data的話就更新 ItemPanel 的 data
        if newdata:
            self.data = newdata     
        # self.contentText.SetValue(self.content)

    def viewBindModel(self):
        """基本上就是更新自己的 content 資料"""
        self.content = self.contentText.GetValue()



    def buttonData(self):
        return (
            (("enter"), self.enterSection),
            (("Export"), self.exportData)
        )

    def createButtonBar(self, panel, xPos = 0):
        yPos = 0
        for eachLabel, eachHandler in self.buttonData():
            pos = (xPos, yPos)
            button = self.buildOneButton(panel, eachLabel,eachHandler, pos)
            self.buttons.append(button)
            yPos += button.GetSize().height

    def buildOneButton(self, parent, label, handler, pos=(0,0)):
        button = wx.Button(parent, -1, label, pos)
        button.Bind(wx.EVT_BUTTON, handler)
        return button

    def enterSection(self, event):
        print("on enterSection!")
        wx.PostEvent(self.eventPanent, event)
        
        wx.CallAfter(self.eventPanent.enterFromSectionItemPanel, event)
        
        event.Skip()


    def exportData(self, event):
        print("on Export Data!!")

        with wx.FileDialog(self, "Save export file", wildcard="export files (*.json)|*.json",
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w', encoding="utf-8") as f:
                    # file.write(self.content)
                    print(self.datas)
                    print(type(self.datas))

                    json.dump(self.datas, f, ensure_ascii=False)
            except IOError:
                wx.LogError(f"Cannot save current data in file: {pathname}.")

    @property
    def datas(self):
        return {
            'label': self.data.label,
            "type" : "section",
            'items': [
                item.data for item in self.data.items
            ],
        }



# ==========================================================================================
# TextPanel
# 這邊需要顯示 Text 物件底下的內容
# 例如: 有3個Section物件 、 有2個 Mathml 物件 等等
# Rewrite 時會更改 self.data 裡面的直
# 讓 未來輸出時可以使用 self.data 輸出
# ==========================================================================================
# 這邊應該要 依照不同的 Item Type 設定不同的
class TextPanel(wx.Panel):

    def __repr__(self):
        return f"<TextPanel Name: {self.name}  Type: {self.type}>"

    def __init__(self, parent, title, content, _type, data, eventParent):
        wx.Panel.__init__(self, parent, wx.ID_ANY, (0, 0), (0, 0))
        self.name = title
        self.content = content
        self.fileMenu = eventParent.fileMenu
        self.type = _type
        self.data = data
        self.buttons = []
        self.contentText = wx.TextCtrl(self, -1, size=(300, 300), style=wx.TE_READONLY|wx.EXPAND)
        self.button_panel = wx.Panel(self)

        self.createButtonBar(self.button_panel, yPos = 0)
        self.modelBindView()

        self.bsizer_btn = wx.BoxSizer(wx.HORIZONTAL)
        for btn in self.buttons:
            self.bsizer_btn.Add(btn, 1, wx.EXPAND|wx.ALL, border=1)


        self.button_panel.SetSizer(self.bsizer_btn)
        self.button_panel.Fit()

        self.bsizer = wx.BoxSizer(wx.VERTICAL)
        self.bsizer.Add(self.contentText, 1, wx.EXPAND|wx.ALL, border=5)
        self.bsizer.Add(self.button_panel, 0, wx.EXPAND|wx.ALL)

        self.SetSizer(self.bsizer)


    def onPanelActivated(self):
        self.Show()

    def onPanelDeactivated(self):
        self.Hide()

    def OnRewrite(self, evt):
        # from xml.etree.ElementTree import tostring
        # import asciimathml

        entryDialog = wx.TextEntryDialog(self, "輸入更改內容:", value=self.content, style=wx.TE_MULTILINE|wx.OK|wx.CANCEL)
        if entryDialog.ShowModal() == wx.ID_OK:
            textValue = entryDialog.GetValue()
            self.content = textValue
            self.modelBindView()

    def OnExport(self, event):
        parent = self
        self.fileMenu.OnExport(event, parent)

    def modelBindView(self):
        """Model 資料放回至 View 中"""
        self.contentText.SetValue(self.content)
        self.data['content'] = self.content

    def viewBindModel(self):
        self.content = self.contentText.GetValue()
        self.data['content'] = self.content

    def buttonData(self):
        return (
            (("Rewrite"), self.OnRewrite),
            (("Export"), self.OnExport)
        )

    def createButtonBar(self, panel, yPos = 0):
        xPos = 0
        for eachLabel, eachHandler in self.buttonData():
            pos = (xPos, yPos)
            button = self.buildOneButton(panel, eachLabel,eachHandler, pos)
            self.buttons.append(button)
            xPos += button.GetSize().width

    def buildOneButton(self, parent, label, handler, pos=(0,0)):
        button = wx.Button(parent, -1, label, pos)
        self.Bind(wx.EVT_BUTTON, handler, button)
        return button

    @property
    def datas(self):
        return {
            'label': self.data.label,
            "type" : "text",
            'content': self.data.content,
        }


# 這邊應該要 依照不同的 Item Type 設定不同的
class MathmlPanel(wx.Panel):

    def __repr__(self):
        return f"<MathmlPanel Name: {self.name}  Type: {self.type}>"

    def __init__(self, parent, title, content, _type, data, eventParent):
        wx.Panel.__init__(self, parent, wx.ID_ANY, (0, 0), (0, 0))
        self.name = title
        self.content = content
        self.data = data
        self.type = _type
        self.buttons = []
        self.treeArea = wx.TreeCtrl(
            self, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.EXPAND
        )
        self.MathmlToTree()


        self.button_panel = wx.Panel(self)
        self.createButtonBar(self.button_panel, xPos = 0)
        self.modelBindView()

        self.bsizer_btn = wx.BoxSizer(wx.VERTICAL)
        for btn in self.buttons:
            self.bsizer_btn.Add(btn, 1, wx.EXPAND|wx.ALL, border=1)

        self.button_panel.SetSizer(self.bsizer_btn)
        self.button_panel.Fit()

        self.bsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bsizer.Add(self.treeArea, 1, wx.EXPAND|wx.ALL, border=5)
        self.bsizer.Add(self.button_panel, 0, wx.EXPAND|wx.ALL)

        self.SetSizer(self.bsizer)

    def MathmlToTree(self):

        self.mathmlObj = parse(self.content)
        for rootMathObj in self.mathmlObj:
            rootId = self.treeArea.AddRoot(
                text=rootMathObj.tag,
                data=rootMathObj
            )
            self._recursive(rootMathObj, rootId)


    def _recursive(self, obj, rootId):
        if len(obj.getchildren()) > 0: # 如果底下還有 children 的話才跑迴圈
            for child in obj.getchildren():
                childId = self.treeArea.AppendItem(
                    parent=rootId,
                    text=child.tag,
                    data=child
                )
                self._recursive(child, childId)

    def onPanelActivated(self):
        self.Show()

    def onPanelDeactivated(self):
        self.Hide()

    def OnRewrite(self, evt):
        from xml.etree.ElementTree import tostring
        import asciimathml
        entryDialog = wx.TextEntryDialog(self, "輸入更改內容:", value=self.content, style=wx.TE_MULTILINE|wx.OK|wx.CANCEL)
        if entryDialog.ShowModal()==wx.ID_OK:
            asciimath = entryDialog.GetValue()
            mathMl = tostring(asciimathml.parse(asciimath))
            self.content = mathMl
            self.modelBindView()

    def OnInteraction(self, evt):
        pass

    def OnRawdataToClip(self, evt):
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.content))
            wx.TheClipboard.Close()


    def modelBindView(self):
        pass
        # self.contentText.SetValue(self.content)

    def viewBindModel(self):
        self.content = self.treeArea.GetValue()

    def buttonData(self):
        return (
            (("Rewrite"), self.OnRewrite),
            (("Interaction"), self.OnInteraction),
            (("Copy"), self.OnRawdataToClip),
        )

    def createButtonBar(self, panel, xPos = 0):
        yPos = 0
        for eachLabel, eachHandler in self.buttonData():
            pos = (xPos, yPos)
            button = self.buildOneButton(panel, eachLabel,eachHandler, pos)
            self.buttons.append(button)
            yPos += button.GetSize().height

    def buildOneButton(self, parent, label, handler, pos=(0,0)):
        button = wx.Button(parent, -1, label, pos)
        self.Bind(wx.EVT_BUTTON, handler, button)
        return button

    @property
    def datas(self):
        return {
            'label': self.name,
            "type" : "mathml",
            # 'content': self.content,
            'content': "HI~", #  太長縮短用
        }


__all__ = ["SectionPanel", "TextPanel", "MathmlPanel"]