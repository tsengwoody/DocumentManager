import wx
from pubsub import pub
from View.toolbar_view import fileMenuView
from View.utility import Hotkey


class TreeView(wx.TreeCtrl, Hotkey):
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

		# 管理文件區
		Hotkey.__init__(self)
		self.fileMenu = fileMenuView(self)
		self.key_map_action = [
			{
				'key': [wx.WXK_F2],
				'action': self.fileMenu.onUpdate,
			},
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
		]
		self.clipboard = None

		# image array
		il = wx.ImageList(36, 36, True)
		docBitmap = wx.Bitmap("./icons/documents.png", wx.BITMAP_TYPE_PNG)
		il.Add(docBitmap)
		self.AssignImageList(il)
		self.Bind(wx.EVT_LEFT_DOWN, self.onLeftMouseDown, self)
		# self.Bind(wx.EVT_RIGHT_DOWN, self.onItemRightClick, self)
		# self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
		# self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSelChanged, self)

		self.root = self.AddRoot("root")
		self.setData(data)

		pub.subscribe(self.setData, 'sections')
		pub.subscribe(self.setSelection, 'current_section')

	def onLeftMouseDown(self, event):
		item, flags = self.HitTest(event.GetPosition())
		self.active_item(event, item)

	def active_item(self, event, item):
		if item.ID is not None:
			pyData = self.GetItemData(item)
			self.SelectItem(item)
			pub.sendMessage('set_index_path', data={'index_path': pyData['index_path'] + [-1]})

	def onItemRightClick(self, event):
		item, flags = self.HitTest(event.GetPosition())
		if item.ID is None:
			item = self.GetSelection()
		if item.ID is not None:
			self.SelectItem(item)
		self.fileMenu.setMenuItem()
		if self.fileMenu.Window is None:
			self.PopupMenu(self.fileMenu, event.GetPosition())
		event.Skip()

	def onKeyDown(self, event):
		keycode = event.GetKeyCode()
		if keycode == Hotkey.WXK_ENTER:
			item = self.GetFocusedItem()
			self.active_item(event, item)
		super().onKeyDown(event)

	def GetItemByIndexPath(self, index_path, root):
		if self.GetItemData(root)['index_path'] == index_path:
			return root

		item, cookie = self.GetFirstChild(root)
		while item.IsOk():
			temp = self.GetItemByIndexPath(index_path, item)
			if temp:
				return temp
			item, cookie = self.GetNextChild(root, cookie)
		return None

	def setSelection(self, data):
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
						'type': 'section',
						'index_path': item['index_path'],
						'items': item['items'],
					})
					self.expandChild(childID, item['items'])
					# self.Expand(childID)
