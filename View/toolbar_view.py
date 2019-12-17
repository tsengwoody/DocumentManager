import wx
from pubsub import pub
from Component.dialog import NewItemDialog


class fileMenuView(wx.Menu):
	def __init__(self, parent):
		wx.Menu.__init__(self)
		self.parent = parent

		self.menus = {}
		for item in self.menuData:
			self.menus[item['id']] = self.Append(wx.ID_ANY, item['label'])
			self.Bind(wx.EVT_MENU, getattr(self, item['action']), self.menus[item['id']])

		self.index_path = None
		# self.data = None

		# pub.subscribe(self.setData, 'pointer_raw_data')
		pub.subscribe(self.setCurrentSection, 'current_section')

	@property
	def menuData(self):
		return [
			{
				'id': 'enter',
				'label': _('Enter'),
				'action': 'onNoAction',
				'show': ['section', ],
			},
			{
				'id': 'edittext',
				'label': _('Edit Text'),
				'action': 'onNoAction',
				'show': ['text', ],
			},
			{
				'id': 'editmathml',
				'label': _('Edit MathML'),
				'action': 'onNoAction',
				'show': ['mathml', ],
			},
			{
				'id': 'add',
				'label': _('Add'),
				'action': 'onAdd',
				'show': ['unselected', ],
			},
			{
				'id': 'update',
				'label': _('Update'),
				'action': 'onUpdate',
				'show': ['text', 'section', 'mathml', ],
			},
			{
				'id': 'remove',
				'label': _('Delete'),
				'action': 'onRemove',
				'show': ['text', 'section', 'mathml', ],
			},
			{
				'id': 'cut',
				'label': _('Cut'),
				'action': 'onNoAction',
				'show': ['text', 'section', 'mathml', ],
			},
			{
				'id': 'copy',
				'label': _('Copy'),
				'action': 'onNoAction',
				'show': ['text', 'section', 'mathml', ],
			},
			{
				'id': 'paste',
				'label': _('Paste'),
				'action': 'onNoAction',
				'show': ['unselected', ],
			},
			{
				'id': 'moveup',
				'label': _('Move Up'),
				'action': 'onNoAction',
				'show': ['text', 'section', 'mathml', ],
			},
			{
				'id': 'movedown',
				'label': _('Move Down'),
				'action': 'onNoAction',
				'show': ['text', 'section', 'mathml', ],
			},
		]

	def onNoAction(self, event):
		pass

	def setData(self, data):
		self.data = data['data'] if data else None
		self.setMenuItem()

	def setCurrentSection(self, data):
		self.index_path = data['index_path']

	def setMenuItem(self):
		for item in self.menus.values():
			try:
				self.Remove(item)
			except:
				pass

		# 根據指向的物件決定顯示項目
		for item in self.menuData:
			if not self.data and 'unselected' in item['show']:
				self.Insert(self.GetMenuItemCount(), self.menus[item['id']])
			elif self.data and self.data['type'] in item['show']:
				self.Insert(self.GetMenuItemCount(), self.menus[item['id']])

	'''def onExport(self, event):
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
				wx.LogError("Cannot save current data in file '%s'." % pathname)'''

	@property
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

		return data

	def onAdd(self, event):
		if not self.data:
			index_path = self.index_path + [-1]
		else:
			index_path = self.data['index_path']

		dlg = NewItemDialog(self.parent)
		if dlg.ShowModal() == wx.ID_OK:
			data = {
				'label': dlg.newItemName,
				'type': dlg.newItemType,
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

		dlg = wx.TextEntryDialog(
			self.parent, 'Enter your update folder',
			value=data['label'], style=wx.TE_MULTILINE | wx.OK | wx.CANCEL,
		)
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


class ToolBarView(wx.Panel):
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
		self.toolbar.Add(self.backPathbtn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)

		self.pathText = wx.StaticText(
			self, -1, data['path'],
			size=(-1, -1), style=wx.ALIGN_CENTRE_HORIZONTAL | wx.BU_NOTEXT,
		)
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
