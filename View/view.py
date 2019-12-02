import wx

from View.frame_view import FrameView
from View.toolbar_view2 import ToolBarView2 as ToolBarView
from View.tree_view2 import TreeView2 as TreeView
from View.component_view2 import RightTopPanel, RightBottomPanel
from Model.model import Model2 as Model


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
