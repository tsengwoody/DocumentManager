# -*- coding: utf-8 -*-

class Document(object):
	id = 0
	def __init__(self, label, **kwargs):
		Document.id = Document.id +1
		self.id = Document.id
		self.label = label

	@classmethod
	def create_by_data(cls, data):
		if data['type'] == 'section':
			items_object = []
			for item in data['items']:
				item_object = cls.create_by_data(item)
				items_object.append(item_object)
			obj = Section(label=data['label'], items=items_object)
		elif data['type'] == 'text':
			obj = Text(label=data['label'], content=data['content'])
		elif data['type'] == 'mathml':
			obj = Mathml(label=data['label'], content=data['content'])
		else:
			raise TypeError('type unknown')
		return obj

class Section(Document):

	def __repr__(self):
		return f"<Section name: {self.label}>"

	def __init__(self, label, **kwargs):
		super(Section, self).__init__(label, **kwargs)
		self.type = 'section'
		self.items = kwargs['items']
		self.pointer = None

	@property
	def data(self):
		return {
			'label': self.label,
			"type": self.type,
			'items': [i.data for i in self.items],
		}

	@property
	def lists(self):
		return [{
			'type': item.type,
			'label': item.label,
		} for item in self.items]

	@property
	def contents(self):
		return {type: self.counts(type) for type in ['section', 'text', 'mathml',]}

	def counts(self, type):
		count = 0
		if type=='section':
			for item in self.items:
				if isinstance(item, Section):
					count = count +item.counts('section') +1
		elif type=='text':
			for item in self.items:
				if isinstance(item, Section):
					count = count +item.counts('text')
				elif isinstance(item, Text):
					count = count +1
		elif type=='mathml':
			for item in self.items:
				if isinstance(item, Section):
					count = count +item.counts('mathml')
				elif isinstance(item, Mathml):
					count = count +1

		return count

	def select(self, index):
		self.pointer = self.items[index]
		return True

	def unselect(self):
		self.pointer = None
		return True

	def insert(self, index, obj):
		self.items.insert(index, obj)
		return True

	def remove(self, obj):
		self.items.remove(obj)
		return True

class RootSection(Section):
	def __init__(self, label, **kwargs):
		super(RootSection, self).__init__(label, **kwargs)
		self.path = [self]

	@property
	def current_section(self):
		return self.path[-1]

	@property
	def path_str(self):
		return '/'.join([
			str(document.label) for document in self.path
		])

	def enter(self):
		if self.current_section.pointer and isinstance(self.current_section.pointer, Section):
			self.path.append(self.current_section.pointer)
			return True
		return False

	def leave(self):
		if len(self.path) > 1:
			del self.path[-1]
			return True
		return False

	@classmethod
	def create_by_data(cls, data):
		items_obj = []
		for i in data['items']:
			obj = Document.create_by_data(i)
			items_obj.append(obj)
		document_object = cls(label=data['label'], items=items_obj)
		return document_object

	def export_data(self):
		obj = []
		for itemIndex, item in enumerate( self.current_section.items ):
			if item.type == "section":
				self.current_section.select(itemIndex)
				if self.enter():
					_ = self.export_data()
				self.unselect()
				obj.append( {
					'label': item.label,
					"type": item.type,
					'items': _
				} )
			elif item.type == "text":
				obj.append( {
					'label': item.label,
					"type": item.type,
					'content': item.contents
				} )
			elif item.type == "mathml":
				obj.append( {
					'label': item.label,
					"type": item.type,
					'content': item.contents
				} )
		self.leave()

		return obj

class Text(Document):
	def __init__(self, label, **kwargs):
		super(Text, self).__init__(label, **kwargs)
		self.type = 'text'
		self.content = kwargs['content']

	@property
	def data(self):
		return {
			'label': self.label,
			"type": self.type,
			'content': self.content,
		}

	@property
	def contents(self):
		return self.content

