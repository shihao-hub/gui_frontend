### 1.0.0
```python
from typing import List


def _head_adjust(seq: List[int], length: int, k: int):
    """
    :param k: 需要调整的节点下标
    """
    i = k * 2
    value = seq[k]
    while i < length:
        if i + 1 < length and seq[i] < seq[i + 1]:
            i += 1
        if value >= seq[i]:
            break
        seq[k] = seq[i]
        k = i
        i *= 2
    seq[k] = value


def build_max_heap(seq: List[int], length: int):
    for i in range(length // 2, 0, -1):
        _head_adjust(seq, length, i)


def heap_sort(seq: List[int]):
    """
    graph TD
    A[构建大顶堆] --> B[交换堆顶和最后一个元素]
    B --> C[调整堆（注意当前堆长度减 1）]
    C --> |循环直到堆长度为 1| B
    """

    length = len(seq)
    build_max_heap(seq, length)
    print(seq)
    for i in range(length, 1, -1):
        seq[1], seq[i - 1] = seq[i - 1], seq[1]
        _head_adjust(seq, i - 1, 1)


def main():
    array = [None, 1, 2, 4, 6, 8, 5, 9]
    heap_sort(array)
    print(array)


if __name__ == '__main__':
    main()

```
