import wx
import wx.html2
from pubsub import pub
from enums import ImageIdEnum, InputType, PanelType, ActionType
from module.asciimathml import parse
from View.toolbar_view import fileMenuView
from View.utility import Hotkey


class HtmlPanel(wx.Panel):
	def __init__(self, parent, content):
		wx.Panel.__init__(self, parent, wx.ID_ANY, (0, 0), (0, 0))
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.browser = wx.html2.WebView.New(self)
		self.browser.SetPage(content['content'], "")
		sizer.Add(self.browser, 1, wx.EXPAND | wx.ALL, 5)
		self.SetSizer(sizer)


class SectionPanel(wx.Panel):
	def __init__(self, parent, content):
		wx.Panel.__init__(self, parent, wx.ID_ANY, (0, 0), (0, 0))
		self.content = content
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

		self.lst = wx.ListCtrl(self, -1, size=(300, 600), style=wx.LC_ICON | wx.LC_AUTOARRANGE)
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

		self.bsizer_btn = wx.BoxSizer(wx.VERTICAL)
		for btn in self.buttons:
			self.bsizer_btn.Add(btn, proportion=1, flag=wx.EXPAND | wx.ALL, border=1)

		self.button_panel.SetSizer(self.bsizer_btn)
		self.button_panel.Fit()

		self.bsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.bsizer.Add(self.lst, 1, wx.EXPAND | wx.ALL, border=5)
		self.bsizer.Add(self.button_panel, 0, wx.EXPAND | wx.ALL)

		self.SetSizer(self.bsizer)


class TextPanel(wx.Panel):
	def __init__(self, parent, content):
		wx.Panel.__init__(self, parent, wx.ID_ANY, (0, 0), (0, 0))
		self.content = content
		self.buttons = []
		# self.contentText = wx.TextCtrl(self, -1, size=(300, 300), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.EXPAND)
		self.contentText = wx.TextCtrl(self, -1, size=(300, 300), style=wx.TE_READONLY | wx.EXPAND)
		self.button_panel = wx.Panel(self)

		self.createButtonBar(self.button_panel, yPos=0)

		self.bsizer_btn = wx.BoxSizer(wx.HORIZONTAL)
		for btn in self.buttons:
			self.bsizer_btn.Add(btn, 1, wx.EXPAND | wx.ALL, border=1)

		self.button_panel.SetSizer(self.bsizer_btn)
		self.button_panel.Fit()
		self.bsizer = wx.BoxSizer(wx.VERTICAL)
		self.bsizer.Add(self.contentText, 1, wx.EXPAND | wx.ALL, border=5)
		self.bsizer.Add(self.button_panel, 0, wx.EXPAND | wx.ALL)

		self.SetSizer(self.bsizer)

	def onPanelActivated(self):
		self.Show()

	def onPanelDeactivated(self):
		self.Hide()

	def OnRewrite(self, evt):
		# from xml.etree.ElementTree import tostring
		# import asciimathml

		entryDialog = wx.TextEntryDialog(
			self, _("update content:"), value=self.content, style=wx.TE_MULTILINE | wx.OK | wx.CANCEL
		)
		if entryDialog.ShowModal() == wx.ID_OK:
			textValue = entryDialog.GetValue()
			self.content = textValue

	def OnExport(self, event):
		pass

	def buttonData(self):
		return (
			(("Rewrite"), self.OnRewrite),
			(("Export"), self.OnExport)
		)

	def createButtonBar(self, panel, yPos=0):
		xPos = 0
		for eachLabel, eachHandler in self.buttonData():
			pos = (xPos, yPos)
			button = self.buildOneButton(panel, eachLabel, eachHandler, pos)
			self.buttons.append(button)
			xPos += button.GetSize().width

	def buildOneButton(self, parent, label, handler, pos=(0, 0)):
		button = wx.Button(parent, -1, label, pos)
		self.Bind(wx.EVT_BUTTON, handler, button)
		return button


