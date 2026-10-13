import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline


def connect_points_with_rules(x_data, y_data, n_points=300):
    """
    根据规则连接点：
    1. 如果两个点都是100%，直接用直线连接
    2. 其他情况使用平滑曲线
    """
    x_data = np.array(x_data)
    y_data = np.array(y_data)

    # 存储所有段的x和y坐标
    X_segments = []
    Y_segments = []

    for i in range(len(x_data) - 1):
        start_x = x_data[i]
        end_x = x_data[i + 1]
        start_y = y_data[i]
        end_y = y_data[i + 1]

        # 如果两个点都是100%，使用直线连接
        if abs(start_y - 1.0) < 1e-6 and abs(end_y - 1.0) < 1e-6:
            x_segment = np.array([start_x, end_x])
            y_segment = np.array([start_y, end_y])
        else:
            # 其他情况使用平滑曲线
            x_segment = np.linspace(start_x, end_x, int(n_points / len(x_data)))

            # 只有两个点时使用线性插值
            if i == 0 or i == len(x_data) - 2:
                y_segment = np.interp(x_segment, [start_x, end_x], [start_y, end_y])
            else:
                # 使用周围的点来创建更平滑的曲线
                x_local = x_data[max(0, i - 1):min(len(x_data), i + 3)]
                y_local = y_data[max(0, i - 1):min(len(x_data), i + 3)]

                if len(x_local) > 2:
                    spl = make_interp_spline(x_local, y_local, k=min(3, len(x_local) - 1))
                    y_segment = spl(x_segment)

                    # 确保不会超出范围
                    y_segment = np.clip(y_segment, min(start_y, end_y), max(start_y, end_y))
                else:
                    y_segment = np.interp(x_segment, [start_x, end_x], [start_y, end_y])

        X_segments.append(x_segment)
        Y_segments.append(y_segment)

    return np.concatenate(X_segments), np.concatenate(Y_segments)


def process_csv_files(folder_path):
    # 参数列表（修正格式）
    beta_values = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.5]
    fixed_p = 0.9
    fixed_gamma = 0.9

    # 存储结果的字典
    results = {
        'beta_values': [],
        'filenames': [],
        'fault_free_correct_ratio': [],
        'faulty_correct_ratio': []
    }

    # 固定的其他参数
    n = None
    k = None

    # 遍历beta值
    for beta in beta_values:
        # 构建文件名模式
        filename_pattern = f'diagnosis_results_n6_k3_p{fixed_p}_beta{beta}_gamma{fixed_gamma}.csv'

        # 查找匹配的文件
        matching_files = [f for f in os.listdir(folder_path) if f == filename_pattern]

        if matching_files:
            file_path = os.path.join(folder_path, matching_files[0])
            df = pd.read_csv(file_path)

            # 提取最后一行的数据
            last_row = df.iloc[-1]

            # 打印当前文件的数据
            print(f"\nFile: {matching_files[0]}")
            print(f"beta = {beta:.2f}")
            print(f"Fault-free Correct Ratio: {last_row['fault_free_correct_ratio']:.4f}")
            print(f"Faulty Correct Ratio: {last_row['faulty_correct_ratio']:.4f}")

            # 记录结果
            results['beta_values'].append(beta)
            results['filenames'].append(matching_files[0])
            results['fault_free_correct_ratio'].append(last_row['fault_free_correct_ratio'])
            results['faulty_correct_ratio'].append(last_row['faulty_correct_ratio'])

            # 记录固定参数（假设所有文件的这些参数都相同）
            if n is None:
                n = 6
                k = 3

    # 对两条线分别进行处理
    X_smooth_ff, Y_smooth_ff = connect_points_with_rules(
        results['beta_values'],
        results['fault_free_correct_ratio']
    )

    X_smooth_f, Y_smooth_f = connect_points_with_rules(
        results['beta_values'],
        results['faulty_correct_ratio']
    )

    # 绘制折线图
    plt.figure(figsize=(6, 4))

    # 绘制处理后的曲线和原始数据点
    plt.plot(X_smooth_ff, Y_smooth_ff, '-', linewidth=1.5, label='Fault-free Correct Ratio')
    plt.plot(X_smooth_f, Y_smooth_f, '-', linewidth=1.5, label='Faulty Correct Ratio')
    plt.plot(results['beta_values'], results['fault_free_correct_ratio'], 'o',
             color='blue', markersize=4)
    plt.plot(results['beta_values'], results['faulty_correct_ratio'], 'o',
             color='orange', markersize=4)

    plt.title(f'Diagnosis Performance (n={n}, k={k}, p={fixed_p}, γ={fixed_gamma})', fontsize=10)
    plt.xlabel('β', fontsize=9)
    plt.ylabel('Correct Ratio', fontsize=9)
    plt.legend(fontsize=8)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.tight_layout(pad=1.0)

    # 获取y轴的范围
    y_min, y_max = plt.ylim()
    y_range = y_max - y_min

    # 添加数据点的具体值，使用交错的垂直偏移
    for i, beta in enumerate(results['beta_values']):
        # 为fault-free的标注添加向上的偏移
        offset_up = y_range * 0.02
        if i % 2 == 0:
            offset_up = y_range * 0.04

        # 为faulty的标注添加向下的偏移
        offset_down = y_range * 0.02
        if i % 2 == 1:
            offset_down = y_range * 0.04

        # 添加fault-free的标注
        plt.text(beta, results['fault_free_correct_ratio'][i] + offset_up,
                 f'{results["fault_free_correct_ratio"][i]:.2f}',
                 verticalalignment='bottom', fontsize=7, ha='center')

        # 添加faulty的标注
        plt.text(beta, results['faulty_correct_ratio'][i] - offset_down,
                 f'{results["faulty_correct_ratio"][i]:.2f}',
                 verticalalignment='top', fontsize=7, ha='center')

    # 自定义x轴刻度
    plt.xticks(beta_values, [f'{beta:.2f}' for beta in beta_values], fontsize=8, rotation=45)
    plt.yticks(fontsize=8)

    # 调整x轴范围，减小边距使图形更紧凑
    plt.xlim(-0.02, 0.52)

    # 稍微扩大y轴范围以容纳标注
    current_ymin, current_ymax = plt.ylim()
    plt.ylim(current_ymin - y_range * 0.05, current_ymax + y_range * 0.05)

    # 先保存为PDF，再显示图形
    plt.savefig('diagnosis_performance_beta_n_6.pdf', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

    # 打印汇总数据
    print("\nSummary of Results:")
    print("beta_values:", [f"{beta:.2f}" for beta in results['beta_values']])
    print("Fault-free correct ratios:", [f"{ratio:.4f}" for ratio in results['fault_free_correct_ratio']])
    print("Faulty correct ratios:", [f"{ratio:.4f}" for ratio in results['faulty_correct_ratio']])

    return results


# 使用示例
folder_path = './evaluation/beta'
results = process_csv_files(folder_path)