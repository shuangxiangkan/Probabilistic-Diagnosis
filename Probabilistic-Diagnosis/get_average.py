import os
import pandas as pd


def compute_averages(folder_path):
    # 遍历文件夹中的所有 CSV 文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)

            # 读取 CSV 文件
            df = pd.read_csv(file_path)

            # 复制前5列原始值
            avg_row = df.tail(1).copy()

            # 计算后面列的均值并保留4位小数
            avg_values = df.tail(10).iloc[:, 5:].mean().round(4)

            # 更新计算出的均值到 avg_row
            avg_row.iloc[0, 5:] = avg_values.values

            # 将均值作为新行追加
            df = pd.concat([df, avg_row], ignore_index=True)

            # 写回 CSV 文件
            df.to_csv(file_path, index=False)
            print(f"Processed: {filename}")


# 使用示例
folder_path = "evaluation/p"  # 替换为你的文件夹路径
compute_averages(folder_path)
