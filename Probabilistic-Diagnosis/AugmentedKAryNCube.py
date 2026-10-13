import multiprocessing as mp
import os
import time
from itertools import product
import random
import csv


class AugmentedKAryNCube:
    def __init__(self, n, k, p, beta, gamma):
        """
        初始化 Augmented k-ary n-cube

        :param n: 维度
        :param k: 基数
        :param p: 节点无故障的概率
        :param beta: 故障节点测试故障节点结果为 0 的概率
        :param gamma: 无故障节点测试故障节点结果为 0 的概率
        """
        self.n = n
        self.k = k
        self.p = p
        self.beta = beta
        self.gamma = gamma
        self.nodes = list(product(range(k), repeat=n))  # 所有节点
        self.edges = self._generate_edges()  # 所有边
        self.node_states = {}  # 节点状态：fault-free 或 faulty
        self.edge_states = {}  # 边的权重：存储双向测试结果

        # 初始化节点状态和边状态
        self.set_node_states()
        self.set_edge_states()

    def _generate_edges(self):
        """
        生成所有边
        """
        edges = set()
        for node in self.nodes:
            for i in range(self.n):
                # (i, ±1)-边
                neighbor_plus = self._get_neighbor(node, i, +1)
                neighbor_minus = self._get_neighbor(node, i, -1)
                if neighbor_plus:
                    edges.add(tuple(sorted([node, neighbor_plus])))
                if neighbor_minus:
                    edges.add(tuple(sorted([node, neighbor_minus])))
            for i in range(1, self.n):
                # (≤i, ±1)-边
                neighbor_plus = self._get_cascading_neighbor(node, i, +1)
                neighbor_minus = self._get_cascading_neighbor(node, i, -1)
                if neighbor_plus:
                    edges.add(tuple(sorted([node, neighbor_plus])))
                if neighbor_minus:
                    edges.add(tuple(sorted([node, neighbor_minus])))
        return list(edges)

    def _get_neighbor(self, node, i, direction):
        """
        获取 (i, ±1) 邻居
        """
        new_node = list(node)
        new_node[i] = (new_node[i] + direction) % self.k
        return tuple(new_node)

    def _get_cascading_neighbor(self, node, i, direction):
        """
        获取 (≤i, ±1) 邻居
        """
        new_node = list(node)
        for j in range(i + 1):
            new_node[j] = (new_node[j] + direction) % self.k
        return tuple(new_node)

    def get_neighbors(self, node):
        """
        获取节点的所有邻居节点

        :param node: 当前节点
        :return: 邻居节点列表
        """
        neighbors = []
        # 计算 (i, ±1) 邻居
        for i in range(self.n):
            neighbor_plus = self._get_neighbor(node, i, +1)
            neighbor_minus = self._get_neighbor(node, i, -1)
            neighbors.append(neighbor_plus)
            neighbors.append(neighbor_minus)
        # 计算 (≤i, ±1) 邻居
        for i in range(1, self.n):
            neighbor_plus = self._get_cascading_neighbor(node, i, +1)
            neighbor_minus = self._get_cascading_neighbor(node, i, -1)
            neighbors.append(neighbor_plus)
            neighbors.append(neighbor_minus)
        # 去重并返回
        return list(set(neighbors))

    def set_node_states(self):
        """
        设置节点状态
        """
        for node in self.nodes:
            if random.random() < self.p:
                self.node_states[node] = "fault-free"
            else:
                self.node_states[node] = "faulty"

    def set_edge_states(self):
        """
        设置边的权重（双向测试结果）
        """
        for edge in self.edges:
            a, b = edge
            # 计算 a 测试 b 的结果
            a_to_b = self._calculate_sigma(a, b)
            # 计算 b 测试 a 的结果
            b_to_a = self._calculate_sigma(b, a)
            # 存储双向测试结果
            self.edge_states[edge] = {
                'a_to_b': a_to_b,
                'b_to_a': b_to_a
            }

    def _calculate_sigma(self, tester, tested):
        """
        计算 tester 测试 tested 的结果
        """
        if self.node_states[tester] == "fault-free" and self.node_states[tested] == "fault-free":
            return 0
        elif ((self.node_states[tester] == "fault-free" and self.node_states[tested] == "faulty") or
              (self.node_states[tester] == "faulty" and self.node_states[tested] == "fault-free")):
            a_test_b = 1 if random.random() < self.gamma else 0
            b_test_a = 1 if random.random() < self.gamma else 0
            return 0 if a_test_b == 0 and b_test_a == 0 else 1
        elif self.node_states[tester] == "faulty" and self.node_states[tested] == "faulty":
            a_test_b = 0 if random.random() < self.beta else 1
            b_test_a = 0 if random.random() < self.beta else 1
            return 0 if a_test_b == 0 and b_test_a == 0 else 1
        else:
            return 1

    def get_edge_weight(self, a, b, direction):
        """
        获取边的权重（0 或 1）

        :param a: 节点 a
        :param b: 节点 b
        :param direction: 测试方向，'a_to_b' 或 'b_to_a'
        :return: 测试结果（0 或 1）
        """
        edge = tuple(sorted([a, b]))
        if edge in self.edge_states:
            return self.edge_states[edge].get(direction, 1)  # 默认返回 1（如果方向不存在）
        return 1  # 默认返回 1（如果边不存在）


