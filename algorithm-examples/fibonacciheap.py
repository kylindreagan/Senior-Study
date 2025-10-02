#assistance from https://github.com/woodfrog/FibonacciHeap
import math

class FibHeapNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.mark = False

class FibHeap:
    def __init__(self):
        self.min = None
        self.n = 0

    def insert(self, key):
        node = FibHeapNode(key)
        if not self.min:
            self.min = node
        else:
            self._add_to_root_list(node)
            if node.key < self.min.key:
                self.min = node
        self.n += 1
        return node

    def _add_to_root_list(self, node):
        node.left = self.min
        node.right = self.min.right
        self.min.right.left = node
        self.min.right = node

    def find_min(self):
        return self.min.key if self.min else None

    def extract_min(self):
        z = self.min
        if z:
            if z.child:
                children = []
                x = z.child
                while True:
                    children.append(x)
                    x = x.right
                    if x == z.child:
                        break
                for child in children:
                    self._add_to_root_list(child)
                    child.parent = None
            z.left.right = z.right
            z.right.left = z.left
            if z == z.right:
                self.min = None
            else:
                self.min = z.right
                self._consolidate()
            self.n -= 1
        return z.key if z else None

    def _consolidate(self):
        A = [None] * int(math.log(self.n, 2) + 2)
        roots = []
        x = self.min
        while True:
            roots.append(x)
            x = x.right
            if x == self.min:
                break
        for w in roots:
            x = w
            d = x.degree
            while A[d] != None:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self._heap_link(y, x)
                A[d] = None
                d += 1
            A[d] = x
        self.min = None
        for a in A:
            if a:
                if not self.min:
                    self.min = a
                    a.left = a.right = a
                else:
                    self._add_to_root_list(a)
                    if a.key < self.min.key:
                        self.min = a

    def _heap_link(self, y, x):
        y.left.right = y.right
        y.right.left = y.left
        y.parent = x
        if not x.child:
            x.child = y
            y.left = y.right = y
        else:
            y.left = x.child
            y.right = x.child.right
            x.child.right.left = y
            x.child.right = y
        x.degree += 1
        y.mark = False

    def decrease_key(self, x, k):
        if k > x.key:
            raise ValueError("new key is greater than current key")
        x.key = k
        y = x.parent
        if y and x.key < y.key:
            self._cut(x, y)
            self._cascading_cut(y)
        if x.key < self.min.key:
            self.min = x

    def _cut(self, x, y):
        if x.right == x:
            y.child = None
        else:
            x.right.left = x.left
            x.left.right = x.right
            if y.child == x:
                y.child = x.right
        y.degree -= 1
        self._add_to_root_list(x)
        x.parent = None
        x.mark = False

    def _cascading_cut(self, y):
        z = y.parent
        if z:
            if not y.mark:
                y.mark = True
            else:
                self._cut(y, z)
                self._cascading_cut(z)

def main():
    fib = FibHeap()
    a = fib.insert(10)
    b = fib.insert(3)
    c = fib.insert(15)
    d = fib.insert(6)
    fib.insert(2)

    print("Min:", fib.find_min())  # 2
    print("Extract Min:", fib.extract_min())
    print("New Min:", fib.find_min())  # 3

    fib.decrease_key(c, 1)
    print("New Min after decrease-key:", fib.find_min())  # 1