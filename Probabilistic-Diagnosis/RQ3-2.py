import os
import pandas as pd


def compute_overall_averages(folder_path):
    seq_times = []
    parallel_times = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)

            # 获取最后一行的 seq_time 和 parallel_compute_time
            last_row = df.iloc[-1]
            seq_times.append(last_row["seq_time"])
            parallel_times.append(last_row["parallel_compute_time"])

    # 计算整体平均值（保留4位小数）
    avg_seq_time = round(sum(seq_times) / len(seq_times), 4)
    avg_parallel_time = round(sum(parallel_times) / len(parallel_times), 4)

    # 生成解释性文本
    explanation = (
        f"在所有测试配置中，串行算法的平均执行时间为 {avg_seq_time} 秒，而并行计算时间的平均值为 {avg_parallel_time} 秒。\n"
        f"这表明，并行算法相比于串行算法减少了计算时间，提高了执行效率。\n"
        f"加速比（speedup）可计算为 {round(avg_seq_time / avg_parallel_time, 4)}，表明并行计算相较于串行计算的加速效果。"
    )

    return explanation


# 运行代码
folder_path = "evaluation/"  # 你的 CSV 文件夹路径
result = compute_overall_averages(folder_path)
print(result)
