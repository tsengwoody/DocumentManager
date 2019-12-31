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


class ButtonPanel:
	def buttonData(self):
		return []

	def createButtonPanel(self, orientation):
		self.buttons = []
		button_panel = self.createButtonBar(0, orientation)
		button_sizer = wx.BoxSizer(getattr(wx, orientation))
		for button in self.buttons:
			button_sizer.Add(button, 1, wx.EXPAND | wx.ALL, border=1)

		button_panel.SetSizer(button_sizer)
		button_panel.Fit()
		return button_panel

	def createButtonBar(self, sPos, orientation):
		panel = wx.Panel(self)
		dPos = 0
		if orientation == 'HORIZONTAL':
			for item in self.buttonsData:
				pos = (dPos, sPos)
				button = self.buildOneButton(panel, label=item['label'], pos=pos, action=item['action'])
				self.buttons.append(button)
				dPos += button.GetSize().width
		elif orientation == 'VERTICAL':
			for item in self.buttonsData:
				pos = (sPos, dPos)
				button = self.buildOneButton(panel, label=item['label'], pos=pos, action=item['action'])
			self.buttons.append(button)
			dPos += button.GetSize().height

		return panel

	def buildOneButton(self, parent, label, pos, action):
		button = wx.Button(parent, -1, label=label, pos=pos)
		button.Bind(wx.EVT_BUTTON, action)
		return button


class SectionPanel(wx.Panel, ButtonPanel):
	def __init__(self, parent, content):
		wx.Panel.__init__(self, parent, wx.ID_ANY, (0, 0), (0, 0))
		self.content = content

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

		self.button_panel = self.createButtonPanel(orientation='HORIZONTAL')
		self.bsizer = wx.BoxSizer(wx.VERTICAL)
		self.bsizer.Add(self.lst, 1, wx.EXPAND | wx.ALL, border=5)
		self.bsizer.Add(self.button_panel, 0, wx.EXPAND | wx.ALL)
		self.SetSizer(self.bsizer)

	@property
	def buttonsData(self):
		return [
			{
				'id': 'enter',
				'label': _('Enter'),
				'type': 'button',
				'action': self.onEnter,
			},
			{
				'id': 'export',
				'label': _('Export'),
				'type': 'button',
				'action': self.onExport,
			},
		]

	def onEnter(self, event):
		print('on enter')

	def onExport(self, event):
		print('on export')


class TextPanel(wx.Panel, ButtonPanel):
	def __init__(self, parent, content):
		wx.Panel.__init__(self, parent, wx.ID_ANY, (0, 0), (0, 0))
		self.data = content['data']
		self.contentText = wx.TextCtrl(self, -1, size=(300, 300), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.EXPAND)
		# self.contentText = wx.TextCtrl(self, -1, size=(300, 300), style=wx.TE_READONLY | wx.EXPAND)
		self.contentText.SetValue(self.data['content'])


		self.button_panel = self.createButtonPanel(orientation='HORIZONTAL')
		self.bsizer = wx.BoxSizer(wx.VERTICAL)
		self.bsizer.Add(self.contentText, 1, wx.EXPAND | wx.ALL, border=5)
		self.bsizer.Add(self.button_panel, 0, wx.EXPAND | wx.ALL)
		self.SetSizer(self.bsizer)

	@property
	def buttonsData(self):
		return [
			{
				'id': 'edit',
				'label': _('Edit'),
				'type': 'button',
				'action': self.onEdit,
			},
			{
				'id': 'export',
				'label': _('Export'),
				'type': 'button',
				'action': self.onExport,
			},
		]

	def onEdit(self, event):
		# from xml.etree.ElementTree import tostring
		# import asciimathml

		entryDialog = wx.TextEntryDialog(
			self, _("update content:"), value=self.content, style=wx.TE_MULTILINE | wx.OK | wx.CANCEL
		)
		if entryDialog.ShowModal() == wx.ID_OK:
			textValue = entryDialog.GetValue()
			self.content = textValue

	def onExport(self, event):
		print('on export')


