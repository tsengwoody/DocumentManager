from copy import deepcopy
import wx
from pubsub import pub
from View.dialog import NewItemDialog


class fileMenuView(wx.Menu):
	def __init__(self, parent):
		wx.Menu.__init__(self)
		self.parent = parent
		self.index_path = None

		self.menus = {}
		for item in self.menuData:
			self.menus[item['id']] = self.Append(wx.ID_ANY, item['label'])
			self.Bind(wx.EVT_MENU, getattr(self, item['action']), self.menus[item['id']])

		self.parent.Bind(wx.EVT_RIGHT_DOWN, self.onRightClick)

		pub.subscribe(self.setCurrentSection, 'current_section')

	@property
	def menuData(self):
		return [
			{
				'id': 'enter',
				'label': _('Enter'),
				'action': 'onEnter',
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
				'action': 'onCut',
				'show': ['text', 'section', 'mathml', ],
			},
			{
				'id': 'copy',
				'label': _('Copy'),
				'action': 'onCopy',
				'show': ['text', 'section', 'mathml', ],
			},
			{
				'id': 'paste',
				'label': _('Paste'),
				'action': 'onPaste',
				'show': ['unselected', ],
			},
			{
				'id': 'moveup',
				'label': _('Move Up'),
				'action': 'onMoveUp',
				'show': ['text', 'section', 'mathml', ],
			},
			{
				'id': 'movedown',
				'label': _('Move Down'),
				'action': 'onMoveDown',
				'show': ['text', 'section', 'mathml', ],
			},
			{
				'id': 'export',
				'label': _('Export'),
				'action': 'onExport',
				'show': ['section', ],
			},
		]

	def onNoAction(self, event):
		pass

	def onRightClick(self, event):
		pos = event.GetPosition()
		index, flags = self.parent.HitTest(pos)
		if index == wx.NOT_FOUND:
			index = self.parent.GetFirstSelected()

		if index != wx.NOT_FOUND:
			if hasattr(self.parent, 'Select'):
				self.parent.Select(index)
				rect = self.parent.GetItemRect(index)
				pos = wx.Point(rect.Left+rect.Width/2, rect.Top+rect.Height/2)

		self.setMenuItem()
		if self.Window is None:
			self.parent.PopupMenu(self, pos)

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

	@property
	def data(self):
		if hasattr(self.parent, 'getList'):
			lst = self.parent.getList()
			# item = lst.GetFocusedItem()
			item = lst.GetFirstSelected()
			if item < 0:
				data = None
			else:
				data = lst.GetPyData(item)
		else:
			lst = self.parent
			# item = lst.GetFocusedItem()
			item = lst.GetSelection()
			if item.ID is None:
				data = None
			else:
				data = lst.GetItemData(item)

		return data

	def onEnter(self, event):
		data = self.data
		if not data:
			parent = self.parent
			caption = _("無法進入")
			message = _("無選定項目，無法進入")
			dlg = wx.MessageDialog(parent, message, caption, wx.OK)
			dlg.ShowModal()
			return False
		if not data['type'] == 'section':
			parent = self.parent
			caption = _("無法進入")
			message = _("選定項目非資料夾，無法進入")
			dlg = wx.MessageDialog(parent, message, caption, wx.OK)
			dlg.ShowModal()
			return False
		print(data['index_path'])
		pub.sendMessage('set_index_path', data={
			'index_path': data['index_path'] + [-1],
		})

	def onBack(self, event):
		data = self.data
		if len(data['index_path'][:-1]) <= 1:
			parent = self.parent
			caption = _("無法返回")
			message = _("已在最頂層資料夾，無法返回上一層")
			dlg = wx.MessageDialog(parent, message, caption, wx.OK)
			dlg.ShowModal()
			return False
		pub.sendMessage('set_index_path', data={
			'index_path': data['index_path'][:-2] + [-1]
		})

	def onExport(self, event):
		from json import dump
		parent = self.parent
		with wx.FileDialog(
			parent, "Save export file", wildcard="export files (*.json)|*.json",
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
		) as fileDialog:

			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return False #  the user changed their mind

			# save the current contents in the file
			pathname = fileDialog.GetPath()
			try:
				dump(self.data, open(pathname, 'w', encoding="utf-8"))
			except IOError:
				wx.LogError("Cannot save current data in file '%s'." % pathname)

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
			self.parent, _('Enter update label'),
			value=data['label'], style=wx.OK | wx.CANCEL,
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

	def onMoveUp(self, event):
		data = self.data
		if not data:
			parent = self.parent
			caption = "無法移動"
			message = "無選定項目，無法進行移動"
			dlg = wx.MessageDialog(parent, message, caption, wx.OK)
			dlg.ShowModal()
			return False
		if data['index_path'][-1] == 0:
			parent = self.parent
			caption = "無法移動"
			message = "選定項目已在最前面，無法進行移動"
			dlg = wx.MessageDialog(parent, message, caption, wx.OK)
			dlg.ShowModal()
			return False
		old_index_path = data['index_path']
		new_index_path = data['index_path'][:-1] + [data['index_path'][-1] - 1]
		pub.sendMessage("move", data={
			'old_index_path': old_index_path,
			'new_index_path': new_index_path,
		})

	def onMoveDown(self, event):
		data = self.data
		if not data:
			parent = self.parent
			caption = "無法移動"
			message = "無選定項目，無法進行移動"
			dlg = wx.MessageDialog(parent, message, caption, wx.OK)
			dlg.ShowModal()
			return False
		old_index_path = data['index_path']
		new_index_path = data['index_path'][:-1] + [data['index_path'][-1] + 1]
		pub.sendMessage("move", data={
			'old_index_path': old_index_path,
			'new_index_path': new_index_path,
		})

	def onCut(self, event):
		data = self.data
		if not data:
			parent = self.parent
			caption = _("無法剪下")
			message = _("無選定項目，無法進行剪下")
			dlg = wx.MessageDialog(parent, message, caption, wx.OK)
			dlg.ShowModal()
			return False

		self.parent.clipboard = deepcopy(data)
		pub.sendMessage("remove", data={
			'index_path': data['index_path'],
		})

	def onCopy(self, event):
		data = self.data
		if not data:
			parent = self.parent
			caption = _("無法複製")
			message = _("無選定項目，無法進行複製")
			dlg = wx.MessageDialog(parent, message, caption, wx.OK)
			dlg.ShowModal()
			return False

		self.parent.clipboard = deepcopy(self.data)

	def onPaste(self, event):
		data = self.parent.clipboard
		if not data:
			parent = self.parent
			caption = _("無法貼上")
			message = _("剪貼簿無資料，無法進行貼上")
			dlg = wx.MessageDialog(parent, message, caption, wx.OK)
			dlg.ShowModal()
			return False

		if not self.data:
			index_path = self.index_path + [-1]
		else:
			index_path = self.data['index_path']

		pub.sendMessage("add", data={
			'index_path': index_path,
			'data': data,
		})


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
		self.backPathbtn.SetLabel(_("Back"))

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