class DiagnosisBase:

    def __init__(self, aqncube):
        """
        初始化诊断基类

        :param aqncube: AugmentedKAryNCube 实例
        """
        self.aqncube = aqncube

    def local_fault_diagnosis(self):
        """
        局部故障诊断算法（需子类实现）
        """
        raise NotImplementedError


class SequentialDiagnosis(DiagnosisBase):

    def local_fault_diagnosis(self):
        """
        顺序执行局部故障诊断
        """
        # time.sleep(1)
        T = set()  # 无故障节点集合
        F = set()  # 故障节点集合

        for node in self.aqncube.nodes:
            if node in F or node in T:
                continue  # 如果节点已经分类，跳过

            # 为了减轻进程创建和销毁的开销对于时间故障诊断的影响，对于每一个进行诊断的node都增加0.001s的时间
            time.sleep(0.001)

            node_neighbors = self.aqncube.get_neighbors(node)
            # 使用双向测试结果判断匹配邻居
            matching_neighbors = [
                n for n in node_neighbors
                if self.aqncube.get_edge_weight(node, n, 'a_to_b') == 0 and self.aqncube.get_edge_weight(n, node, 'b_to_a') == 0
            ]

            if len(matching_neighbors) >= 3:
                T.add(node)
                T.update(matching_neighbors)
            elif len(matching_neighbors) == 2:
                a1, a2 = matching_neighbors
                # 分别计算 a1 和 a2 的 matching_neighbors
                # 计算 a1 的 matching_neighbors
                a1_matching = []
                # 获取 a1 的所有邻居节点
                a1_neighbors = self.aqncube.get_neighbors(a1)
                for n in a1_neighbors:
                    # 排除当前节点 node
                    if n == node or n == a2:
                        continue
                    # 检查 σ(a1, n) 是否为 0
                    if self.aqncube.get_edge_weight(a1, n, 'a_to_b') == 0 and self.aqncube.get_edge_weight(n, a1, 'b_to_a') == 0:
                        a1_matching.append(n)

                # 计算 a2 的 matching_neighbors
                a2_matching = []
                # 获取 a2 的所有邻居节点
                a2_neighbors = self.aqncube.get_neighbors(a2)
                for n in a2_neighbors:
                    # 排除当前节点 node
                    if n == node or n == a1:
                        continue
                    # 检查 σ(a2, n) 是否为 0
                    if self.aqncube.get_edge_weight(a2, n, 'a_to_b') == 0 and self.aqncube.get_edge_weight(n, a2, 'b_to_a') == 0:
                        a2_matching.append(n)

                # 如果 a1 或 a2 有至少一个 matching_neighbor，则将 node、a1、a2 分类为无故障
                if len(a1_matching) >= 1:
                    T.add(node)
                    T.add(a1)
                    T.add(a2)
                    T.update(a1_matching)
                elif len(a2_matching) >= 1:
                    T.add(node)
                    T.add(a1)
                    T.add(a2)
                    T.update(a2_matching)
                else:
                    # 否则，将 node、a1、a2 分类为故障
                    F.add(node)
                    F.add(a1)
                    F.add(a2)

            elif len(matching_neighbors) == 1:
                a1 = matching_neighbors[0]
                # 计算 a1 的 matching_neighbors（排除当前节点 node 和 a1）
                a1_matching = []
                a1_neighbors = self.aqncube.get_neighbors(a1)

                for n in a1_neighbors:
                    # 排除当前节点 node 和 a1
                    if n == node or n == a1:
                        continue
                    # 检查 σ(a1, n) 是否为 0
                    if self.aqncube.get_edge_weight(a1, n, 'a_to_b') == 0 and self.aqncube.get_edge_weight(n, a1, 'b_to_a') == 0:
                        a1_matching.append(n)

                if len(a1_matching) >= 2:
                    # 如果 a1 有至少两个 matching_neighbors，则将 a1 及其 matching_neighbors 分类为无故障
                    T.add(node)
                    T.add(a1)
                    T.update(a1_matching)
                elif len(a1_matching) == 1:
                    b1 = a1_matching[0]
                    # 计算 b1 的 matching_neighbors（排除 a1 和 b1）
                    b1_matching = []
                    b1_neighbors = self.aqncube.get_neighbors(b1)
                    for n in b1_neighbors:
                        # 排除 a1 和 b1
                        if n == node or n == a1 or n == b1:
                            continue
                        # 检查 σ(b1, n) 是否为 0
                        if self.aqncube.get_edge_weight(b1, n, 'a_to_b') == 0 and self.aqncube.get_edge_weight(n, b1, 'b_to_a') == 0:
                            b1_matching.append(n)
                    if len(b1_matching) >= 1:
                        # 如果 b1 有至少一个 matching_neighbor，则将 a1、b1 分类为无故障
                        T.add(node)
                        T.add(a1)
                        T.add(b1)
                        T.update(b1_matching)
                    else:
                        # 否则，将 node、a1、b1 分类为故障
                        F.add(node)
                        F.add(a1)
                        F.add(b1)
                else:
                    # 如果 a1 没有 matching_neighbors，则将 node 和 a1 分类为故障
                    F.add(node)
                    F.add(a1)
            else:
                F.add(node)

        return T, F


