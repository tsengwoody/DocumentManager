import wx


class FrameView(wx.Frame):
	def __init__(self, parent, title, size=wx.Size(800, 400)):
		wx.Frame.__init__(self, None, title=title)
		self.Centre()
		self.SetMinSize(size)
		self.SetSize(size)
		self.SetMenuBar(self.createMenuBar())

	def show(self, isShow=True):
		self.Show(isShow)

	@property
	def menusData(self):
		return [
			{
				'label': _('&File'),
				'type': 'menu',
				'items': [
					{
						'id': 'open',
						'label': _('&Open'),
						'type': 'menuitem',
						'action': 'onNoAction',
						'show': ['section'],
					},
					{
						'id': 'close',
						'label': _('&Close'),
						'type': 'menuitem',
						'action': 'onNoAction',
						'show': ['section'],
					},
				],
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
				menu.Append(wx.ID_ANY, item['label'])
				# menu.Bind(wx.EVT_MENU, getattr(self, item['action']), self.menus[item['id']])

		'''for eachItem in menuData:
			if len(eachItem) == 2:
				label = eachItem[0]
				subMenu = self.createMenu(eachItem[1])
				menu.AppendMenu(wx.NewId(), label, subMenu)

			else:
				self.createMenuItem(menu, *eachItem)'''

		return menu

	def createMenuItem(self, menu, label, status, handler, kind=wx.ITEM_NORMAL):
		if not label:
			menu.AppendSeparator()
			return
		menuItem = menu.Append(-1, label, status, kind)
		self.Bind(wx.EVT_MENU, handler, menuItem)

	def setMenuBar(self, fileMenu):
		self.fileMenu = fileMenu
		self.menubar = wx.MenuBar()
		self.menubar.Append(self.fileMenu, 'Add')
		self.SetMenuBar(self.menubar)
