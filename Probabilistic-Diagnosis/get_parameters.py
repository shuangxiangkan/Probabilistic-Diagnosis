import csv

def get_p():
    # 固定参数
    n = 5
    k = 3
    beta = 0.1
    gamma_value = 0.9

    # p的取值范围
    p_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    # 创建CSV文件
    filename = 'parameters/p.csv'
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        # 写入表头
        csvwriter.writerow(['n', 'k', 'p', 'beta', 'gamma'])

        # 遍历p值并写入数据
        for p in p_values:
            csvwriter.writerow([n, k, p, beta, gamma_value])

    print(f"CSV文件 {filename} 已生成")

def get_gamma():
    # n和beta的取值范围
    n_values = [5, 6, 7]
    gamma_values = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]

    # 其他固定参数
    k = 3
    p = 0.90
    beta_value = 0.10

    # 创建CSV文件
    filename = 'parameters/gamma.csv'
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        # 写入表头
        csvwriter.writerow(['n', 'k', 'p', 'beta', 'gamma'])

        # 遍历n值和beta值并写入数据
        for n in n_values:
            for gamma in gamma_values:
                csvwriter.writerow([n, k, p, beta_value, gamma])

    print(f"CSV文件 {filename} 已生成")

def get_beta():
    n_values = [5, 6, 7]
    beta_values = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.5]

    # 其他固定参数
    k = 3
    p = 0.9
    gamma_value = 0.9

    # 创建CSV文件
    filename = 'parameters/beta.csv'
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        # 写入表头
        csvwriter.writerow(['n', 'k', 'p', 'beta', 'gamma'])

        # 遍历n值和beta值并写入数据
        for n in n_values:
            for beta in beta_values:
                csvwriter.writerow([n, k, p, beta, gamma_value])

    print(f"CSV文件 {filename} 已生成")

if __name__ == "__main__":
    get_beta()
