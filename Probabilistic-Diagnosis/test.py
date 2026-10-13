import re


def convert_txt_to_csv(input_file, output_file):
    try:
        # 读取txt文件
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()

        # 创建CSV header
        header = "n,k,p,beta,gamma"

        # 处理每一行
        result = []
        # 将文本分割成行
        lines = text.strip().split('\n')

        for line in lines:
            # 使用正则表达式提取数值
            matches = re.findall(r'n = ([\d.]+) ,  k = ([\d.]+) ,  p = ([\d.]+) ,  beta = ([\d.]+) ,  gamma = ([\d.]+)',
                                 line)
            if matches:
                # 将匹配到的数值组合成CSV行
                result.append(','.join(matches[0]))

        # 写入CSV文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(header + '\n' + '\n'.join(result))

        print(f"转换完成！输出文件：{output_file}")

    except FileNotFoundError:
        print("错误：找不到输入文件")
    except Exception as e:
        print(f"发生错误：{str(e)}")


# 使用示例
input_file = "parameters-paper/n=7.txt"  # 输入的txt文件名
output_file = "parameters-paper/n=7.csv"  # 输出的csv文件名

convert_txt_to_csv(input_file, output_file)