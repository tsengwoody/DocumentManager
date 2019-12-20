import wx


class Hotkey(object):
	WXK_ENTER = 13
	def __init__(self):
		self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
		self.Bind(wx.EVT_KEY_UP, self.onKeyUp)			
		self.key_down = set([])
		self.key_map_action = []

	def onKeyDown(self, event):
		keycode = event.GetKeyCode()
		# print(keycode)
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
		event.Skip()
