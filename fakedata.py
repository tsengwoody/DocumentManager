from Model.documentManager import *

# ============================================================================================================================================
# 新版資料
# ============================================================================================================================================
# 原始資料
documents = [
	{
		'label': u'一元二次方程式',
		'type': 'section',
		'items': [
			{
				'label': u'公式解法',
				'type': 'section',
				'items': [
					{
						'label': u'XDDDD',
						'type': 'section',
						'items': [
							
							{
								'label': u'OMGGGGG',
								'type': 'text',
								'content': u'對於',
							},
						]
					},
					{
						'label': u'Second t1',
						'type': 'text',
						'content': u'對於',
					},
					{
						'label': u'Second m1',
						'type': 'mathml',
						'content': u'<math><mi>a</mi><msup><mi>x</mi><mn>2</mn></msup><mo>+</mo><mi>b</mi><mi>x</mi><mo>+</mo><mi>c</mi><mo>=</mo><mn>0</mn></math>',
					},
					{
						'label': u'Second t2',
						'type': 'text',
						'content': u'，它的根可以表示為：',
					},
					{
						'label': u'Second m2',
						'type': 'mathml',
						'content': u'<math {http://www.w3.org/XML/1998/namespace}lang="zh"><msub ><mi>x</mi><mrow class="MJX-TeXAtom-ORD"><mn>1</mn><mo>,</mo><mn>2</mn></mrow></msub><mo>=</mo><mfrac ><mrow ><mo>−</mo><mi>b</mi><mo>±</mo><msqrt ><msup ><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mi>a</mi><mi>c</mi><mtext></mtext></msqrt></mrow><mrow ><mn>2</mn><mi>a</mi></mrow></mfrac><mrow encoding="application/x-tex"></mrow></math>',
					},
					{
						'label': u'Second t3',
						'type': 'text',
						'content': u'有些時候也寫成',
					},
					{
						'label': u'Second m3',
						'type': 'mathml',
						'content': u'<math {http://www.w3.org/XML/1998/namespace}lang="zh"><msub ><mi>x</mi><mrow class="MJX-TeXAtom-ORD"><mn>1</mn><mo>,</mo><mn>2</mn></mrow></msub><mo>=</mo><mfrac ><mrow ><mo>−</mo><mi>b</mi><mo>±</mo><msqrt ><msup ><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mi>a</mi><mi>c</mi><mtext></mtext></msqrt></mrow><mrow ><mn>2</mn><mi>a</mi></mrow></mfrac><mrow encoding="application/x-tex"></mrow></math>',
					},
				],
			},
			{
				'label': u't1',
				'type': 'text',
				'content': u'對於',
			},
			{
				'label': u'm1',
				'type': 'mathml',
				'content': u'<math><mi>a</mi><msup><mi>x</mi><mn>2</mn></msup><mo>+</mo><mi>b</mi><mi>x</mi><mo>+</mo><mi>c</mi><mo>=</mo><mn>0</mn></math>',
			},
			{
				'label': u't2',
				'type': 'text',
				'content': u'，它的根可以表示為：',
			},
			{
				'label': u'm2',
				'type': 'mathml',
				'content': u'<math {http://www.w3.org/XML/1998/namespace}lang="zh"><msub ><mi>x</mi><mrow class="MJX-TeXAtom-ORD"><mn>1</mn><mo>,</mo><mn>2</mn></mrow></msub><mo>=</mo><mfrac ><mrow ><mo>−</mo><mi>b</mi><mo>±</mo><msqrt ><msup ><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mi>a</mi><mi>c</mi><mtext></mtext></msqrt></mrow><mrow ><mn>2</mn><mi>a</mi></mrow></mfrac><mrow encoding="application/x-tex"></mrow></math>',
			},
			{
				'label': u't3',
				'type': 'text',
				'content': u'有些時候也寫成',
			},
			{
				'label': u'm3',
				'type': 'mathml',
				'content': u'<math {http://www.w3.org/XML/1998/namespace}lang="zh"><msub ><mi>x</mi><mrow class="MJX-TeXAtom-ORD"><mn>1</mn><mo>,</mo><mn>2</mn></mrow></msub><mo>=</mo><mfrac ><mrow ><mo>−</mo><mi>b</mi><mo>±</mo><msqrt ><msup ><mi>b</mi><mn>2</mn></msup><mo>−</mo><mn>4</mn><mi>a</mi><mi>c</mi><mtext></mtext></msqrt></mrow><mrow ><mn>2</mn><mi>a</mi></mrow></mfrac><mrow encoding="application/x-tex"></mrow></math>',
			},
		],
	},
	{
		'label': 'mark',
		'type': 'section',
		'items': [
			{
				'label': 'sub sup',
				'type': 'mathml',
				'content': '<math><msubsup><mi>a</mi><mn>n</mn><mn>2</mn></msubsup><mo>+</mo><msubsup><mi>a</mi><mn>n+1</mn><mn>2</mn></msubsup></math>',
			},
			{
				'label': 'sup',
				'type': 'mathml',
				'content': '<math><mrow><msup><mi>x</mi><mrow><mi>a</mi><mo>+</mo><mi>b</mi></mrow></msup></mrow></math>',
			},
			{
				'label': 'sub',
				'type': 'mathml',
				'content': '<math><msub><mi>a</mi><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></msub></math>',
			},
			{
				'label': 'XD',
				'type': 'mathml',
				'content': '<math></math>',
			},
			{
				'label': u'又一個',
				'type': 'section',
				'items': [
					
					{
						'label': u'OMGGGGG',
						'type': 'text',
						'content': u'對於',
					},
					{
						'label': u'下一個',
						'type': 'section',
						'items': [
							
							{
								'label': u'OMGGGGG',
								'type': 'text',
								'content': u'對於',
							},
							{
								'label': u'1231321',
								'type': 'text',
								'content': u'對於',
							},
							{
								'label': u'第三層',
								'type': 'section',
								'items': [
									
									{
										'label': u'1111',
										'type': 'text',
										'content': u'對於',
									},
									{
										'label': u'2222',
										'type': 'text',
										'content': u'對於',
									},
									
									{
										'label': u'3333',
										'type': 'text',
										'content': u'對於',
									},
								]
							},
						]
					},
				]
			},
		],
	},
]