class Mathml(Document):
	def __init__(self, label, **kwargs):
		super(Mathml, self).__init__(label, **kwargs)
		self.type = 'mathml'
		self.content = kwargs['content']

	@property
	def data(self):
		return {
			'label': self.label,
			"type": self.type,
			'content': self.content,
		}

	@property
	def contents(self):
		return self.content

class OperationError(Exception):
	"""Base class for other exceptions"""
	pass


__all__ = ["Document", "Section", "RootSection", "Text", "Mathml", "OperationError"]
# documents = [
# 	{
# 		'label': u'一元二次方程式',
# 		'type': 'section',
# 		'items': [
# 			{
# 				'label': u't1',
# 				'type': 'text',
# 				'content': u'對於',
# 			},
# 			{
# 				'label': u'm1',
# 				'type': 'mathml',
# 				'content': u'<math><mi>a</mi><msup><mi>x</mi><mn>2</mn></msup><mo>+</mo><mi>b</mi><mi>x</mi><mo>+</mo><mi>c</mi><mo>=</mo><mn>0</mn></math>',
# 			},
# 			{
# 				'label': u't2',
# 				'type': 'text',
# 				'content': u'，它的根可以表示為：',
# 			},
# 			{
# 				'label': u'm2',
# 				'type': 'mathml',
# 				'content': u'<math {http://www.w3.org/XML/1998/namespace}lang="zh"><msub ><mi>x</mi><mrow class="MJX-TeXAtom-ORD"><mn>1</mn><mo>,</mo><mn>2</mn></mrow></msub><mo>=</mo><mfrac ><mrow ><mo>−</mo><mi>b</mi><mo>±</mo><msqrt ><msup ><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mi>a</mi><mi>c</mi><mtext></mtext></msqrt></mrow><mrow ><mn>2</mn><mi>a</mi></mrow></mfrac><mrow encoding="application/x-tex"></mrow></math>',
# 			},
# 			{
# 				'label': u't3',
# 				'type': 'text',
# 				'content': u'有些時候也寫成',
# 			},
# 			{
# 				'label': u'm3',
# 				'type': 'mathml',
# 				'content': u'<math {http://www.w3.org/XML/1998/namespace}lang="zh"><msub ><mi>x</mi><mrow class="MJX-TeXAtom-ORD"><mn>1</mn><mo>,</mo><mn>2</mn></mrow></msub><mo>=</mo><mfrac ><mrow ><mo>−</mo><mi>b</mi><mo>±</mo><msqrt ><msup ><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mi>a</mi><mi>c</mi><mtext></mtext></msqrt></mrow><mrow ><mn>2</mn><mi>a</mi></mrow></mfrac><mrow encoding="application/x-tex"></mrow></math>',
# 			},
# 		],
# 	},
# 	{
# 		'label': 'mark',
# 		'type': 'section',
# 		'items': [
# 			{
# 				'label': 'sub sup',
# 				'type': 'mathml',
# 				'content': '<math><msubsup><mi>a</mi><mn>n</mn><mn>2</mn></msubsup><mo>+</mo><msubsup><mi>a</mi><mn>n+1</mn><mn>2</mn></msubsup></math>',
# 			},
# 			{
# 				'label': 'sup',
# 				'type': 'mathml',
# 				'content': '<math><mrow><msup><mi>x</mi><mrow><mi>a</mi><mo>+</mo><mi>b</mi></mrow></msup></mrow></math>',
# 			},
# 			{
# 				'label': 'sub',
# 				'type': 'mathml',
# 				'content': '<math><msub><mi>a</mi><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></msub></math>',
# 			},
# 		],
# 	},
# ]

# documents_obj = []
# for d in documents:
# 	obj = RootSection.create_by_data(d)
# 	documents_obj.append(obj)

# documents_obj[0].current_section.select(1)
# documents_obj[0].enter()
# print(documents_obj[0].lists)
# print(documents_obj[0].contents)
# print(documents_obj[0].path_str)
