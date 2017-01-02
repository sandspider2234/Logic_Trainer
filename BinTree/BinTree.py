class BinTreeNode(object):
    def __init__(self, info):
        self.left = None
        self.right = None
        self.info = info

    def insert_left_child(self, node):
        if self.left is None:
            self.left = BinTreeNode(node)
        else:
            tree = BinTreeNode(node)
            tree.left = self.left
            self.left = tree

    def insert_right_child(self, node):
        if self.right is None:
            self.right = BinTreeNode(node)
        else:
            tree = BinTreeNode(node)
            tree.right = self.right
            self.right = tree


def build_tree(string):
    tree = BinTreeNode(None)
    for index, char in enumerate(string):
        if tree.info is None:
            if (char == '|' and string[index + 1] == '|') or \
                    (char == '&' and string[index + 1] == '&'):
                tree = BinTreeNode(string[index:index + 2])
                tree.insert_right_child(build_tree(string[index + 2:len(string)]))
                tree.insert_left_child(build_tree(string[:index]))
    for index, char in enumerate(string):
        if tree.info is None:
            if (char == '<' and string[index + 1] == '=') or \
                    (char == '>' and string[index + 1] == '=') or \
                    (char == '=' and string[index + 1] == '=') or \
                    (char == '!' and string[index + 1] == '='):
                tree = BinTreeNode(string[index:index + 2])
                tree.insert_right_child(build_tree(string[index + 2:len(string)]))
                tree.insert_left_child(build_tree(string[:index]))
            elif char == '>' or char == '<':
                tree = BinTreeNode(char)
                tree.insert_right_child(build_tree(string[index + 1:len(string)]))
                tree.insert_left_child(build_tree(string[:index]))
    if tree.info is None:
        return BinTreeNode(string.strip())
    return tree


def solve_tree(tree, x, y):
    options = {"&&": (lambda left, right: left and right),
               "||": (lambda left, right: left or right),
               "<": (lambda left, right: left < right),
               ">": (lambda left, right: left > right),
               ">=": (lambda left, right: left >= right),
               "<=": (lambda left, right: left <= right),
               "==": (lambda left, right: left == right),
               "!=": (lambda left, right: left != right)}
    if tree.info in options:
        return options[tree.info](solve_tree(tree.left.info, x, y), solve_tree(tree.right.info, x, y))
    elif tree.info == 'x':
        return x
    elif tree.info == 'y':
        return y
    return int(tree.info)
