import wx
from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

useNotifyByWriteFile(sys.stdout)

from Model.model import Model2 as Model
from View.view import View

# 測試是否不同事件會對應不同 method 所用
def decorate_event(event):
	def outer_d_f(f):
		def d_f(data, *args, **kargs):
			print("%s before call" % (event))
			result = f(data, *args, **kargs)
			print("%s after call" % (event))
			return result
		return d_f
	return outer_d_f

def show(data):
	pass
	#print(data)


class DocumentManagerApp:
	def __init__(self):
		self.model = Model()
		self.view = View(self.model)
		self.model.set_index_path({'index_path': [0, -1]})

		# subscribe for model
		model_function = {
			'set_index_path': self.model.set_index_path,
			'add': self.model.add,
			'update': self.model.update,
			'remove': self.model.remove,
		}

		for event, func in model_function.items():
			pub.subscribe(func, event)

		# subscribe for view
		view_function = {
			'current_section': decorate_event('current_section')(show),
			'sections': decorate_event('sections')(show),
			'path': decorate_event('path')(show),
			'pointer_raw_data': decorate_event('pointer_raw_data')(show),
			'pointer_html_data': decorate_event('pointer_html_data')(show),
		}

		for event, func in view_function.items():
			pub.subscribe(func, event)

		pub.sendMessage('set_index_path', data={'index_path': [0, -1]})

if __name__ == "__main__":
	app = wx.App()
	#實例一定要assign到一個變數，不然會被自動回收
	d = DocumentManagerApp()
	app.MainLoop()
