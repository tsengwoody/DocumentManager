import json
import wx
from pubsub import pub


class FrameView(wx.Frame):
	def __init__(self, parent, title, size=wx.Size(800, 400)):
		wx.Frame.__init__(self, None, title=title)
		self.Centre()
		self.SetMinSize(size)
		self.SetSize(size)
		self.SetMenuBar(self.createMenuBar())

		pub.subscribe(self.setRootSection, 'root_section')

	def show(self, isShow=True):
		self.Show(isShow)

	@property
	def menusData(self):
		return [
			{
				'label': _('File'),
				'type': 'menu',
				'items': [
					{
						'id': 'new',
						'label': _('&New'),
						'type': 'menuitem',
						'action': 'onNew',
					},
					{
						'id': 'open',
						'label': _('&Open'),
						'type': 'menuitem',
						'action': 'onOpen',
					},
					{
						'id': 'save',
						'label': _('&Save'),
						'type': 'menuitem',
						'action': 'onSave',
					},
					{
						'id': 'export',
						'label': _('&Export'),
						'type': 'menuitem',
						'action': 'onExport',
					},
					{
						'id': 'exit',
						'label': _('E&xit'),
						'type': 'menuitem',
						'action': 'onExit',
					},
				],
			},
			{
				'label': _('About'),
				'type': 'menu',
				'items': [
					{
						'id': 'ContactUs',
						'label': _('Contact Us'),
						'type': 'menuitem',
						'action': 'onNoAction',
					},
				]
			},
		]

	def createMenuBar(self):
		menuBar = wx.MenuBar()
		for menuData in self.menusData:
			menuLabel = menuData['label']
			menuItems = menuData['items']
			menuBar.Append(self.createMenu(menuItems), menuLabel)

		return menuBar

	def createMenu(self, menuData):
		menu = wx.Menu()
		for item in menuData:
			if item['type'] == 'menu':
				label = item['label']
				subMenu = self.createMenu(item['items'])
				menu.AppendMenu(wx.NewId(), label, subMenu)
			else:
				menuitem = menu.Append(wx.ID_ANY, item['label'])
				menu.Bind(wx.EVT_MENU, getattr(self, item['action']), menuitem)

		return menu

	def setMenuBar(self, fileMenu):
		self.fileMenu = fileMenu
		self.menubar = wx.MenuBar()
		self.menubar.Append(self.fileMenu, 'Add')
		self.SetMenuBar(self.menubar)

	def setRootSection(self, data):
		self.root_index = data['index_path'][0]
		self.root_section = data['data']

	def onNoAction(self, event):
		pass

	def onNew(self, event):
		pub.sendMessage('append', data={
			'label': '新文件',
			'type': 'section',
			'items': [],
		})

	def onOpen(self, event):
		with wx.FileDialog(
			self, message=_("Open file..."), defaultDir='',
			wildcard="json files (*.json) | *.json",
		) as dialog:
			if dialog.ShowModal() != wx.ID_OK:
				return
			path = dialog.GetPath()
		data = json.load(open(path))
		pub.sendMessage('append', data=data)

	def onSave(self, event):
		with wx.FileDialog(
			self, message=_("Save file..."), defaultDir='', defaultFile="DocumentManagerProject.json",
			wildcard="json files (*.json) | *.json", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
		) as dialog:
			if dialog.ShowModal() != wx.ID_OK:
				return
			path = dialog.GetPath()
		json.dump(self.root_section, open(path, "w"))

	def onExport(self, event):
		with wx.FileDialog(
			self, message=_("Save file..."), defaultDir='', defaultFile="DocumentManagerProject.json",
			wildcard="json files (*.json) | *.json", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
		) as dialog:
			if dialog.ShowModal() != wx.ID_OK:
				return
			path = dialog.GetPath()

	def onExit(self, event):
		self.Close()
