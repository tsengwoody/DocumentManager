import wx
from pubsub import pub

from View.toolbar_view import fileMenuView
from View.component_view import SectionPanel, TextPanel, MathmlPanel
from enums import ImageIdEnum, InputType, PanelType
from enums import ImageIdEnum, InputType, PanelType, ActionType

class RightTopPanel(wx.Panel):
	def __init__(self, parent, data, pos=(200, 000), size=wx.Size(600, 200), event_name='data_changed'):
		self.fileMenu = fileMenuView(self)
		wx.Panel.__init__(self, parent, wx.ID_ANY, pos, size, style = wx.BORDER_THEME | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
		self.parent = parent
		self.data = data
		self.is_set_eventbind = 'clickable' not in data or data['clickable']==True
		self.insideItems = wx.BoxSizer(wx.HORIZONTAL)
		self.SetBackgroundColour( wx.Colour( 112, 186, 248 ) )
		pub.subscribe(self.setData, event_name)
		self.setData(self.data)

	def setData(self, data):
		print("data msg in panel view:", data)
		try:
			self.panelItem.Destroy()
		except AttributeError:
			print("there is no created panelItem")
		content = data['data']['items']
		self.panelItem = self.updatePanel(title='', content=content, _type='section', data=data)
		self.insideItems.Add(self.panelItem, 1, wx.EXPAND|wx.ALL)
		self.panelItem.SetSize(self.Size)
		if 'clickable' not in data or data['clickable']==True:
			if hasattr(self.panelItem, "getList"):
				lst = self.panelItem.getList()
				lst.SetItemState(0, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
				self.SetFocus()
	
	def updatePanel(self, title, content, _type, data):
		return SectionPanel(parent=self, title=title, content=content, _type=_type, data=data, eventParent=self)

class RightBottomPanel(wx.Panel):
	def __init__(self, parent, data, pos=(200, 000), size=wx.Size(600, 200), event_name='data_changed'):
		self.fileMenu = fileMenuView(self)
		wx.Panel.__init__(self, parent, wx.ID_ANY, pos, size, style = wx.BORDER_THEME | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
		self.parent = parent
		self.data = data
		self.is_set_eventbind = 'clickable' not in data or data['clickable']==True
		self.insideItems = wx.BoxSizer(wx.HORIZONTAL)
		self.SetBackgroundColour( wx.Colour( 112, 186, 248 ) )
		pub.subscribe(self.setData, event_name)
		self.setData(self.data)

	def setData(self, data):
		print("data msg in panel view:", data)
		try:
			self.panelItem.Destroy()
		except AttributeError:
			print("there is no created panelItem")

		count = {}
		for item in data['data']['items']:
			if item['type'] in count:
				count[item['type']] = count[item['type']] +1
			else:
				count[item['type']] = 1

		content = []
		for key, value in count.items():
			content.append({
				'label': value,
				'type': key,
			})
		print(content)
		self.panelItem = self.updatePanel(title='', content=content, _type='section', data=data)
		self.insideItems.Add(self.panelItem, 1, wx.EXPAND|wx.ALL)
		self.panelItem.SetSize(self.Size)
		if 'clickable' not in data or data['clickable']==True:
			if hasattr(self.panelItem, "getList"):
				lst = self.panelItem.getList()
				lst.SetItemState(0, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
				self.SetFocus()
	
	def updatePanel(self, title, content, _type, data):
		if _type == PanelType.SECTION.value:
			return SectionPanel(parent=self, title=title, content=content, _type=_type, data=data, eventParent=self)
		elif _type == PanelType.TEXT.value:
			return TextPanel(parent=self, title=title, content=content, _type=_type, data=data, eventParent=self)
		elif _type == PanelType.MATH.value:
			return MathmlPanel(parent=self, title=title, content=content, _type=_type, data=data, eventParent=self)
