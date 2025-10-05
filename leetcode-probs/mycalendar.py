#RED BLACK TREES. Assistance from https://www.youtube.com/watch?v=KC3X3h5Uyok
RED = True
BLACK = False

class Node:
    def __init__(self, key, value, color=RED):
        self.key = key
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    def __init__(self):
        self.root = None

    def _is_red(self, node):
        return node is not None and node.color == RED

    def get(self, key):
        node = self.root
        while node:
            if key == node.key:
                return node.value
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    # Floor = largest key <= given key
    def floor_key(self, key):
        node = self.root
        floor = None
        while node:
            if node.key == key:
                return node.key
            elif node.key > key:
                node = node.left
            else:
                floor = node.key
                node = node.right
        return floor

    # Ceil = smallest key >= given key
    def ceiling_key(self, key):
        node = self.root
        ceil = None
        while node:
            if node.key == key:
                return node.key
            elif node.key < key:
                node = node.right
            else:
                ceil = node.key
                node = node.left
        return ceil

    def insert(self, key, value):
        # Insert node like in a BST
        new_node = Node(key, value)
        if self.root is None:
            self.root = new_node
            self.root.color = BLACK
            return

        parent = None
        curr = self.root
        while curr:
            parent = curr
            if key < curr.key:
                curr = curr.left
            elif key > curr.key:
                curr = curr.right
            else:
                curr.value = value
                return

        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self._fix_insert(new_node)

    # Simplified rotation/fix logic
    def _rotate_left(self, node):
        right = node.right
        node.right = right.left
        if right.left:
            right.left.parent = node
        right.parent = node.parent
        if not node.parent:
            self.root = right
        elif node == node.parent.left:
            node.parent.left = right
        else:
            node.parent.right = right
        right.left = node
        node.parent = right

    def _rotate_right(self, node):
        left = node.left
        node.left = left.right
        if left.right:
            left.right.parent = node
        left.parent = node.parent
        if not node.parent:
            self.root = left
        elif node == node.parent.right:
            node.parent.right = left
        else:
            node.parent.left = left
        left.right = node
        node.parent = left

    def _fix_insert(self, node):
        while node.parent and node.parent.color == RED:
            grand = node.parent.parent
            if node.parent == grand.left:
                uncle = grand.right
                if self._is_red(uncle):
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    grand.color = RED
                    node = grand
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._rotate_left(node)
                    node.parent.color = BLACK
                    grand.color = RED
                    self._rotate_right(grand)
            else:
                uncle = grand.left
                if self._is_red(uncle):
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    grand.color = RED
                    node = grand
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._rotate_right(node)
                    node.parent.color = BLACK
                    grand.color = RED
                    self._rotate_left(grand)
        self.root.color = BLACK


class MyCalendar:
    def __init__(self):
        self.calendar = RedBlackTree()

    def book(self, startTime: int, endTime: int) -> bool:
        floorkey = self.calendar.floor_key(startTime)
        ceilkey = self.calendar.ceiling_key(startTime)

        if ((floorkey is None or self.calendar.get(floorkey) <= startTime)
            and (ceilkey is None or endTime <= ceilkey)):
            self.calendar.insert(startTime, endTime)
            return True

        return False
