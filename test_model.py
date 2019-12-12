from pubsub import pub
from Model.model import Model2

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
	print(data)

fs = {
	'current_section': decorate_event('current_section')(show),
	'sections': decorate_event('sections')(show),
	'path': decorate_event('path')(show),
	'pointer_raw_data': decorate_event('pointer_raw_data')(show),
	'pointer_html_data': decorate_event('pointer_html_data')(show),
}

model = Model2()
print(model.index_path)
print(getattr(model, 'path'))

# 測試改變路徑
print('before subscribe')
model.set_index_path({'index_path': [0, 0, 2]})

for event, func in fs.items():
	pub.subscribe(func, event)

print('after subscribe')
model.set_index_path({'index_path': [1, -1]})
print(model.sections)
print(getattr(model, 'current_section')['index_path'])



# 測試model2的add方法
print("#"*30)
print("測試model2的add方法")
print("#"*30)
add_data1 = {
    'index_path': [1,0], # 要放入的位置
    'data': {'label':'add_data_1',
             'type':'text', 
             'content':'content_add_data_1'} # 要放入的資料
			}
model.add(add_data1)
print()
print("#"*30)
print("after 'add add_data1' @[1,0]")
print("#"*30)
print(model.data[1])


add_data2 = {
    'index_path': [1,-1], # 要放入的位置
    'data': {'label':'add_data_2',
             'type':'text', 
             'content':'content_add_data_2'} # 要放入的資料
			}
model.add(add_data2)
print()
print("#"*30)
print("after add 'add_data2' @[1,-1]")
print("#"*30)
print(model.data[1])


# 測試model2的remove方法
print()
print("#"*30)
print("測試model2的remove方法")
print("#"*30)
remove_data1 = {
    'index_path': [1,0], # 要放入的位置
			}
model.remove(remove_data1)
print()
print("#"*30)
print("after remove data @[1,0]")
print("#"*30)
print(model.data[1])

