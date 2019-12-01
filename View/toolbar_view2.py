﻿import wx
from pubsub import pub
from enums import ImageIdEnum, InputType, ActionType
from Component.dialog import NewItemDialog
from View.component_view import SectionPanel, TextPanel, MathmlPanel


class fileMenuView2(wx.Menu):
	def __init__(self, parent):
		wx.Menu.__init__(self)
		self.parent = parent

		self.menu_add=self.Append(wx.ID_ANY,  "Add Item")
		self.Enable(self.menu_add.GetId(), False)
		self.Bind(wx.EVT_MENU, self.onAdd, self.menu_add)

		self.menu_update=self.Append(wx.ID_ANY,  "Update")
		self.Bind(wx.EVT_MENU, self.onUpdate, self.menu_update)
		
		self.menu_delete=self.Append(wx.ID_ANY,  "Delete")
		self.Bind(wx.EVT_MENU, self.OnDelete, self.menu_delete)

		self.menu_import=self.Append(wx.ID_ANY,  "Import")
		self.Enable(self.menu_import.GetId(), False)

		self.menu_export=self.Append(wx.ID_ANY,  "Export")
		self.Bind(wx.EVT_MENU, self.OnExport, self.menu_export)

	def InitOverItemMenu(self):
		self.Enable(self.menu_update.GetId(), True)
		self.Enable(self.menu_delete.GetId(), True)
		self.Enable(self.menu_export.GetId(), True)
		self.Enable(self.menu_add.GetId(), False)
		self.Enable(self.menu_import.GetId(), False)

	def InitNoneOverItemMenu(self):
		self.Enable(self.menu_update.GetId(), False)
		self.Enable(self.menu_delete.GetId(), False)
		self.Enable(self.menu_export.GetId(), False)
		self.Enable(self.menu_add.GetId(), True)
		self.Enable(self.menu_import.GetId(), True)
		
	def RemoveAll(self):
		return True

	def OnDelete(self, event):
		parent = self.parent	
		caption = "即將刪除"
		message = "確認是否刪除?"
		dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.CANCEL | wx.ICON_QUESTION)
		if dlg.ShowModal() == wx.ID_OK:
			lst = None
			if hasattr(parent, 'panelItem') and isinstance(parent.panelItem, wx.Panel):
				lst = parent.panelItem.getList()
			item = -1
			if lst is not None:
				if hasattr(lst, "GetFocusedItem"):
					item = lst.GetFocusedItem()
				if item != -1:
					pub.sendMessage("data_changing", data={'action': ActionType.DEL.value})
					lst.DeleteItem(item)
					lst.Select(0)
					return True
			elif isinstance(parent, wx.TreeCtrl):
				item = parent.GetFocusedItem()
				pyData = parent.GetItemData(item)
				if item != -1 and pyData is not None:
					pub.sendMessage("data_changing", data={'action': ActionType.DEL.value, 'layer': pyData[1], 'index': pyData[2][pyData[1]], 'items':[]})
					return True
			return False

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

	# FolderPanel
	# FolderPanel Update 按鈕觸發事件
	def onUpdate(self, event):
		if hasattr(self.parent, 'panelItem'):
			lst = self.parent.panelItem.getList()
			item = lst.GetFocusedItem()
			if item < 0:
				event.Skip()
				return
		else:
			lst = self.parent
			item = lst.GetFocusedItem()
			if item.ID is None:
				event.Skip()
				return

		data = lst.GetItemData(item)
		dlg = wx.TextEntryDialog(self.parent, 'Enter your update folder', value=data['label'], style=wx.TE_MULTILINE|wx.OK|wx.CANCEL)

		if dlg.ShowModal() == wx.ID_OK:
			data['label'] = dlg.GetValue()
			lst.SetItemText(item, data['label'])
			pub.sendMessage("update", data={
				'index_path': data['index_path'],
				'data': {'label': data['label']},
			})

		dlg.Destroy()

	# FolderPanel Add 按鈕觸發事件
	def onAdd(self, event):
		index_path = []
		# 點在又上時
		if hasattr(self.parent, 'panelItem'):
			lst = self.parent.panelItem.getList()
			item = lst.GetFocusedItem()
			if item < 0:
				index_path = [-1]
			else:
				index_path = lst.GetItemData(item)['index_path']
				index_path = index_path[:-1] + [index_path[-1] + 1]
		# 點在左側時
		else:
			lst = self.parent
			item = lst.GetFocusedItem()
			if item.ID is None:
				index_path = [-1]
			else:
				index_path = lst.GetItemData(item)['index_path']
				index_path = index_path[:-1] + [index_path[-1] + 1]

		dlg = NewItemDialog(self.parent)
		ret = dlg.ShowModal()

		if ret == wx.ID_OK:
			label = dlg.newItemName
			_type = dlg.newItemType

			pub.sendMessage("add", data={
				'index_path': index_path,
				'data': {'label': label},
			})

		dlg.Destroy()


class ToolBarView2(wx.Panel):
	def __init__(self, parent, data):
		wx.Panel.__init__(self, parent, wx.ID_ANY, pos=(parent.Size.width/4, 0), size=(parent.Size.width*3/4, 69), style = wx.TAB_TRAVERSAL|wx.EXPAND)
		self.parent = parent
		self.path = data
		backPathBitmap = wx.Bitmap("./icons/backPath.png", wx.BITMAP_TYPE_PNG)
		self.backPathbtn = wx.Button(self, -1, style=wx.BU_BOTTOM | wx.BU_NOTEXT)
		self.backPathbtn.SetBitmap(backPathBitmap, wx.BOTTOM)
		self.backPathbtn.SetLabel("上一層")
		self.toolbar = wx.BoxSizer(wx.VERTICAL)
		self.toolbar.Add(self.backPathbtn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)				   
		self.pathText = wx.StaticText(self, -1, self.path, size=(-1, -1), style=wx.ALIGN_CENTRE_HORIZONTAL | wx.BU_NOTEXT)
		self.toolbar.Add(self.pathText, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.SetSizer(self.toolbar)
		self.Fit()
		self.backPathbtn.Bind(wx.EVT_BUTTON, self.backPath)

	def setData(self, data):
		try:
			if 'index_array' in data:
				self.index_array = data['index_array'].copy()
			else:
				layer = data['layer']
				self.index_array.insert(layer,data['index'])
				del self.index_array[layer+1:] 
			self.data = data
			self.pathText.SetLabel(data['label'])
		except AttributeError:
			print("there is no created pathText")

	def backPath(self, event):
		print("back to previous path")
		if len(self.index_array) >= 1:
			self.index_array.pop()
			pub.sendMessage("data_changing", data={'type': InputType.PANEL.value, 'layer': self.data['layer']-1,'index': self.index_array})