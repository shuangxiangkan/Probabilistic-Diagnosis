import os
import pandas as pd
import matplotlib.pyplot as plt


def process_csv_files(folder_path):
    # 参数列表
    gamma_values = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
    fixed_p = 0.9

    # 存储结果的字典
    results = {
        'gamma_values': [],
        'filenames': [],
        'fault_free_correct_ratio': [],
        'faulty_correct_ratio': []
    }

    # 固定的其他参数
    n = None
    k = None
    beta = None

    # 遍历gamma值
    for gamma in gamma_values:
        # 构建文件名模式
        filename_pattern = f'diagnosis_results_n5_k3_p{fixed_p}_beta0.1_gamma{gamma}.csv'

        # 查找匹配的文件
        matching_files = [f for f in os.listdir(folder_path) if f == filename_pattern]

        if matching_files:
            file_path = os.path.join(folder_path, matching_files[0])
            df = pd.read_csv(file_path)

            # 提取最后一行的数据
            last_row = df.iloc[-1]

            # 打印当前文件的数据
            print(f"\nFile: {matching_files[0]}")
            print(f"gamma = {gamma:.2f}")
            print(f"Fault-free Correct Ratio: {last_row['fault_free_correct_ratio']:.4f}")
            print(f"Faulty Correct Ratio: {last_row['faulty_correct_ratio']:.4f}")

            # 记录结果
            results['gamma_values'].append(gamma)
            results['filenames'].append(matching_files[0])
            results['fault_free_correct_ratio'].append(last_row['fault_free_correct_ratio'])
            results['faulty_correct_ratio'].append(last_row['faulty_correct_ratio'])

            # 记录固定参数（假设所有文件的这些参数都相同）
            if n is None:
                n = 5
                k = 3
                beta = 0.1

    # 绘制折线图
    plt.figure(figsize=(6, 4))  # 稍微加宽以适应更多数据点
    plt.plot(results['gamma_values'], results['fault_free_correct_ratio'], marker='o', label='Fault-free Correct Ratio')
    plt.plot(results['gamma_values'], results['faulty_correct_ratio'], marker='o', label='Faulty Correct Ratio')

    plt.title(f'Diagnosis Performance (n={n}, k={k}, p={fixed_p}, beta={beta})', fontsize=10)
    plt.xlabel('γ', fontsize=9)
    plt.ylabel('Correct Ratio', fontsize=9)
    plt.legend(fontsize=8)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.tight_layout(pad=1.0)

    # 获取y轴的范围
    y_min, y_max = plt.ylim()
    y_range = y_max - y_min

    # 添加数据点的具体值，使用交错的垂直偏移
    for i, gamma in enumerate(results['gamma_values']):
        # 为fault-free的标注添加向上的偏移
        offset_up = y_range * 0.02  # 上方标注的偏移量
        if i % 2 == 0:
            offset_up = y_range * 0.04  # 偶数索引的点使用更大的偏移

        # 为faulty的标注添加向下的偏移
        offset_down = y_range * 0.02  # 下方标注的偏移量
        if i % 2 == 1:
            offset_down = y_range * 0.04  # 奇数索引的点使用更大的偏移

        # 添加fault-free的标注
        plt.text(gamma, results['fault_free_correct_ratio'][i] + offset_up,
                 f'{results["fault_free_correct_ratio"][i]:.2f}',
                 verticalalignment='bottom', fontsize=7, ha='center')

        # 添加faulty的标注
        plt.text(gamma, results['faulty_correct_ratio'][i] - offset_down,
                 f'{results["faulty_correct_ratio"][i]:.2f}',
                 verticalalignment='top', fontsize=7, ha='center')

    # 自定义x轴刻度
    plt.xticks(gamma_values, [f'{gamma:.2f}' for gamma in gamma_values], fontsize=8, rotation=45)
    plt.yticks(fontsize=8)

    # 调整x轴范围，减小边距使图形更紧凑
    plt.xlim(0.48, 1.02)

    # 稍微扩大y轴范围以容纳标注
    current_ymin, current_ymax = plt.ylim()
    plt.ylim(current_ymin - y_range * 0.05, current_ymax + y_range * 0.05)

    # 先保存为PDF，再显示图形
    plt.savefig('diagnosis_performance_gamma_n_5.pdf', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

    # 打印汇总数据
    print("\nSummary of Results:")
    print("gamma_values:", [f"{gamma:.2f}" for gamma in results['gamma_values']])
    print("Fault-free correct ratios:", [f"{ratio:.4f}" for ratio in results['fault_free_correct_ratio']])
    print("Faulty correct ratios:", [f"{ratio:.4f}" for ratio in results['faulty_correct_ratio']])

    return results


# 使用示例
folder_path = './evaluation/gamma'
results = process_csv_files(folder_path)