class ParallelDiagnosis(DiagnosisBase):

    def __init__(self, aqncube):
        super().__init__(aqncube)
        self.num_cpus = mp.cpu_count()


    def local_fault_diagnosis(self):
        """
        并行执行局部故障诊断，同时统计真正的并行计算时间
        """
        subgraphs = self._decompose_aqn_k()

        start_time = time.time()
        with mp.Pool(processes=self.num_cpus) as pool:
            # 返回值为 (诊断结果, 子任务开始时间, 子任务结束时间)
            results = pool.map(self._diagnose_subgraph, subgraphs)

        parallel_process_time = time.time() - start_time
        # print(f"并行诊断总执行时间（包括进程启动和通信）: {parallel_time:.4f} 秒")

        # 合并结果，同时统计并行计算时间区间
        T = set()
        F = set()
        earliest_start = float('inf')
        latest_end = float('-inf')
        for (t, f), task_start, task_end in results:
            T.update(t)
            F.update(f)
            earliest_start = min(earliest_start, task_start)
            latest_end = max(latest_end, task_end)

        # 计算真正的并行计算时间
        parallel_compute_time = latest_end - earliest_start
        # print(f"并行总计算时间（任务实际运行时间）: {parallel_compute_time:.4f} 秒")
        # print(f"并行额外开销（进程启动和通信）: {parallel_time - parallel_compute_time:.4f} 秒")

        return T, F, parallel_compute_time, parallel_process_time

    def _decompose_aqn_k(self):
        """
        将 AQn,k 分解为 k 个 AQn-1,k，并保留子图之间的边
        """
        subgraphs = []
        for i in range(self.aqncube.k):
            # 筛选第 n 维坐标为 i 的节点
            subgraph_nodes = [node for node in self.aqncube.nodes if node[-1] == i]

            # 创建子图
            subgraph = AugmentedKAryNCube(self.aqncube.n - 1, self.aqncube.k, self.aqncube.p, self.aqncube.beta,
                                          self.aqncube.gamma)
            subgraph.nodes = subgraph_nodes

            # 筛选子图内部的边
            internal_edges = [
                edge for edge in self.aqncube.edges
                if edge[0] in subgraph_nodes and edge[1] in subgraph_nodes
            ]

            # 筛选跨子图的边（至少一个端点在当前子图中）
            cross_edges = [
                edge for edge in self.aqncube.edges
                if (edge[0] in subgraph_nodes and edge[1] not in subgraph_nodes) or
                   (edge[1] in subgraph_nodes and edge[0] not in subgraph_nodes)
            ]

            # 将内部边和跨子图的边合并
            subgraph.edges = internal_edges + cross_edges

            # 设置子图的节点状态
            subgraph.node_states = {
                node: self.aqncube.node_states[node] for node in subgraph_nodes
            }

            # 设置子图的边状态（包括内部边和跨子图的边）
            subgraph.edge_states = {
                edge: self.aqncube.edge_states[edge] for edge in subgraph.edges
            }

            subgraphs.append(subgraph)

        return subgraphs

    def _diagnose_subgraph(self, subgraph):
        """
        对子图进行局部故障诊断，记录子任务的时间区间
        """
        start_time = time.time()  # 子任务开始时间
        diagnosis = SequentialDiagnosis(subgraph)
        result = diagnosis.local_fault_diagnosis()
        end_time = time.time()  # 子任务结束时间

        # compute_time = end_time - start_time
        # print(f"- Process ID: {os.getpid()} | 计算时间: {compute_time:.4f} 秒")
        return result, start_time, end_time