class MathmlPanel(wx.Panel):
	def __init__(self, parent, content):
		wx.Panel.__init__(self, parent, wx.ID_ANY, (0, 0), (0, 0))
		self.html_panel = HtmlPanel(parent=self, content=content['data'])
		self.content = content
		self.buttons = []
		# self.treeArea = wx.TreeCtrl(
		# self, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.EXPAND
		# )
		# self.MathmlToTree()

		self.button_panel = wx.Panel(self)
		self.createButtonBar(self.button_panel, xPos=0)

		self.bsizer_btn = wx.BoxSizer(wx.VERTICAL)
		for btn in self.buttons:
			self.bsizer_btn.Add(btn, 1, wx.EXPAND | wx.ALL, border=1)

		self.button_panel.SetSizer(self.bsizer_btn)
		self.button_panel.Fit()

		self.bsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.bsizer.Add(self.html_panel, 1, wx.EXPAND | wx.ALL, border=5)
		self.bsizer.Add(self.button_panel, 0, wx.EXPAND | wx.ALL)

		self.SetSizer(self.bsizer)

	def MathmlToTree(self):
		if self.content:
			self.mathmlObj = parse(self.content)
			for rootMathObj in self.mathmlObj:
				rootId = self.treeArea.AddRoot(
					text=rootMathObj.tag,
					data=rootMathObj
				)
				self._recursive(rootMathObj, rootId)

	def _recursive(self, obj, rootId):
		if len(obj.getchildren()) > 0:  # 如果底下還有 children 的話才跑迴圈
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
		entryDialog = wx.TextEntryDialog(
			self, _("update content:"), value=self.content, style=wx.TE_MULTILINE | wx.OK | wx.CANCEL
		)
		if entryDialog.ShowModal() == wx.ID_OK:
			asciimath = entryDialog.GetValue()
			mathMl = tostring(asciimathml.parse(asciimath))
			self.content = mathMl

	def OnInteraction(self, evt):
		pass

	def OnRawdataToClip(self, evt):
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(wx.TextDataObject(self.content))
			wx.TheClipboard.Close()

	def buttonData(self):
		return (
			(("Rewrite"), self.OnRewrite),
			(("Interaction"), self.OnInteraction),
			(("Copy"), self.OnRawdataToClip),
		)

	def createButtonBar(self, panel, xPos=0):
		yPos = 0
		for eachLabel, eachHandler in self.buttonData():
			pos = (xPos, yPos)
			button = self.buildOneButton(panel, eachLabel, eachHandler, pos)
			self.buttons.append(button)
			yPos += button.GetSize().height

	def buildOneButton(self, parent, label, handler, pos=(0, 0)):
		button = wx.Button(parent, -1, label, pos)
		self.Bind(wx.EVT_BUTTON, handler, button)
		return button


class ListCtrl(wx.ListCtrl):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.id = 0
		self.map = {}

		self.Bind(wx.EVT_LIST_DELETE_ITEM, self.OnDeleteItem)
		self.Bind(wx.EVT_LIST_DELETE_ALL_ITEMS, self.OnDeleteAllItems)

	def SetPyData(self, item, data):
		self.map[self.id] = data
		self.SetItemData(item, self.id)
		self.id += 1

	def GetPyData(self, item):
		item_id = self.GetItemData(item)
		return self.map[item_id]

	def SortPyItems(self, fn):
		from functools import wraps

		@wraps(fn)
		def wrapper(a, b):
			return fn(self.map[a], self.map[b])

		self.SortItems(wrapper)

	def OnDeleteItem(self, event):
		try:
			del self.map[event.Data]
		except KeyError:
			pass
		event.Skip()

	def OnDeleteAllItems(self, event):
		self.map.clear()
		event.Skip()


