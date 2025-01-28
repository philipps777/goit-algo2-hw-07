import timeit
from functools import lru_cache
import matplotlib.pyplot as plt



@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)



class SplayNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None



class SplayTree:
    def __init__(self):
        self.root = None

    def _zig(self, node):
        """Right rotation"""
        left = node.left
        node.left = left.right
        left.right = node
        return left

    def _zag(self, node):
        """Left rotation"""
        right = node.right
        node.right = right.left
        right.left = node
        return right

    def _splay(self, node, key):
        if not node or node.key == key:
            return node

        if key < node.key:
            if not node.left:
                return node
            if key < node.left.key:
                node.left.left = self._splay(node.left.left, key)
                node = self._zig(node)
            elif key > node.left.key:
                node.left.right = self._splay(node.left.right, key)
                if node.left.right:
                    node.left = self._zag(node.left)
            return self._zig(node) if node.left else node
        else:
            if not node.right:
                return node
            if key > node.right.key:
                node.right.right = self._splay(node.right.right, key)
                node = self._zag(node)
            elif key < node.right.key:
                node.right.left = self._splay(node.right.left, key)
                if node.right.left:
                    node.right = self._zig(node.right)
            return self._zag(node) if node.right else node

    def search(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None

    def insert(self, key, value):
        if not self.root:
            self.root = SplayNode(key, value)
            return

        self.root = self._splay(self.root, key)
        if self.root.key == key:
            self.root.value = value
        elif key < self.root.key:
            new_node = SplayNode(key, value)
            new_node.left = self.root.left
            new_node.right = self.root
            self.root.left = None
            self.root = new_node
        else:
            new_node = SplayNode(key, value)
            new_node.right = self.root.right
            new_node.left = self.root
            self.root.right = None
            self.root = new_node



def fibonacci_splay(n, tree):
    if n <= 1:
        return n
    result = tree.search(n)
    if result is not None:
        return result
    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result



def test_fibonacci():
    
    n_values = list(range(0, 951, 50))

   
    lru_times = []
    for n in n_values:
        time = timeit.timeit(lambda: fibonacci_lru(n), number=1)
        lru_times.append(time)

    
    splay_times = []
    for n in n_values:
        tree = SplayTree()
        time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=1)
        splay_times.append(time)

    
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, lru_times, label='LRU Cache', marker='o')
    plt.plot(n_values, splay_times, label='Splay Tree', marker='s')
    plt.xlabel('n (номер числа Фібоначчі)')
    plt.ylabel('Середній час виконання (секунди)')
    plt.title('Порівняння часу виконання: LRU Cache vs Splay Tree')
    plt.legend()
    plt.grid(True)
    plt.show()

  
    print(f"{'n':<10}{'LRU Cache Time (s)':<20}{'Splay Tree Time (s)':<20}")
    print("-" * 50)
    for n, lru_time, splay_time in zip(n_values, lru_times, splay_times):
        print(f"{n:<10}{lru_time:<20.8f}{splay_time:<20.8f}")



if __name__ == "__main__":
    test_fibonacci()
