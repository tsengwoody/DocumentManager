import json
from fakedata import documents
from enums import PanelType, ActionType
from pubsub import pub


class Model:
	"""
		每次更新皆需發送以下資料給 UI 顯示，需額外加 index_path 資訊，以便 UI 操作時傳訊給 model
		current section ：右上當前資料夾內容
		sections ：左側資料夾樹
		path ：路徑
		raw data ：選定物件的原始資料
		html data ：選定物件的轉換 html 資料
	"""

	def __init__(self):
		# data = documents
		# json.dump(data, open(path, "w"))
		data = json.load(open('save.json'))
		self.data = data

		# index_path 放入逐層的索引項來指到特定物件
		# 最後一項代表選取項目，可為 -1 代表無選取項目
		self.index_path = [0, -1]

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

	@classmethod
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
	def root_section(self):
		"""
			return: {
				'index_path': [0,1,1],
				'data': {...}, # 當前資料夾的資料，需含 index_path
			}
		"""
		return {
			'index_path': self.index_path[:1],
			'data': self.get_node_by_index_path(self.index_path[:1]),
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
		data = {
			'index_path': self.index_path,
			'data': self.get_node_by_index_path(self.index_path),
		} if not self.index_path[-1] == -1 else None
		return data

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

	def announcement(self):
		# 將結果發布給訂閱者。
		for event in [
			'sections',
			'root_section',
			'current_section',
			'path',
			'pointer_raw_data',
			'pointer_html_data',
		]:
			try:
				pub.sendMessage(event, data=getattr(self, event))
			except BaseException as e:
				print(event)
				print('error:', str(e))  

	# === 操作修改資料 ===
	def set_index_path(self, data):
		"""
			資料格式：data: {
				'index_path': [0,1,1], # 要放入的位置
			}
			判斷：如果 index_path 為不存在的 index 則 raise exception
		"""
		old_index_path = self.index_path
		self.index_path = data['index_path']
		if not self.index_path[0] == old_index_path[0]:
			try:
				pub.sendMessage('root_section', data=getattr(self, 'root_section'))
			except BaseException as e:
				print('root_section')
				print('error:', str(e))
		if not self.index_path[:-1] == old_index_path[:-1]:
			try:
				pub.sendMessage('current_section', data=getattr(self, 'current_section'))
			except BaseException as e:
				print('current_section')
				print('error:', str(e))

		for event in ['path', 'pointer_raw_data', 'pointer_html_data']:
			try:
				pub.sendMessage(event, data=getattr(self, event))
			except BaseException as e:
				print(event)
				print('error:', str(e))

	def append(self, data):
		self.data.append(data)
		self.set_descendant_index_path(self.data[-1], [len(self.data) - 1])
		self.announcement()

	def add(self, data):
		"""
			資料格式：data: {
				'index_path': [0,1,1], # 要放入的位置
				'data': {...}, # 要放入的資料
			}
			判斷：如果 index_path 除最後一個外有不存在的 index 則 raise exception
			筆記：
			index_path=[0,0,-1]時，在index_path=[0,0]的地方加入data；
			index_path=[0,0,1] 時，在index_path=[0,0,2]的地方加入data。
		"""
		# print(data['index_path'], data['data']['label']) #for test purpose only
		prev_index_path = data['index_path'][:-1]
		index = data['index_path'][-1] #index是index_path的最後一個數字
		try:
			node = self.get_node_by_index_path(prev_index_path)
		except BaseException as e:
			print('index_path:', previous_index_path)
			print('error:', str(e)) 

		# 左側樹選在在最頂層資料夾
		if not node and data['data'] == 'section':
			node = self.data
			# 插入data。
			if index == -1:
				node.append(data['data'])
			else:
				node.insert(index + 1, data['data'])
				for index, node in enumerate(self.data):
					self.set_descendant_index_path(node, [index])
		else:
			# node底下如果沒有'items'時，將node['items']初始化。
			if 'items' not in node:
				node['items'] = []

			# 插入data。
			if index == -1:
				node['items'].append(data['data'])
			else:
				node['items'].insert(index + 1, data['data'])

			# 更新在node之下所有子節點的index_path：
			self.set_descendant_index_path(node, prev_index_path)

		# 將結果發布給訂閱者。
		self.announcement()

	def update(self, data):
		"""
			data: {
				'index_path': [0,1,1], # 要更新的位置
				'data': {...}, # 要更新的資料
			}
			判斷：如果 index_path 有不存在的 index 則 raise exception
		"""
		print(data['index_path'])
		node = self.get_node_by_index_path(data['index_path'])
		node['label'] = data['data']['label']
		self.announcement() #將結果發布給訂閱者。


	def remove(self, data):
		"""
			data: {
				'index_path': [0,1,1], # 要刪除的位置
			}
			判斷：如果 index_path 有不存在的 index 則 raise exception
		"""

		prev_index_path = data['index_path'][:-1]
		index = data['index_path'][-1] #index是index_path的最後一個數字
		try:
			self.get_node_by_index_path(prev_index_path + [index])
		except BaseException as e:
			print('index_path:', prev_index_path + [index])
			print('error:', str(e))
		node = self.get_node_by_index_path(prev_index_path)

		# 刪除資料
		node['items'].pop(index)

		# 更新在node之下所有子節點的index_path：
		self.set_descendant_index_path(node, prev_index_path)

		# 將結果發布給訂閱者。
		self.announcement()

	def move(self, data):
		"""
			data: {
				'old_index_path': [0,1,1], # 要搬移前的位置
				'new_index_path': [0,1,3], # 要搬移後的位置
			}
			判斷：如果 index_path 有不存在的 index 則 raise exception
		"""

		old_index_path = data['old_index_path'][:-1]
		old_index = data['old_index_path'][-1]
		try:
			self.get_node_by_index_path(old_index_path + [old_index])
		except BaseException as e:
			print('index_path:', prev_index_path + [index])
			print('error:', str(e))	 

		# 搬移出資料
		obj = self.get_node_by_index_path(old_index_path)['items'].pop(old_index)

		new_index_path = data['new_index_path'][:-1]
		new_index = data['new_index_path'][-1]
		try:
			self.get_node_by_index_path(new_index_path)
		except BaseException as e:
			print('index_path:', prev_index_path + [index])
			print('error:', str(e))	 

		# 搬移入資料
		node = self.get_node_by_index_path(new_index_path)
		node['items'].insert(new_index, obj)

		# 整個資料重新更新
		for index, node in enumerate(self.data):
			self.set_descendant_index_path(node, [index])

		# 將結果發布給訂閱者。
		self.announcement()