class FolderView(ListCtrl, Hotkey):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		Hotkey.__init__(self)
		self.fileMenu = fileMenuView(self)
		self.key_map_action = [
			{
				'key': [wx.WXK_SHIFT, wx.WXK_CONTROL, ord('N')],
				'action': self.fileMenu.onAdd,
			},
			{
				'key': [wx.WXK_F2],
				'action': self.fileMenu.onUpdate,
			},
			{
				'key': [wx.WXK_DELETE],
				'action': self.fileMenu.onRemove,
			},
			{
				'key': [wx.WXK_CONTROL, ord('X')],
				'action': self.fileMenu.onCut,
			},
			{
				'key': [wx.WXK_CONTROL, ord('C')],
				'action': self.fileMenu.onCopy,
			},
			{
				'key': [wx.WXK_CONTROL, ord('V')],
				'action': self.fileMenu.onPaste,
			},
			{
				'key': [wx.WXK_SHIFT, wx.WXK_CONTROL, wx.WXK_LEFT],
				'action': self.fileMenu.onMoveUp,
			},
			{
				'key': [wx.WXK_SHIFT, wx.WXK_CONTROL, wx.WXK_RIGHT],
				'action': self.fileMenu.onMoveDown,
			},
			{
				'key': [wx.WXK_BACK],
				'action': self.fileMenu.onBack,
			},
		]
		self.clipboard = None

	'''def update(self, event):
		# index = event.GetId()
		index = self.GetFirstSelected()
		self.EditLabel(index)'''

	def getList(self):
		return self


class CurrentSectionPanel(wx.Panel):
	def __init__(self, parent, data):
		wx.Panel.__init__(self, parent, wx.ID_ANY, (0, 0), (0, 0))
		self.current_section = data
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

		self.lst = FolderView(self, -1, size=(300, 600), style=wx.LC_ICON | wx.LC_AUTOARRANGE)
		# 將剛剛的圖片陣列放入 左邊的 ListCtrl 中，這樣新增 item 時就可以直接說我要加入第幾種圖片就可以了
		self.lst.AssignImageList(il, wx.IMAGE_LIST_NORMAL)

		for item in self.current_section['data']['items']:
			index = self.current_section['data']['items'].index(item)
			wxitem = self.lst.InsertItem(index, f"{item['label']}", ImageIdEnum.typeToEnum(item['type']))
			self.lst.SetPyData(wxitem, {
				'index_path': item['index_path'],
				'label': item['label'],
				'type': item['type'],
				'content': item['content'] if 'content' in item else '',
				'items': item['items'] if 'items' in item else [],
			})
			# print(self.lst.GetPyData(wxitem))

		# ==============================================================
		# SectionPanel 的按鈕們
		# ==============================================================
		self.button_panel = wx.Panel(self)
		# self.createButtonBar(self.button_panel, xPos = 0)

		self.bsizer_btn = wx.BoxSizer(wx.VERTICAL)
		for btn in self.buttons:
			self.bsizer_btn.Add(btn, proportion=1, flag=wx.EXPAND | wx.ALL, border=1)

		self.button_panel.SetSizer(self.bsizer_btn)
		self.button_panel.Fit()

		self.bsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.bsizer.Add(self.lst, 1, wx.EXPAND | wx.ALL, border=5)
		self.bsizer.Add(self.button_panel, 0, wx.EXPAND | wx.ALL)
		self.SetSizer(self.bsizer)

		self.lst.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDBClickItem)
		self.lst.Bind(wx.EVT_TEXT_ENTER, self.onDBClickItem)
		self.lst.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelectedItem)
		self.lst.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onDeselectedItem)

	def setData(self, data):
		self.lst.DeleteAllItems()
		self.current_section = data
		for item in self.current_section['data']['items']:
			index = self.current_section['data']['items'].index(item)
			wxitem = self.lst.InsertItem(index, f"{item['label']}", ImageIdEnum.typeToEnum(item['type']))
			self.lst.SetPyData(wxitem, {
				'index_path': item['index_path'],
				'label': item['label'],
				'type': item['type'],
				'content': item['content'] if 'content' in item else '',
				'items': item['items'] if 'items' in item else [],
			})

	def getList(self):
		return self.lst

	def onDBClickItem(self, event):
		self.lst.fileMenu.onEnter(event)

	def onSelectedItem(self, event):
		item = event.GetItem()
		index = item.GetId()
		data = {'index_path': self.current_section['index_path'] + [index]}
		pub.sendMessage('set_index_path', data=data)

	def onDeselectedItem(self, event):
		data = {'index_path': self.current_section['index_path'] + [-1]}
		pub.sendMessage('set_index_path', data=data)

	def buttonData(self):
		return (
			(("enter"), self.enterSection),
			(("Export"), self.exportData)
		)

	def createButtonBar(self, panel, xPos=0):
		yPos = 0
		for eachLabel, eachHandler in self.buttonData():
			pos = (xPos, yPos)
			button = self.buildOneButton(panel, eachLabel, eachHandler, pos)
			self.buttons.append(button)
			yPos += button.GetSize().height

	def buildOneButton(self, parent, label, handler, pos=(0, 0)):
		button = wx.Button(parent, -1, label, pos)
		button.Bind(wx.EVT_BUTTON, handler)
		return button