class MathmlPanel(wx.Panel, ButtonPanel):
	def __init__(self, parent, content):
		wx.Panel.__init__(self, parent, wx.ID_ANY, (0, 0), (0, 0))
		self.html_panel = HtmlPanel(parent=self, content=content['data'])
		self.content = content
		# self.treeArea = wx.TreeCtrl(
		# self, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.EXPAND
		# )
		# self.MathmlToTree()

		self.button_panel = self.createButtonPanel(orientation='VERTICAL')
		self.bsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.bsizer.Add(self.html_panel, 1, wx.EXPAND | wx.ALL, border=5)
		self.bsizer.Add(self.button_panel, 0, wx.EXPAND | wx.ALL)
		self.SetSizer(self.bsizer)

	@property
	def buttonsData(self):
		return [
			{
				'id': 'edit',
				'label': _('Edit'),
				'type': 'button',
				'action': self.onEdit,
			},
			{
				'id': 'interaction',
				'label': _('Interaction'),
				'type': 'button',
				'action': self.onInteraction,
			},
		]

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

	def onEdit(self, event):
		from xml.etree.ElementTree import tostring
		import asciimathml
		entryDialog = wx.TextEntryDialog(
			self, _("update content:"), value=self.content, style=wx.TE_MULTILINE | wx.OK | wx.CANCEL
		)
		if entryDialog.ShowModal() == wx.ID_OK:
			asciimath = entryDialog.GetValue()
			mathMl = tostring(asciimathml.parse(asciimath))
			self.content = mathMl

	def onInteraction(self, evt):
		pass

	def OnRawdataToClip(self, evt):
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(wx.TextDataObject(self.content))
			wx.TheClipboard.Close()


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
			{
				'key': [wx.WXK_LEFT],
				'action': self.onKeyLeftArrow,
			},
			{
				'key': [wx.WXK_RIGHT],
				'action': self.onKeyRightArrow,
			},
		]
		self.clipboard = None

		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.fileMenu.onEnter)
		self.Bind(wx.EVT_TEXT_ENTER, self.fileMenu.onEnter)
		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelectedItem)
		self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onDeselectedItem)

		pub.subscribe(self.setData, 'current_section')
		pub.subscribe(self.setFocusListItem, 'pointer_raw_data')

	'''def update(self, event):
		# index = event.GetId()
		index = self.GetFirstSelected()
		self.EditLabel(index)'''

	def getList(self):
		return self

	def setFocusListItem(self, data):
		self.SetFocus()
		if data:
			index = data['index_path'][-1]
			if not index == -1:
				self.SingleSelect(index)
				self.Focus(index)
			else:
				self.UnSelect()
				self.Focus(0)

	def setData(self, data):
		self.current_section = data
		self.DeleteAllItems()
		for item in data['data']['items']:
			index = data['data']['items'].index(item)
			wxitem = self.InsertItem(index, f"{item['label']}", ImageIdEnum.typeToEnum(item['type']))
			self.SetPyData(wxitem, {
				'index_path': item['index_path'],
				'label': item['label'],
				'type': item['type'],
				'content': item['content'] if 'content' in item else '',
				'items': item['items'] if 'items' in item else [],
			})

		self.SetFocus()

	def onSelectedItem(self, event):
		item = event.GetItem()
		index = item.GetId()
		data = {'index_path': self.current_section['index_path'] + [index]}
		pub.sendMessage('set_index_path', data=data)

	def onDeselectedItem(self, event):
		data = {'index_path': self.current_section['index_path'] + [-1]}
		pub.sendMessage('set_index_path', data=data)

	def onKeyLeftArrow(self, event):
		index = self.GetFirstSelected()
		index = 0 if index == -1 else index
		if index > 0:
			index = index - 1
			self.SingleSelect(index)

	def onKeyRightArrow(self, event):
		index = self.GetFirstSelected()
		index = 0 if index == -1 else index
		if index < len(self.current_section['data']['items']) - 1:
			index = index + 1
			self.SingleSelect(index)

	def UnSelect(self):
		for x in range(self.GetItemCount()):
			self.Select(x, on=0)

	def SingleSelect(self, index):
		for x in range(self.GetItemCount()):
			if x == index:
				self.Select(x, on=1)
			else:
				self.Select(x, on=0)


class CurrentSectionPanel(wx.Panel):
	def __init__(self, parent, data):
		wx.Panel.__init__(self, parent, wx.ID_ANY, (0, 0), (0, 0))

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

		for item in data['data']['items']:
			index = data['data']['items'].index(item)
			wxitem = self.lst.InsertItem(index, f"{item['label']}", ImageIdEnum.typeToEnum(item['type']))
			self.lst.SetPyData(wxitem, {
				'index_path': item['index_path'],
				'label': item['label'],
				'type': item['type'],
				'content': item['content'] if 'content' in item else '',
				'items': item['items'] if 'items' in item else [],
			})

		self.lst.current_section = data

		self.bsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.bsizer.Add(self.lst, 1, wx.EXPAND | wx.ALL, border=5)
		self.SetSizer(self.bsizer)


class RightTopPanel(wx.Panel):
	def __init__(self, parent, data, pos=(200, 000), size=wx.Size(600, 200)):
		wx.Panel.__init__(
			self, parent, wx.ID_ANY, pos, size, style=wx.BORDER_THEME | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND
		)
		self.insideItems = wx.BoxSizer(wx.HORIZONTAL)
		self.SetBackgroundColour(wx.Colour(112, 186, 248))

		self.panelItem = CurrentSectionPanel(parent=self, data=data)
		self.insideItems.Add(self.panelItem, 1, wx.EXPAND | wx.ALL)
		self.panelItem.SetSize(self.Size)


class RightBottomPanel(wx.Panel):
	def __init__(self, parent, data, pos=(200, 000), size=wx.Size(600, 200)):
		wx.Panel.__init__(
			self, parent, wx.ID_ANY, pos, size, style=wx.BORDER_THEME | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND
		)
		self.current_section_index_path = None
		self.current_section_data = None
		self.pointer_index_path = None
		self.pointer_data = None
		self.insideItems = wx.BoxSizer(wx.HORIZONTAL)
		self.SetBackgroundColour(wx.Colour(112, 186, 248))
		pub.subscribe(self.setData, 'pointer_raw_data')
		pub.subscribe(self.setCurrentSection, 'current_section')

	def setData(self, data):
		if data:
			self.pointer_index_path = data['index_path']
			self.pointer_data = data['data']
		else:
			self.pointer_index_path = None
			self.pointer_data = None
		self.setPanel()

	def setCurrentSection(self, data):
		self.current_section_index_path = data['index_path']
		self.current_section_data = data['data']
		self.setPanel()

	def setPanel(self):
		if self.pointer_index_path and self.pointer_data:
			data = {
				'index_path': self.pointer_index_path,
				'data': self.pointer_data,
			}
		else:
			data = {
				'index_path': self.current_section_index_path,
				'data': self.current_section_data,
			}
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
