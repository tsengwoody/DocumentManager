import wx
from View.toolbar_view import fileMenuView


class Hotkey(object):
	WXK_N = 78
	WXK_ENTER = 13
	def __init__(self, lst):
		self.fileMenu = fileMenuView(self)
		self.lst = lst
		self.lst.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
		self.lst.Bind(wx.EVT_KEY_UP, self.onKeyUp)			
		self.lst.Bind(wx.EVT_RIGHT_DOWN, self.onRightClick)

		self.key_down = set([])
		self.key_map_action = [
			{
				'key': [wx.WXK_F2],
				'action': self.fileMenu.onUpdate,
			},
			{
				'key': [wx.WXK_SHIFT, wx.WXK_CONTROL, self.WXK_N],
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
		]

	def onRightClick(self, event):
		pos = event.GetPosition()
		index, flags = self.lst.HitTest(pos)
		if index == wx.NOT_FOUND:
			index = self.lst.GetFirstSelected()

		if index != wx.NOT_FOUND:
			if hasattr(self.lst, 'Select'):
				self.lst.Select(index)
				rect = self.lst.GetItemRect(index)
				pos = wx.Point(rect.Left+rect.Width/2, rect.Top+rect.Height/2)

		self.fileMenu.setMenuItem()
		if self.fileMenu.Window is None:
			self.PopupMenu(self.fileMenu, pos)

	def onKeyDown(self, event):
		keycode = event.GetKeyCode()
		self.key_down.add(keycode)
		for item in self.key_map_action:
			if self.key_down == set(item['key']):
				self.key_down.clear()
				item['action'](event)
				break
		event.Skip()

	def onKeyUp(self, event):
		keycode = event.GetKeyCode()	
		try:
			self.key_down.remove(keycode)
		except KeyError:
			self.key_down.clear()
		print(self.key_down)
		event.Skip()