def diagnose(n, k, p, beta, gamma):
    # 创建一个 Augmented k-ary n-cube
    aqncube = AugmentedKAryNCube(n, k, p, beta, gamma)

    # 测试顺序诊断
    start_time = time.time()
    seq_diagnosis = SequentialDiagnosis(aqncube)
    T_seq, F_seq = seq_diagnosis.local_fault_diagnosis()
    seq_time = time.time() - start_time

    # 检查故障顶点和无故障顶点是否被正确分类
    original_fault_free = set(node for node, state in aqncube.node_states.items() if state == "fault-free")
    original_faulty = set(node for node, state in aqncube.node_states.items() if state == "faulty")

    # 正确分类的无故障节点
    correctly_diagnosed_fault_free = T_seq.intersection(original_fault_free)
    # 正确分类的故障节点
    correctly_diagnosed_faulty = F_seq.intersection(original_faulty)

    # 计算比例
    total_fault_free = len(original_fault_free)
    total_faulty = len(original_faulty)

    # 无故障节点的正确分类比例
    fault_free_correct_ratio = len(correctly_diagnosed_fault_free) / total_fault_free if total_fault_free > 0 else 1.0
    # 故障节点的正确分类比例
    faulty_correct_ratio = len(correctly_diagnosed_faulty) / total_faulty if total_faulty > 0 else 1.0

    # 测试并行诊断
    start_time = time.time()
    parallel_diagnosis = ParallelDiagnosis(aqncube)
    T_par, F_par, parallel_compute_time, parallel_process_time = parallel_diagnosis.local_fault_diagnosis()
    parallel_all_time = time.time() - start_time

    # # 比较结果
    # results_consistent = T_seq == T_par and F_seq == F_par

    return (seq_time, fault_free_correct_ratio, faulty_correct_ratio, parallel_process_time,
            parallel_compute_time, parallel_all_time)


def save_results_to_csv(filename, n, k, p, beta, gamma, all_results):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # 写入表头
        writer.writerow([
            "n", "k", "p", "beta", "gamma",
            "seq_time", "fault_free_correct_ratio",
            "faulty_correct_ratio", "parallel_process_time",
            "parallel_compute_time", "parallel_all_time"
        ])
        # 写入每次运行的数据
        for results in all_results:
            writer.writerow([
                n, k, p, beta, gamma,
                f"{float(results[0]):.4f}", f"{float(results[1]) * 100:.4f}", f"{float(results[2]) * 100:.4f}",
                f"{float(results[3]):.4f}", f"{float(results[4]):.4f}", f"{float(results[5]):.4f}"
            ])

def evaulation_test(n, k, p, beta, gamma):
    all_results = []
    # 运行10次
    for _ in range(10):
        results = diagnose(n, k, p, beta, gamma)
        all_results.append(results)

    # 格式化文件名
    filename = f"evaluation/beta/diagnosis_results_n{n}_k{k}_p{p}_beta{beta}_gamma{gamma}.csv"
    # 保存所有结果到CSV文件
    save_results_to_csv(filename, n, k, p, beta, gamma, all_results)

    # 打印保存完成信息
    print(f"Results saved to {filename} for n={n}, k={k}, p={p}, beta={beta}, gamma={gamma}")

if __name__ == "__main__":
    evaulation_test(7, 3, 0.9, 0.1, 0.9)