#https://www.geeksforgeeks.org/dsa/binomial-heap-2/#
class Node:
    def __init__(self, value):
        self.v = value
        self.p = None
        self.children = []
        self.degree = 0
        self.marked = False

class BinomialHeap:
    def __init__(self, root=None):
        self.trees = []
        self.min_node = None
        self.count = 0
        if root:
            self.trees.append(root)
            self.min_node = root
            self.count = 1
    
    def __len__(self):
        return self.count
    
    def is_empty(self):
        return self.min_node == None
    
    def insert(self, value):
        node = Node(value)
        self.merge(BinomialHeap(node))
    
    def get_min(self):
        return self.min_node.v
    
    def extract_min(self):
        min_node = self.min_node
        self.trees.remove(min_node)
        new_heap = BinomialHeap()
        new_heap.trees = min_node.children
        new_heap.count = sum(self._subtree_size(child) for child in min_node.children)
        self.merge(new_heap)
        self._consolidate()
        self.count -= 1
        return min_node.v
    
    def merge(self, other_heap):
        self.trees.extend(other_heap.trees)
        self.count += other_heap.count
        self._consolidate()
    
    def _find_min(self):
        self.min_node = None
        for tree in self.trees:
            if self.min_node is None or tree.v < self.min_node.v:
                self.min_node = tree
    
    def decrease_key(self, node, new_value):
        if new_value > node.v:
            raise ValueError("New value is greater than current value")
        node.v = new_value
        self._bubble_up(node)
    
    def delete(self, node):
        self.decrease_key(node, float('-inf'))
        self.extract_min()
    
    def _bubble_up(self, node):
        parent = node.p
        while parent is not None and node.v < parent.v:
            node.v, parent.v = parent.v, node.v
            node, parent = parent, node
    
    def _link(self, tree1, tree2):
        if tree1.v > tree2.v:
            tree1, tree2 = tree2, tree1
        tree2.p = tree1
        tree1.children.append(tree2)
        tree1.degree += 1
    
    def _consolidate(self):
        degree_to_tree = {}

        for current in self.trees:  # just iterate over roots
            degree = current.degree
            while degree in degree_to_tree:
                other = degree_to_tree.pop(degree)
                if current.v < other.v:
                    self._link(current, other)
                else:
                    self._link(other, current)
                degree += 1
            degree_to_tree[degree] = current

        self.trees = list(degree_to_tree.values())
        self.min_node = min(self.trees, key=lambda t: t.v, default=None)

    
    def _subtree_size(self, node):
        return 1 + sum(self._subtree_size(child) for child in node.children)