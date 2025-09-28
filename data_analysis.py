import os
import pandas as pd
import numpy as np

# 设定 txt 文件夹的路径和输出的 Excel 文件名
txt_folder = 'F:\B208\Publish_A_Deep_Learning-Assisted_Comprehensive_Evaluation_Method_for_the_Morphology_of_SWNT_Arrays\Figure3'
output_excel = 'F:/B208/Publish_A_Deep_Learning-Assisted_Comprehensive_Evaluation_Method_for_the_Morphology_of_SWNT_Arrays/Figure3/test.xlsx'

# 初始化一个空的字典，存储所有的数据
data_dict = {}

# 遍历文件夹中的所有 txt 文件
for filename in os.listdir(txt_folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(txt_folder, filename)
        
        # 获取文件名的第一个单词作为 y 列名
        y_column_name = filename.split()[0]
        
        # 打开并读取文件内容
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    # 用逗号分割每行数据，提取 x 和 y
                    x_value, y_value = line.strip().split(',', 1)
                    x_value = float(x_value)  # 假设 x 是数字
                    y_value = float(y_value)  # 假设 y 也是数字
                    
                    # 将 x 值调整为循环角度
                    if x_value < 0:
                        x_value += 180  # 将负角度调整为正角度
                    elif x_value <= 2.5:
                        x_value = 177.5  # 将 0 到 2.5 的角度调整为 177.5
                
                    # 如果 x 值不在字典中，初始化为一个空字典
                    if x_value not in data_dict:
                        data_dict[x_value] = {}
                    
                    # 将 y 值存储在以文件名命名的列下
                    data_dict[x_value][y_column_name] = y_value
                
                except ValueError:
                    # 如果 x 或 y 不是数字，则跳过这一行
                    print(f"跳过无法解析的行: {line.strip()}")
                    continue

# 将数据转换为 DataFrame
df_final = pd.DataFrame.from_dict(data_dict, orient='index').reset_index().rename(columns={'index': 'x'})

# 将 NaN 替换为 0（即没有对应的 y 值时）
df_final.fillna(0, inplace=True)

# 归一化每一列：每列的所有数值除以该列数值之和
for column in df_final.columns[1:]:  # 跳过第一列 'x'
    column_sum = df_final[column].sum()
    if column_sum != 0:  # 避免除以 0
        df_final[column] = df_final[column] / column_sum

# 定义循环的5度区间，从-2.5开始到180
bins = np.arange(-2.5, 182.5, 5)  # 从-2.5到180.5，步长为5
labels = np.arange(0, 180, 5)  # 标签从0开始，每5度一个，共36个标签

# 使用 pd.cut 创建分组，按照定义的区间进行分段
df_final['bin'] = pd.cut(df_final['x'], bins=bins, labels=labels, include_lowest=True)

# 创建一个 DataFrame 存储加和后的结果
df_binned = pd.DataFrame({'bin': labels})  # 保留标签数量

# 对每列的 y 值按分组进行加和
for column in df_final.columns[1:-1]:  # 跳过 'x' 和 'bin' 列
    binned_sums = df_final.groupby('bin')[column].sum().reindex(df_binned['bin']).reset_index(drop=True)
    
    # 将分组加和的结果存储到新的 DataFrame 中
    df_binned[column] = binned_sums

# 保存到 Excel 文件
df_binned.to_excel(output_excel, index=False)

print(f"数据已成功保存到 {output_excel}")
