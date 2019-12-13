import wx
from pubsub import pub
from Component.dialog import NewItemDialog


class fileMenuView2(wx.Menu):
	def __init__(self, parent):
		wx.Menu.__init__(self)
		self.parent = parent

		self.menu_add = self.Append(wx.ID_ANY, "Add Item")
		self.Bind(wx.EVT_MENU, self.onAdd, self.menu_add)

		self.menu_update = self.Append(wx.ID_ANY, "Update")
		self.Bind(wx.EVT_MENU, self.onUpdate, self.menu_update)

		self.menu_delete = self.Append(wx.ID_ANY, "Delete")
		self.Bind(wx.EVT_MENU, self.onRemove, self.menu_delete)

		self.index_path = None
		self.data = None

		pub.subscribe(self.setData, 'pointer_raw_data')
		pub.subscribe(self.setCurrentSection, 'current_section')

	def setData(self, data):
		self.data = data['data'] if data else None
		if self.data:
			self.InitOverItemMenu()
		else:
			self.InitNoneOverItemMenu()

	def setCurrentSection(self, data):
		self.index_path = data['index_path']

	def InitOverItemMenu(self):
		self.Enable(self.menu_add.GetId(), True)
		self.Enable(self.menu_update.GetId(), True)
		self.Enable(self.menu_delete.GetId(), True)

	def InitNoneOverItemMenu(self):
		self.Enable(self.menu_add.GetId(), True)
		self.Enable(self.menu_update.GetId(), False)
		self.Enable(self.menu_delete.GetId(), False)

	def OnExport(self, event):
		parent = self.parent
		with wx.FileDialog(parent, "Save export file", wildcard="export files (*.json)|*.json",
					   style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return	 # the user changed their mind

			# save the current contents in the file
			pathname = fileDialog.GetPath()
			try:
				with open(pathname, 'w', encoding="utf-8") as file:
					file.write(parent.content)
			except IOError:
				wx.LogError("Cannot save current data in file '%s'." % pathname)

	'''@property
	def data(self):
		if hasattr(self.parent, 'getList'):
			lst = self.parent.getList()
			item = lst.GetFocusedItem()
			if item < 0:
				data = None
			else:
				data = lst.GetPyData(item)
		else:
			lst = self.parent
			item = lst.GetFocusedItem()
			if item.ID is None:
				data = None
			else:
				data = lst.GetItemData(item)

		return data'''


	def onAdd(self, event):
		if not self.data:
			index_path = self.index_path + [-1]
		else:
			index_path = self.data['index_path']

		dlg = NewItemDialog(self.parent)
		if dlg.ShowModal() == wx.ID_OK:
			data = {
				'label' :dlg.newItemName,
				'type' :dlg.newItemType,
			}
			if dlg.newItemType == 'section':
				data.update({'items': []})
			else:
				data.update({'content': ''})

			pub.sendMessage("add", data={
				'index_path': index_path,
				'data': data,
			})

		dlg.Destroy()

	def onUpdate(self, event):
		data = self.data
		if not data:
			parent = self.parent
			caption = "無法更新"
			message = "無選定項目，無法進行更新"
			dlg = wx.MessageDialog(parent, message, caption, wx.OK)
			dlg.ShowModal()
			return False

		dlg = wx.TextEntryDialog(self.parent, 'Enter your update folder', value=data['label'], style=wx.TE_MULTILINE|wx.OK|wx.CANCEL)
		if dlg.ShowModal() == wx.ID_OK:
			data['label'] = dlg.GetValue()
			pub.sendMessage("update", data={
				'index_path': data['index_path'],
				'data': {'label': data['label']},
			})

		dlg.Destroy()

	def onRemove(self, event):
		data = self.data
		if not data:
			parent = self.parent
			caption = "無法刪除"
			message = "無選定項目，無法進行刪除"
			dlg = wx.MessageDialog(parent, message, caption, wx.OK)
			dlg.ShowModal()
			return False

		parent = self.parent
		caption = "即將刪除"
		message = "確認是否刪除?"
		dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.CANCEL | wx.ICON_QUESTION)
		if dlg.ShowModal() == wx.ID_OK:
			pub.sendMessage("remove", data={
				'index_path': data['index_path'],
			})

		dlg.Destroy()

class ToolBarView2(wx.Panel):
	def __init__(self, parent, data):
		wx.Panel.__init__(
			self, parent, wx.ID_ANY,
			pos=(parent.Size.width / 4, 0), size=(parent.Size.width * 3 / 4, 69),
			style=wx.TAB_TRAVERSAL | wx.EXPAND
		)
		self.parent = parent

		backPathBitmap = wx.Bitmap("./icons/backPath.png", wx.BITMAP_TYPE_PNG)
		self.backPathbtn = wx.Button(self, -1, style=wx.BU_BOTTOM | wx.BU_NOTEXT)
		self.backPathbtn.SetBitmap(backPathBitmap, wx.BOTTOM)
		self.backPathbtn.SetLabel("上一層")

		self.toolbar = wx.BoxSizer(wx.VERTICAL)
		self.toolbar.Add(self.backPathbtn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)

		self.pathText = wx.StaticText(self, -1, data['path'], size=(-1, -1), style=wx.ALIGN_CENTRE_HORIZONTAL | wx.BU_NOTEXT)
		self.toolbar.Add(self.pathText, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

		self.SetSizer(self.toolbar)
		self.Fit()

		self.backPathbtn.Bind(wx.EVT_BUTTON, self.backPath)

		self.path = data['path']
		self.current_section = data['current_section']

		pub.subscribe(self.setPath, 'path')
		pub.subscribe(self.setData, 'current_section')

	def setPath(self, data):
		self.path = data
		self.pathText.SetLabel(data)

	def setData(self, data):
		self.current_section = data

	def backPath(self, event):
		if len(self.current_section['index_path']) > 1:
			pub.sendMessage('set_index_path', data={'index_path': self.current_section['index_path'][:-1] + [-1]})
