import csv

from AugmentedKAryNCube import evaulation_test


def augmentedKAryNCube_diagnosis_1():
    # 打开 CSV 文件
    with open('parameters/p.csv', mode='r') as file:
        # 创建 CSV 读取器
        reader = csv.DictReader(file)

        # 逐行读取 CSV 文件
        for row in reader:
            # 提取参数
            n = int(row['n'])
            k = int(row['k'])
            p = float(row['p'])
            beta = float(row['beta'])
            gamma = float(row['gamma'])

            # 调用 evaluation_rest 函数
            evaulation_test(n, k, p, beta, gamma)

def augmentedKAryNCube_diagnosis_2():
    # 打开 CSV 文件
    with open('parameters/beta.csv', mode='r') as file:
        # 创建 CSV 读取器
        reader = csv.DictReader(file)

        # 逐行读取 CSV 文件
        for row in reader:
            # 提取参数
            n = int(row['n'])
            k = int(row['k'])
            p = float(row['p'])
            beta = float(row['beta'])
            gamma = float(row['gamma'])

            # 调用 evaluation_rest 函数
            evaulation_test(n, k, p, beta, gamma)

def augmentedKAryNCube_diagnosis_3():
    # 打开 CSV 文件
    with open('parameters/gamma.csv', mode='r') as file:
        # 创建 CSV 读取器
        reader = csv.DictReader(file)

        # 逐行读取 CSV 文件
        for row in reader:
            # 提取参数
            n = int(row['n'])
            k = int(row['k'])
            p = float(row['p'])
            beta = float(row['beta'])
            gamma = float(row['gamma'])

            # 调用 evaluation_rest 函数
            evaulation_test(n, k, p, beta, gamma)


if __name__ == "__main__":
    augmentedKAryNCube_diagnosis_2()