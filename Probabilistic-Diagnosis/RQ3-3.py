import os
import pandas as pd


def compute_averages_by_n(folder_path):
    # 初始化存储不同n值的时间列表
    times_by_n = {
        'n5': {'seq': [], 'parallel': []},
        'n6': {'seq': [], 'parallel': []},
        'n7': {'seq': [], 'parallel': []}
    }

    # 遍历文件夹中的CSV文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            # 判断文件名中的n值
            if 'n5' in filename:
                n_key = 'n5'
            elif 'n6' in filename:
                n_key = 'n6'
            elif 'n7' in filename:
                n_key = 'n7'
            else:
                continue

            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)

            # 获取最后一行的时间数据
            last_row = df.iloc[-1]
            times_by_n[n_key]['seq'].append(last_row["seq_time"])
            times_by_n[n_key]['parallel'].append(last_row["parallel_compute_time"])

    # 计算每个n值的平均时间并生成解释文本
    explanation = "不同规模网络的性能分析：\n\n"

    for n_key in times_by_n:
        if times_by_n[n_key]['seq']:  # 确保有数据
            avg_seq = round(sum(times_by_n[n_key]['seq']) / len(times_by_n[n_key]['seq']), 4)
            avg_parallel = round(sum(times_by_n[n_key]['parallel']) / len(times_by_n[n_key]['parallel']), 4)
            speedup = round(avg_seq / avg_parallel, 4)

            explanation += f"{n_key}配置下：\n"
            explanation += f"串行算法平均执行时间: {avg_seq} 秒\n"
            explanation += f"并行算法平均执行时间: {avg_parallel} 秒\n"
            explanation += f"加速比: {speedup}\n\n"

    return explanation


# 运行代码
folder_path = "evaluation/"  # CSV文件夹路径
result = compute_averages_by_n(folder_path)
print(result)
