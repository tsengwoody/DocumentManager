from fakedata import documents
from enums import PanelType, ActionType
from pubsub import pub


class Model:
	def __init__(self, controller):
		self.ori_data = {'items': documents}
		self.data = {'items': documents[0]['items'], 'index':[0], 'layer': 0, 'label':documents[0]['label'], 'type':documents[0]['type']}
		self.event_name = ['data_changed', 'count_changed']
		self.controller = controller

	def count_item(self):
		list_item = {}
		for item in self.data['items']:
			if item['type'] in list_item:
				list_item[item['type']] = list_item[item['type']] + 1
			else:
				list_item[item['type']] = 1
		return [{'type':k, 'label':v} for k, v in list_item.items()]

	def updateItem(self, data):
		index_array = self.data['index']
		layer = data['layer'] if 'layer' in data else self.data['layer']
		if 'action' in data:
			self.data['action'] = data['action']
		elif 'action' in self.data:
			del self.data['action'] 
		count_data_items = []
		if 'index' in data:
			# from tree_view.py
			if isinstance(data['index'], list):
				index_array = data['index']
			# from panels_view.py
			else:
				index_array.insert(layer, data['index'])
			del index_array[layer+1:]
		source = self.ori_data['items']
		path_str = ""
		for idx, val in enumerate(index_array):
			if (len(index_array)-1 == idx):
				if val >= len(source):
					source.append({'label': data['label'], 'type': data['type'], 'items': data['items'] if 'items' in data else []})
				elif 'label' in data and (source[val]['label'] != data['label']):
					source[val]['label'] = data['label']
				elif 'action' in data and data['action'] == ActionType.DEL.value:
					del source[val]
					val = 0
					index_array[-1] = val
					if len(source)==0:
						break
			path_str = path_str + ('' if idx==0 else '/') + source[val]['label']
			self.data['type'] = source[val]['type']
			if 'items' in source[val]:
				source = source[val]['items']
				self.data['items'] = source
				count_data_items = self.count_item()
				for idy, item in enumerate(self.data['items']):
					self.data['items'][idy]['layer'] = layer + 1
			else:
				del self.data['items']
				self.data['content'] = source[val]['content']
				source = []
		self.data['index'] = index_array
		self.data['index_array'] = index_array
		self.data['label'] = path_str
		self.data['layer'] = layer
		if 'index' in data:
			if isinstance(data['index'], list):
				current_index = data['index'][-1]
			else:
				current_index = data['index']
		else:
			current_index = index_array[-1]
		data = self.data.copy()
		data['index'] = current_index
		count_data = data.copy()
		if 'action' not in data or data['action'] == ActionType.NONE.value:
			if 'items' in data:
				self.controller.sendMessage(self.event_name[0], data=data)
		if 'action' in data:
			if data['action'] == ActionType.COUNTING.value:
				if data['type'] == PanelType.SECTION.value:
					count_data['items'] = count_data_items
			elif data['action'] == ActionType.DEL.value:
				self.controller.sendMessage('data_changedTree', data=self.ori_data)
			count_data['clickable'] = False
			self.controller.sendMessage(self.event_name[1], data=count_data)
