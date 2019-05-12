# -*-coding:utf-8 -*-
"""
dijkstra寻找最短路径
author @boole
date 2019-05-12
"""

# 表示无穷大
INF_VAL = 9999999


class DijkstraPath(object):
    def __init__(self, node, node_map):
        self.node = node
        self.node_map = node_map
        self.node_length = len(node_map)
        self.node_col = []
        self.node_dis = {}

    def dijkstra(self, from_node):
        """
        dijkstra 算法
        :param from_node:
        :return:
        """
        self.node_col.append(from_node)
        for i in range(self.node_length):
            self.node_dis[i] = [INF_VAL, -1]
        self.node_dis[from_node] = [0, -1]
        for i, w in enumerate(self.node_map[from_node]):
            if w:
                self.node_dis[i] = [w, from_node]

        while len(self.node_col) < self.node_length - 1:
            min_key = -1
            min_val = INF_VAL
            for k, v in self.node_dis.items():
                if v[0] < min_val and k not in self.node_col:
                    min_key = k
                    min_val = v[0]
            if min_key != -1:
                self.node_col.append(min_key)

            for i, w in enumerate(self.node_map[min_key]):
                if w > 0 and self.node_dis[i][0] > w + min_val:
                    self.node_dis[i][0] = w + min_val
                    self.node_dis[i][1] = min_key

    def get_path(self, from_node, to_node):
        """
        获取路径
        :param from_node:
        :param to_node:
        :return:
        """
        from_idx = self.node.index(from_node)
        to_idx = self.node.index(to_node)
        self.dijkstra(from_idx)
        path_list = list()
        path_list.append((self.node[to_idx], self.node_dis[to_idx][0]))
        while self.node_dis[to_idx][1] != -1:
            to_idx = self.node_dis[to_idx][1]
            path_list.append((self.node[to_idx], self.node_dis[to_idx][0]))
        path_list.reverse()
        return path_list


def set_node_map(node_list):
    """
    生成关联矩阵
    :param node_list:
    :return:
    """
    node = set()
    for s, e, w in node_list:
        node.add(s)
        node.add(e)
    node = list(node)
    node_map = [[0 for n in range(len(node))] for n in range(len(node))]
    for s, e, w in node_list:
        x = node.index(s)
        y = node.index(e)
        node_map[x][y] = node_map[y][x] = w
    return node, node_map


if __name__ == "__main__":
    node_list_temp = [('A', 'B', 1),
                      ('A', 'C', 2),
                      ('C', 'D', 3),
                      ('D', 'E', 4),
                      ('A', 'F', 3),
                      ('F', 'G', 7),
                      ('C', 'F', 8),
                      ('B', 'G', 9),
                      ('B', 'E', 10)]
    # 创建关联矩阵
    node_temp, node_map_temp = set_node_map(node_list_temp)
    # 计算距离
    f_node = 'A'
    t_node = 'E'
    djs = DijkstraPath(node_temp, node_map_temp)
    path = djs.get_path(f_node, t_node)
    print(path)
    # [('A', 0), ('C', 2), ('D', 5), ('E', 9)]

