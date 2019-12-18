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
		self.shift_down = False
		self.ctrl_down = False

	def onRightClick(self, event):
		index, flags = self.lst.HitTest(event.GetPosition())
		if index == wx.NOT_FOUND:
			index = self.lst.GetFirstSelected()

		if index != wx.NOT_FOUND:
			pos = event.GetPosition()
			if hasattr(self.lst, 'Select'):
				self.lst.Select(index)
				rect = self.lst.GetItemRect(index)
				pos = wx.Point(rect.Left+rect.Width/2, rect.Top+rect.Height/2)
			self.fileMenu.setMenuItem()
			if self.fileMenu.Window is None:
				self.PopupMenu(self.fileMenu, pos)
		else:
			self.fileMenu.setMenuItem()
			if self.fileMenu.Window is None:
				self.PopupMenu(self.fileMenu, event.GetPosition())

	def onKeyDown(self, event):
		keycode = event.GetKeyCode()
		if keycode == wx.WXK_DELETE:   
			self.fileMenu.onRemove(event)
		if keycode == wx.WXK_F2:
			self.fileMenu.onUpdate(event)
		if keycode == wx.WXK_F3:
			self.fileMenu.onAdd(event)			
		if keycode == wx.WXK_SHIFT:
			self.shift_down = True
		if keycode == wx.WXK_CONTROL:
			self.ctrl_down = True
		event.Skip()

	def onKeyUp(self, event):
		keycode = event.GetKeyCode()	
		if keycode == wx.WXK_SHIFT:
			self.shift_down = False
		if keycode == wx.WXK_CONTROL:
			self.ctrl_down = False
		if self.shift_down and self.ctrl_down and keycode == self.WXK_N:
			self.fileMenu.onAdd(event)
		event.Skip()
