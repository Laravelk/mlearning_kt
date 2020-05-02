import pandas as pd
import numpy as np
from collections import OrderedDict
from lab_math import gain, create_tree


# функция, которая возвращает первый лист
def get_prepare_data(path):
	file = pd.ExcelFile(path)
	data_frame = file.parse(file.sheet_names[1], skiprows=0, index_col=None, na_values=['None'])
	return data_frame;

# очистим данные в столбце kfg
def clear_kgf_in_data_frame(data_frame):
	kgf_data = data_frame["КГФ"]
	kgf_data = kgf_data / 1000 # уменьшаем значение на три порядка, чтобы с ними было удобней работать
	kgf_data1 = data_frame["КГФ.1"]
	new_data_frame = data_frame.drop(["КГФ.1", "КГФ"], axis=1)
	clear_kgf = pd.concat([kgf_data, kgf_data1], ignore_index=True)
	new_data_frame["КГФ"] = clear_kgf
	return new_data_frame


# удаляем столбцы с единственным значением
def delete_column_with_single_unique_value(data_frame):
	unique_ser = data_frame.nunique()
	unique_data_frame = pd.DataFrame(unique_ser).rename(columns={0:"count_of_unic"})
	unique_data_frame = unique_data_frame.sort_values("count_of_unic", ascending=True)
	unique_columns = pd.DataFrame(unique_ser[unique_ser == 1]).reset_index().rename(columns={"index":"feat"})
	new_data_frame = data_frame.drop(unique_columns["feat"], axis=1)
	return new_data_frame

# удалим столбцы, где много пропущенных значений
#def delete_column_with_bad_data():


if __name__ == '__main__':
	data_frame = get_prepare_data("Test.xlsx")
	data_frame = clear_kgf_in_data_frame(data_frame)

	print("data frame before delete columns with single value")
	print(data_frame)
	new_data_frame = delete_column_with_single_unique_value(data_frame)
	data_frame = delete_column_with_single_unique_value(data_frame)
	print("data frame after delete columns with single value")
	print(new_data_frame)
	
	g_total = new_data_frame["G_total"]
	kgf = new_data_frame["КГФ"]

	print(" ");
	print("print g_total:")
	print(g_total)
	print("kgf")
	print(kgf)

	new_data_frame = new_data_frame.drop(["G_total", "КГФ"], axis=1)
	tmp_buffer = []

	print("Формируем столбец Kgf_total")
	for i, k in zip(g_total, kgf):
		tmp_buffer.append(tuple([i, k]))
	new_data_frame["Kgf_Total"] = list(zip(g_total, kgf))
	print("Сформированный столбец KGF_Total:")
	print(new_data_frame["Kgf_Total"])

	deleted_rows = []

	for index, data in new_data_frame["Kgf_Total"].items():
		if (index == 180):
			print(index)
			pass

		if (np.isnan(data[0]) and np.isnan(data[1])):
			deleted_rows.append(index)

	new_data_frame = new_data_frame.drop(index=deleted_rows)
	print(new_data_frame["Kgf_Total"])

	table = {}
	values = {}
	for i, k in new_data_frame.to_dict().items():
		table[i] = list(k.values())

	for i in new_data_frame.columns.values:
		g = gain(table, i, "Kgf_Total")
		values[i] = g
	print("gain:")
	print(values)



	# задание номер два. Тут мы берем data_frame, а не new_data_frame
	table = {}
	for i, k in data_frame.items():
		table[i] = list(k.values)

	a = create_tree(table, "КГФ")
