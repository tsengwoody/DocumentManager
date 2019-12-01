import wx
from View.toolbar_view2 import fileMenuView2 as fileMenuView
from pubsub import pub


class TreeView2(wx.TreeCtrl):
	def __init__(self, parent, data):
		self.panel = wx.Panel(
			parent, pos=(0, 0),
			size=(parent.Size.width / 4, parent.Size.height),
			style=wx.BORDER_THEME | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND,
		)
		wx.TreeCtrl.__init__(
			self, self.panel,
			size=(parent.Size.width / 4, parent.Size.height),
			style=wx.TR_HIDE_ROOT | wx.TR_DEFAULT_STYLE,
		)

		# image array
		il = wx.ImageList(36, 36, True)
		docBitmap = wx.Bitmap("./icons/documents.png", wx.BITMAP_TYPE_PNG)
		il.Add(docBitmap)
		self.AssignImageList(il)
		self.fileMenu = fileMenuView(self)
		self.Bind(wx.EVT_LEFT_DOWN, self.onLeftMouseDown, self)
		self.Bind(wx.EVT_RIGHT_DOWN, self.onItemRightClick, self)
		self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown, self)
		# self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSelChanged, self)

		self.root = self.AddRoot("root")
		self.setData(data.sections)

		# 要加這行才能正常用 pub.sendMessage，不限定 self.model 測試 self.model2 也成功
		self.model = data

		pub.subscribe(self.setData, 'sections')
		pub.subscribe(self.setSelection, 'current_section')

	def onKeyDown(self, event):
		keycode = event.GetKeyCode()
		WXK_ENTER = 13
		if keycode == WXK_ENTER:
			item = self.GetFocusedItem()
			self.active_item(event, item)
		if keycode == wx.WXK_F2:
			self.fileMenu.onUpdate(event)
		if keycode == wx.WXK_F3:
			self.fileMenu.onAdd(event)
		event.Skip()

	def onLeftMouseDown(self, event):
		item, flags = self.HitTest(event.GetPosition())
		self.active_item(event, item)

	def active_item(self, event, item):
		self.fileMenu.RemoveAll()
		if item.ID is not None:
			self.fileMenu.InitOverItemMenu()
			pyData = self.GetItemData(item)
			self.SelectItem(item)
			# self.model.set_index_path({'index_path': pyData['index_path'] +[-1]})
			pub.sendMessage('set_index_path', data={'index_path': pyData['index_path'] + [-1]})

	def onItemRightClick(self, event):
		item, flags = self.HitTest(event.GetPosition())
		self.fileMenu.RemoveAll()
		if item.ID is not None:
			self.fileMenu.InitOverItemMenu()
			pyData = self.GetItemData(item)
			index = pyData[1]
			if index != wx.NOT_FOUND:
				self.SelectItem(item)
				self.active_item(event, item)
				if self.fileMenu.Window is None:
					self.PopupMenu(self.fileMenu, event.GetPosition())
		else:
			self.fileMenu.InitNoneOverItemMenu()
			if self.fileMenu.Window is None:
				self.PopupMenu(self.fileMenu, event.GetPosition())
		event.Skip()

	def GetItemByIndexPath(self, index_path, root):
		if self.GetItemData(root)['index_path'] == index_path:
			return root

		item, cookie = self.GetFirstChild(root)
		while item.IsOk():
			if self.GetItemData(item)['index_path'] == index_path:
				return item
			if self.ItemHasChildren(item):
				temp = self.GetItemByIndexPath(index_path, item)
				if temp:
					return temp
			item, cookie = self.GetNextChild(root, cookie)
		return None

	def setSelection(self, data):
		print(data['index_path'])
		item = self.GetRootItem()
		while item.IsOk():
			selection = self.GetItemByIndexPath(data['index_path'], item)
			if selection:
				self.SelectItem(selection)
				self.EnsureVisible(selection)
				print(self.GetItemData(selection)['label'])
				break
			item = self.GetNextSibling(item)

	def setData(self, data):
		self.DeleteAllItems()
		self.expandChild(self.root, data)
		# self.ExpandAll()

	def expandChild(self, parent, data):
		if data is None or len(data) == 0:
			return False
		else:
			for index, item in enumerate(data):
				if 'items' in item:
					childID = self.AppendItem(parent, item['label'], 0)
					self.SetItemData(childID, {
						'label': item['label'],
						'index_path': item['index_path'],
						'items': item['items'],
					})
					self.expandChild(childID, item['items'])
					# self.Expand(childID)
