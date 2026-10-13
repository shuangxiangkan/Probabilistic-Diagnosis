import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 画整体图，不区分p,n,beta,gamma
def extract_final_rows(folder_path):
    data = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            last_row = df.iloc[-1]  # 获取最后一行

            # 提取关键数据
            n, k, p, beta, gamma = last_row[:5]
            seq_time = last_row["seq_time"]
            parallel_time = last_row["parallel_compute_time"]

            data.append([n, k, p, beta, gamma, seq_time, parallel_time])

    return pd.DataFrame(data, columns=["n", "k", "p", "beta", "gamma", "seq_time", "parallel_time"])


def plot_results(df, output_folder):
    os.makedirs(output_folder, exist_ok=True)  # 创建存储图表的文件夹

    # 创建索引用于绘图
    df["index"] = np.arange(len(df))

    # 1. 折线图（Line Plot）
    plt.figure(figsize=(10, 5))
    plt.plot(df["index"], df["seq_time"], label="Sequential Time", marker='o', linestyle='-')
    plt.plot(df["index"], df["parallel_time"], label="Parallel Time", marker='s', linestyle='--')
    plt.xlabel("Different Configurations")
    plt.ylabel("Execution Time (s)")
    plt.legend()
    plt.title("Sequential vs Parallel Execution Time")
    plt.grid()
    plt.savefig(os.path.join(output_folder, "line_plot.pdf"))  # 保存为 PDF
    plt.show()

    # 2. 柱状图（Bar Chart）
    plt.figure(figsize=(12, 6))
    bar_width = 0.4
    x = np.arange(len(df))
    plt.bar(x - bar_width / 2, df["seq_time"], width=bar_width, label="Sequential Time")
    plt.bar(x + bar_width / 2, df["parallel_time"], width=bar_width, label="Parallel Time")
    plt.xlabel("Different Configurations")
    plt.ylabel("Execution Time (s)")
    plt.legend()
    # plt.title("Comparison of Sequential and Parallel Execution Time")
    plt.xticks([])
    plt.grid(axis='y')
    plt.savefig(os.path.join(output_folder, "bar_chart.pdf"))  # 保存为 PDF
    plt.show()

    # 3. 散点图（Scatter Plot）
    plt.figure(figsize=(6, 6))
    plt.scatter(df["seq_time"], df["parallel_time"], alpha=0.7)
    plt.plot([df["seq_time"].min(), df["seq_time"].max()],
             [df["seq_time"].min(), df["seq_time"].max()],
             linestyle="--", color="red")  # y = x 线
    plt.xlabel("Sequential Time (s)")
    plt.ylabel("Parallel Time (s)")
    plt.title("Scatter Plot: Sequential vs Parallel Execution Time")
    plt.grid()
    plt.savefig(os.path.join(output_folder, "scatter_plot.pdf"))  # 保存为 PDF
    plt.show()

    # 4. 加速比折线图（Speedup Line Plot）
    df["speedup"] = df["seq_time"] / df["parallel_time"]
    plt.figure(figsize=(10, 5))
    plt.plot(df["index"], df["speedup"], marker='o', linestyle='-')
    plt.xlabel("Different Configurations")
    plt.ylabel("Speedup (seq_time / parallel_time)")
    plt.title("Speedup of Parallel Execution")
    plt.grid()
    plt.savefig(os.path.join(output_folder, "speedup_plot.pdf"))  # 保存为 PDF
    plt.show()


# 运行代码
folder_path = "evaluation/"  # 你的CSV文件夹路径
output_folder = "evaluation/plots/"  # 存储图表的文件夹
df = extract_final_rows(folder_path)
plot_results(df, output_folder)
