from pubsub import pub
from Model.model import Model

model = Model()
print(model.index_path)
print(getattr(model, 'path'))

# 測試改變路徑
model.set_index_path({'index_path': [0, 0, 2]})
model.set_index_path({'index_path': [1, -1]})

print(model.sections)
print(getattr(model, 'current_section')['index_path'])

# 測試model的add方法
print("#"*30)
print("測試model的add方法")
print("#"*30)
add_data1 = {
	'index_path': [1,0], # 要放入的位置
	'data': {
		'label':'add_data_1',
		'type':'text', 
		'content':'content_add_data_1'
	} # 要放入的資料
}
model.add(add_data1)
print()
print("#"*30)
print("after 'add add_data1' @[1,0]")
print("#"*30)
print(model.data[1])


add_data2 = {
	'index_path': [1,-1], # 要放入的位置
	'data': {
	'label':'add_data_2',
	'type':'text', 
	'content':'content_add_data_2'} # 要放入的資料
}
model.add(add_data2)
print()
print("#"*30)
print("after add 'add_data2' @[1,-1]")
print("#"*30)
print(model.data[1])

# 測試model的remove方法
print()
print("#"*30)
print("測試model的remove方法")
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
