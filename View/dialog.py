import wx


class NewItemDialog(wx.Dialog):
	def __init__(self, parent, defaultValue=""):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, _("Add Item"), size=(420, 220), pos=(500, 300))
		self.parent = parent
		self.newItemType = "section"
		self.newItemName = "New Item"
		self.objectTypes = ["section", "text", "mathml"] 

		# ===============================================================================
		# UI Control Initialize
		# ===============================================================================
		self.panel = wx.Panel(self, wx.ID_ANY)
		self.box = wx.BoxSizer(wx.VERTICAL) 

		# Select Type
		self.objectTypesLabel = wx.StaticText(self.panel, label="選擇新增的物件類型?")
		self.typeChoice = wx.Choice(self.panel, -1, choices=self.objectTypes)
		self.typeChoice.SetSelection(0)

		# Input Name
		self.nameLabel = wx.StaticText(self.panel, label="輸入物件名稱: ")
		self.nameTextCtrl = wx.TextCtrl(self.panel, size=(-1,20), value=defaultValue)

		self.OKBtn = wx.Button(self.panel, -1, label="OK")
		self.QuitBtn = wx.Button(self.panel, -1, label="Cancel")

		# ===============================================================================
		# Sizer
		# ===============================================================================
		self.btn_BSizer = wx.BoxSizer(orient = wx.HORIZONTAL)
		self.btn_BSizer.Add(self.OKBtn, 1, wx.EXPAND, border=5)
		self.btn_BSizer.Add(self.QuitBtn, 1, wx.EXPAND, border=5)



		self.all_BSizer = wx.BoxSizer(orient = wx.VERTICAL)
		self.all_BSizer.Add(self.objectTypesLabel, 1, wx.TOP | wx.BOTTOM| wx.ALL, border=5)
		self.all_BSizer.Add(self.typeChoice, 1, wx.EXPAND| wx.ALL, border=1)
		self.all_BSizer.Add(self.nameLabel, 1, wx.TOP | wx.BOTTOM| wx.ALL, border=5)
		self.all_BSizer.Add(self.nameTextCtrl, 1, wx.EXPAND| wx.ALL, border=1)
		self.all_BSizer.Add(self.btn_BSizer, 1, wx.EXPAND| wx.ALL, border=1)

		self.panel.SetSizer(self.all_BSizer)

		# ===============================================================================
		# EVENT BINDING
		# ===============================================================================
		self.typeChoice.Bind(wx.EVT_CHOICE, self.onSelect)
		self.OKBtn.Bind(wx.EVT_BUTTON, self.onOK)
		self.QuitBtn.Bind(wx.EVT_BUTTON, self.onQuit)

	def onSelect(self, event):
		# print(self.combo.GetValue())
		self.newItemType = self.objectTypes[ self.typeChoice.GetSelection() ]

	def onOK(self, event):
		self.newItemType = self.objectTypes[ self.typeChoice.GetSelection() ]
		self.newItemName = self.nameTextCtrl.GetValue().strip()
		self.EndModal(wx.ID_OK)

	def onQuit(self, event):
		self.Destroy()


class TextDialog(wx.Dialog):
	def __init__(self, parent, content):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, _("edit text"), size=(420, 220), pos=(500, 300))


class MathmlDialog(wx.Dialog):
	def __init__(self, parent, content):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, _("edit mathml"), size=(420, 220), pos=(500, 300))
