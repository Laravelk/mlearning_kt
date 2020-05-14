import pandas as pd
import numpy as np
from collections import OrderedDict
from lab_math import gain
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

plt.figure(figsize = (25,25))


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

# удаляем значения
def identify_missing(data_frame, treshold):
	missing_ser = data_frame.isnull().sum() / data_frame.shape[0]
	missing = pd.DataFrame(missing_ser)
	missing = missing.sort_values(0, ascending = False)
	missing_columns = pd.DataFrame(missing_ser[missing_ser>treshold]).reset_index().rename(columns = {'index' : 'feat', 0 : '% Nones'})
	data_frame_drop = data_frame.drop(missing_columns["feat"], axis = 1)
	return data_frame_drop
def identify_collinear(data_frame, treshold):
	correct_matrix = data_frame.corr()
	lower = correct_matrix.where(np.tril(np.ones(correct_matrix.shape), k = -1).astype(np.bool))
	drop_columns = [column for column in lower.columns if any(lower[column].abs() >treshold)]
	new_data_frame = data_frame.drop(drop_columns, axis = 1)
	cmap = sns.cubehelix_palette(as_cmap = True, light=.9)
	krg = sns.heatmap(lower, annot = True, cmap=cmap)
	plt.show()
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
	print("data frame after delete columns with single value")
	print(new_data_frame)

	# откоментировать блок для heatmap
	#new_data_frame = identify_missing(new_data_frame, 0.4)
	#new_data_frame = identify_collinear(new_data_frame, 0.98)
	# конец блока
	
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
	plt.bar(values.keys(), values.values())
	plt.show()


	# откоментировать для heatmap
	#data_column = data_frame["дд.мм.гггг"]
	#replace = data_frame.drop(["дд.мм.гггг"], axis = 1)
	#for i in data_frame.columns.values:
	#	gistogram(data_frame, i)
	#конец блока

