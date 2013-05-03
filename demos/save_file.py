#coding=utf8

""" 将已知的数据按指定的列顺序写入文件，通过Filds类，我们只需定义每列的名称及其类型，默认值等信息
    通过Fieds对象可转换为按指定顺序的list，该list可作为文件行写入文件
"""

import os
import slimlist.fields as slfields
from slimlist.fields import Fields

definer = (
    ('name', {'field_type': slfields.OPT_STRING, 'title': '用户名'}),
    ('age', {'field_type': slfields.OPT_INT, 'title': '年龄'}),
    ('is_star', {'field_type': slfields.OPT_BOOLEAN, 'title': '是否加星用户', 'default': False}),
)

data = [
    {'id': 1, 'name': 'tonsh', 'age': 16, 'is_star': 1},
    {'id': 2, 'name': 'woody', 'age': 18, 'is_star': 0},
]

def write_file(data):
    with open('./save_user.txt', 'a') as file_obj:
        line = '\t'.join(str(value) for value in data)
        file_obj.write(line)
        file_obj.write('\n')

fields = Fields(definer)
write_file(fields.titles())
for item in data:
    fields.to_list(item, callback=write_file)