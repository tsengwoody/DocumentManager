from fakedata import documents
from enums import PanelType, ActionType
from pubsub import pub


class Model2:
	"""
		每次更新皆需發送以下資料給 UI 顯示，需額外加 index_path 資訊，以便 UI 操作時傳訊給 model
		current section ：右上當前資料夾內容
		sections ：左側資料夾樹
		path ：路徑
		raw data ：選定物件的原始資料
		html data ：選定物件的轉換 html 資料
	"""

	def __init__(self):
		self.data = documents

		# index_path 放入逐層的索引項來指到特定物件
		# 最後一項代表選取項目，可為 -1 代表無選取項目
		self.index_path = [0, 0, 1]

		for index, node in enumerate(self.data):
			self.set_descendant_index_path(node, [index])

	def get_node_by_index_path(self, index_path):
		pointer = None
		for node in self.visit_node_by_index_path(index_path):
			pointer = node
		return pointer

	def visit_node_by_index_path(self, index_path):
		pointer = None
		for i, index in enumerate(index_path):
			# 特例，最上層為一個多文件的 list
			if i == 0:
				pointer = self.data[index]
			else:
				pointer = pointer['items'][index]
			yield pointer

	@classmethod
	def set_descendant_index_path(cls, node, index_path):
		node['index_path'] = index_path
		if node['type'] == 'section':
			for index, child in enumerate(node['items']):
				child_index_path = index_path + [index]
				cls.set_descendant_index_path(child, child_index_path)

	def get_descendant_sections(cls, node):
		child_sections = []
		if node['type'] == 'section':
			for child in node['items']:
				if child['type'] == 'section':
					child_sections.append(cls.get_descendant_sections(child))

		return {
			'index_path': node['index_path'],
			'label': node['label'],
			'items': child_sections,
		}

	@property
	def current_section(self):
		"""
			return: {
				'index_path': [0,1,1],
				'data': {...}, # 當前資料夾的資料，需含 index_path
			}
		"""
		return {
			'index_path': self.index_path[:-1],
			'data': self.get_node_by_index_path(self.index_path[:-1]),
		}

	@property
	def sections(self):
		"""
			return: [
				{
					'index_path': [0,1,1], # 節點的 index_path
					'label': '', # 節點的顯示 label
					'items': [...], # 子節點
				}, ...
			]
		"""
		return [
			self.get_descendant_sections(self.data[i]) for i in range(len(self.data))
		]

	@property
	def path(self):
		path = []
		for node in self.visit_node_by_index_path(self.index_path[:-1]):
			path.append(node['label'])

		return '/'.join(path)

	@property
	def pointer_raw_data(self):
		"""
			return: {
				'index_path': [0,1,1],
				'data': {...}, # 選定物件的 raw
			}
		"""
		return {
			'index_path': self.index_path if not self.index_path[-1] == -1 else None,
			'data': self.get_node_by_index_path(self.index_path) if not self.index_path[-1] == -1 else None,
		}

	@property
	def pointer_html_data(self):
		"""
			return: {
				'index_path': [0,1,1],
				'data': {...}, # 選定物件的 html
			}
		"""
		return {
			'index_path': self.index_path if not self.index_path[-1] == -1 else None,
			'data': self.get_node_by_index_path(self.index_path) if not self.index_path[-1] == -1 else None,
		}

	# === 操作修改資料 ===
	def set_index_path(self, data):
		"""
			資料格式：data: {
				'index_path': [0,1,1], # 要放入的位置
			}
			判斷：如果 index_path 為不存在的 index 則 raise exception
		"""
		self.index_path = data['index_path']
		for event in ['current_section', 'sections', 'path', 'pointer_raw_data', 'pointer_html_data']:
			try:
				pub.sendMessage(event, data=getattr(self, event))
			except BaseException as e:
				print(event)
				print('error:', str(e))

	def add(self, data):
		"""
			資料格式：data: {
				'index_path': [0,1,1], # 要放入的位置
				'data': {...}, # 要放入的資料
			}
			判斷：如果 index_path 除最後一個外有不存在的 index 則 raise exception
		"""
		pass

	def update(self, data):
		"""
			data: {
				'index_path': [0,1,1], # 要更新的位置
				'data': {...}, # 要更新的資料
			}
			判斷：如果 index_path 有不存在的 index 則 raise exception
		"""
		pass

	def remove(self, data):
		"""
			data: {
				'index_path': [0,1,1], # 要刪除的位置
			}
			判斷：如果 index_path 有不存在的 index 則 raise exception
		"""
		pass


# layer: current folder layer number in data
# index: current item index number in a layer

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
