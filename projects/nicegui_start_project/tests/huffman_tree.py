import heapq
from abc import ABC, abstractmethod

from typing import Set, List, Iterable


class Function(ABC):
    def call(self, *args, **kwargs): ...


class HuffmanTreeNode:
    def __init__(self, value: int, left: "HuffmanTreeNode" = None, right: "HuffmanTreeNode" = None, name: str = "", ):
        self.value: int = value
        self.left: HuffmanTreeNode = left
        self.right: HuffmanTreeNode = right
        self.name: str = name

    def __lt__(self, other):
        return self.value < other.value

    def __str__(self):
        return f"Node({self.value}, {self.left}, {self.right})"


class _Nodes:
    def __init__(self, nodes: Iterable[HuffmanTreeNode]):
        self._nodes: List[HuffmanTreeNode] = []
        for e in nodes:
            heapq.heappush(self._nodes, e)

    def add(self, node: HuffmanTreeNode):
        heapq.heappush(self._nodes, node)

    def remove(self):
        return heapq.heappop(self._nodes)

    def __len__(self):
        return len(self._nodes)


class CreateHuffmanTree(Function):
    def __init__(self, nodes: Set[HuffmanTreeNode]):
        self.nodes: _Nodes = _Nodes(nodes)

    def _choose_target_node(self):
        """选择值最小的那个节点"""
        return self.nodes.remove()

    def call(self) -> HuffmanTreeNode:
        this = self

        n = len(self.nodes) - 1
        for i in range(n):
            left = self._choose_target_node()
            right = self._choose_target_node()
            node = HuffmanTreeNode(left.value + right.value, left, right)
            self.nodes.add(node)
        assert len(self.nodes) == 1
        return self.nodes.remove()


def test():
    huffman_tree = CreateHuffmanTree({
        HuffmanTreeNode(1),
        HuffmanTreeNode(2),
        HuffmanTreeNode(2),
        HuffmanTreeNode(3),
        HuffmanTreeNode(7),
    }).call()
    print(huffman_tree)


if __name__ == '__main__':
    test()
