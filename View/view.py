import wx

from View.frame_view import FrameView
from View.toolbar_view import ToolBarView2 as ToolBarView
from View.tree_view import TreeView2 as TreeView
from View.component_view import RightTopPanel, RightBottomPanel


class View:
	def __init__(self, model):
		self.model = model
		self.size = wx.Size(1000, 400)
		self.frame = FrameView(None, title='math content manager', size=self.size)
		self.panel = wx.Panel(self.frame, size=self.size)
		self.tree = TreeView(self.panel, self.model.sections)
		self.toolbarPanel = ToolBarView(self.panel, {
			'path': self.model.path,
			'current_section': self.model.current_section,
		})
		self.rightTopPanel = RightTopPanel(
			self.panel, data=self.model.current_section,
			pos=(self.frame.Size.width / 4, 70), size=(self.frame.Size.width * 3 / 4 - 15, self.frame.Size.height / 3),
		)
		self.rightBottomPanel = RightBottomPanel(
			self.panel, data=self.model.current_section,
			pos=(self.frame.Size.width / 4, self.frame.Size.height / 2),
			size=(self.frame.Size.width * 3 / 4 - 15, self.frame.Size.height / 2 - 40),
		)

		self.frame.show(True)