documents_obj = []
for d in documents:
	obj = RootSection.create_by_data(d)
	documents_obj.append(obj)


# ============================================================================================================================================
# 舊版資料
# ============================================================================================================================================


data = [
	{
		'name': 'fraction',
		'items': [
			{
				'name': 'fraction',
				'content': '<math><mrow><mfrac><mn>3</mn><mrow><mn>1</mn><mo>+</mo><mi>x</mi></mrow></mfrac></mrow></math>',
			},
			{
				'name': 'single fraction',
				'content': '<math><mfrac><mi>3</mi><mi>4</mi></mfrac></math>',
			},
			{
				'name': 'add integer fraction1',
				'content': '<math><mn>17</mn><mfrac><mn>2</mn><mn>5</mn></mfrac></math>',
			},
			{
				'name': 'add integer fraction2',
				'content': '<math><mn>17</mn><mfrac><mn>2</mn><mn>5</mn></mfrac></math>',
			},
			{
				'name': 'add integer fraction3',
				'content': '<math><mn>17</mn><mfrac><mn>2</mn><mn>5</mn></mfrac></math>',
			},
		],
	},
	{
		'name': 'mark',
		'items': [
			{
				'name': 'sub sup',
				'content': '<math><msubsup><mi>a</mi><mn>n</mn><mn>2</mn></msubsup><mo>+</mo><msubsup><mi>a</mi><mn>n+1</mn><mn>2</mn></msubsup></math>',
			},
			{
				'name': 'sup',
				'content': '<math><mrow><msup><mi>x</mi><mrow><mi>a</mi><mo>+</mo><mi>b</mi></mrow></msup></mrow></math>',
			},
			{
				'name': 'sub',
				'content': '<math><msub><mi>a</mi><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></msub></math>',
			},
		],
	},
]



__all__ = ["data", "documents", "documents_obj"]