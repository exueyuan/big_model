# 读取excel文件并把两列转化成python
# 读取excel文件并把两列转化成python，json的格式如下：
# {
#     "汤面": "xxx",
#     "汤底": "xxx",
# }
import pandas as pd
import json

# 读取excel文件
df = pd.read_excel('海龟汤合集_海龟汤_海龟汤合集.xlsx')

# 转化成字典
data = []
# 遍历每一行
for index, row in df.iterrows():
    add_value = {}
    # 获取第一列的值
    key = row["汤面"]
    # 获取第二列的值
    value = row["汤底"]
    # 添加到字典中
    add_value["汤面"] = key
    add_value["汤底"] = value
    data.append(add_value)

# 保存到json文件
with open('data.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
