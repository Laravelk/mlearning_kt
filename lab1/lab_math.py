import pandas as np
from collections import OrderedDict
import math

# количество определенного элемента в столбце
def count(table, column, element):
	return table[column].count(element)

# удаляем элементы, которые повторились
def delete_values(table, index):
	return {k: [v[i] for i in range(len(v)) if i in index] for k, v in table.items()}

# https://pythonz.net/references/named/dict.fromkeys/
# формируем лист уникальных элементов
def delete_no_unique_values(vals):
	return list(OrderedDict.fromkeys(vals))

# записываем индексы элементов, которые повторились
def get_indexes(table, column, v):
	list = []
	start = 0
	for row in table[column]:
		if row == v:
			index = table[column].index(row, start)
			list.append(index)
			start = index + 1
	return list

# получаем подтаблицу признаков. по факту просто столбец
def get_sub_tablees(table, column):
	delete_dublicate = delete_no_unique_values(table[column])
	sub_table = [delete_values(table, get_indexes(table, column, v)) for v in delete_dublicate]
	return sub_table

# specific conditional entropy
def specific_entropy(table, column, res_column):
	sigma = 0
	for sub_table in get_sub_tablees(table, column):
		sigma += (float(len(sub_table[column])) / len(table[column])) * entropy(sub_table, res_column)
	return sigma

# считаем энтропию для словаря по столбцу
def entropy(table, name_rescol):
	sigma = 0
	for v in delete_no_unique_values(table[name_rescol]):
		h = count(table, name_rescol, v) / float(len(table[name_rescol]))
		sigma += h * math.log(h)
	return (-1) * sigma 

# рассчитывает gain для словаря, признака и заносит в результирующий столбец
def gain(table, sign, name_rescol):
	gain = entropy(table, name_rescol) - specific_entropy(table, sign, name_rescol)
	return gain

# создает дерево важности признаков
def create_tree(table, result):
	column = max([(k, gain(table, k, result)) for k in table.keys() if k != result], key=lambda x: x[1])[0]
	print(column)
	tree = []
	return tree