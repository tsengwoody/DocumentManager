import wx
from View.toolbar_view import fileMenuView
from pubsub import pub
from enums import InputType

class TreeView2(wx.TreeCtrl):
	id = 1
	def __init__(self, parent, data):
		self.panel = wx.Panel(parent, wx.ID_ANY, (0, 0), size=(parent.Size.width/4, parent.Size.height), style = wx.BORDER_THEME | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
		wx.TreeCtrl.__init__(self, self.panel, self.id, wx.DefaultPosition, (parent.Size.width/4, parent.Size.height), wx.TR_HIDE_ROOT|wx.TR_DEFAULT_STYLE)

		# image array
		il = wx.ImageList(36, 36, True)
		docBitmap = wx.Bitmap("./icons/documents.png", wx.BITMAP_TYPE_PNG)
		il.Add(docBitmap)
		self.AssignImageList(il)
		self.fileMenu = fileMenuView(self)
		self.Bind(wx.EVT_LEFT_DOWN, self.onLeftMouseDown, self)
		self.Bind(wx.EVT_RIGHT_DOWN, self.onItemRightClick, self)
		self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown, self)
		#self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSelChanged, self)

		self.root = self.AddRoot("root") 
		self.setData(data.sections)
		self.model = data

	def onKeyDown(self, event):
		keycode = event.GetKeyCode()
		WXK_ENTER = 13
		if keycode == WXK_ENTER:
			item = self.GetFocusedItem()
			self.active_item(event, item)
		if keycode == wx.WXK_F2:
			self.fileMenu.onUpdate(event)
		event.Skip()

	def onLeftMouseDown(self, event):
		item, flags = self.HitTest(event.GetPosition())
		self.active_item(event, item)

	def onSelChanged(self, event):
		item = event.GetItem()
		self.active_item(event, item)

	def active_item(self, event, item):
		self.fileMenu.RemoveAll()
		if item.ID is not None:
			self.fileMenu.InitOverItemMenu()
			pyData = self.GetItemData(item)
			self.SelectItem(item)	   
			self.model.set_index_path({'index_path': pyData['index_path'] +[-1]})
			#pub.sendMessage('set_index_path', data={'index_path': pyData['index_path'] +[-1]})

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

	def setData(self, data):
		self.DeleteAllItems()
		self.expandChild(self.root, data)
		#self.ExpandAll()

	def expandChild(self, parent, data):
		if data is None or len(data) == 0:
			return False
		else:
			for index, item in enumerate(data):
				#if 'items' in item:
					label = item['label']
					index_path = item['index_path']
					childID = self.AppendItem(parent, label, 0)
					self.SetPyData(childID, item)
					self.expandChild(childID, item['items'])
					#self.Expand(childID)


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
		self.fileMenu = fileMenuView(self)
		self.Bind(wx.EVT_LEFT_DOWN, self.onLeftMouseDown, self)
		self.Bind(wx.EVT_RIGHT_DOWN, self.onItemRightClick, self)
		self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown, self)
		#self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSelChanged, self)

		self.root = self.AddRoot("root") 
		pub.subscribe(self.setData, "data_changedTree")
		self.setData(data)

	def onKeyDown(self, event):
		keycode = event.GetKeyCode()
		WXK_ENTER = 13
		if keycode == WXK_ENTER:
			item = self.GetFocusedItem()
			self.active_item(event, item)
		if keycode == wx.WXK_F2:
			self.fileMenu.onUpdate(event)
		event.Skip()

	def onLeftMouseDown(self, event):
		item, flags = self.HitTest(event.GetPosition())
		self.active_item(event, item)

	def onSelChanged(self, event):
		item = event.GetItem()
		self.active_item(event, item)
	
	def active_item(self, event, item):
		self.fileMenu.RemoveAll()
		if item.ID is not None:
			self.fileMenu.InitOverItemMenu()
			pyData = self.GetItemData(item)
			level = pyData[1]
			index_array = pyData[2]
			if index_array is not None and index_array[0] != wx.NOT_FOUND: 
				self.SelectItem(item)	   
				label = self.GetItemText(item)
				pub.sendMessage("data_changing", data={'type': InputType.PANEL.value, 'index': index_array, 'label': label, 'layer': level})

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

	def setData(self, data):
		items = data['items']
		self.DeleteAllItems()
		self.expandChild(self.root, 0, [], items)
		self.ExpandAll()

	def expandChild(self, parent, level, index_array, data=[]):
		if data is None or len(data) == 0:
			return False
		else:
			for index, item in enumerate(data):
				if 'items' in item:
					_index_array = index_array.copy()
					label = item['label']
					childID = self.AppendItem(parent, label, 0)
					_index_array.insert(level, index)
					self.SetPyData(childID, (label, level, _index_array))
					self.expandChild(childID, level+1, _index_array.copy(), item['items'])
					self.Expand(childID)