class RightTopPanel(wx.Panel):
	def __init__(self, parent, data, pos=(200, 000), size=wx.Size(600, 200)):
		wx.Panel.__init__(
			self, parent, wx.ID_ANY, pos, size, style=wx.BORDER_THEME | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND
		)
		self.data = data
		self.insideItems = wx.BoxSizer(wx.HORIZONTAL)
		self.SetBackgroundColour(wx.Colour(112, 186, 248))

		self.panelItem = CurrentSectionPanel(parent=self, data=data)
		self.insideItems.Add(self.panelItem, 1, wx.EXPAND | wx.ALL)
		self.panelItem.SetSize(self.Size)

		pub.subscribe(self.setData, 'current_section')

	def setData(self, data):
		self.panelItem.setData(data)
		lst = self.panelItem.getList()
		# lst.SetItemState(0, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
		lst.SetFocus()


class RightBottomPanel(wx.Panel):
	def __init__(self, parent, data, pos=(200, 000), size=wx.Size(600, 200)):
		wx.Panel.__init__(
			self, parent, wx.ID_ANY, pos, size, style=wx.BORDER_THEME | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND
		)
		self.data = data
		self.insideItems = wx.BoxSizer(wx.HORIZONTAL)
		self.SetBackgroundColour(wx.Colour(112, 186, 248))
		pub.subscribe(self.setData, 'pointer_raw_data')
		self.setData(self.data)

	def setData(self, data):
		if not data:
			return False
		try:
			self.panelItem.Destroy()
		except AttributeError:
			print("there is no created panelItem")
		except BaseException as e:
			print(str(e))

		type = data['data']['type']
		if type == PanelType.SECTION.value:
			count = {}
			for item in data['data']['items']:
				if item['type'] in count:
					count[item['type']] = count[item['type']] + 1
				else:
					count[item['type']] = 1

			content = []
			for key, value in count.items():
				content.append({
					'label': value,
					'type': key,
				})
		elif type == PanelType.TEXT.value:
			content = data
		elif type == PanelType.MATH.value:
			content = data

		self.panelItem = self.updatePanel(content=content, _type=type)
		self.insideItems.Add(self.panelItem, 1, wx.EXPAND | wx.ALL)
		self.panelItem.SetSize(self.Size)

	def updatePanel(self, content, _type):
		if _type == PanelType.SECTION.value:
			return SectionPanel(parent=self, content=content)
		elif _type == PanelType.TEXT.value:
			return TextPanel(parent=self, content=content)
		elif _type == PanelType.MATH.value:
			return MathmlPanel(parent=self, content=content)
