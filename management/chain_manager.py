import os
import logging
#from varieties.recipe import Recipe

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class ChainManager(object):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.head = None
        self.tail = None
        self.count = 0


    def add_head(self, node, position=None):

        tmp = self.head
        self.head = node
        self.head.index = self.count + 1
        self.head.next = tmp
        self.count += 1


    def remove_node(self, position=0):
        """
        if this is linked list
        :param position:
        :return:
        """
        current = self.head
        if position > self.count:
            raise Exception()
        count = 0
        while current:
            if count > position:
                current = current.next
            current = current.next

        return None


    def revert_path_from_root(self, start, node):
         """
         Revert from root
         :param node:
         :return:
         """
         newlist = None
         return newlist

    def find_ansector(self, first_node, second_node):
         first_revereted = self.revert_path(self.head, first_node)

    @property
    def length(self):
        return self.count



class RecipeTree:
    def __init__(self):

        self.root = None


    def add_node(self, node, root=None):
        if self.root is None:
            self.root = node
            return
        if node is None:
            return node
        else:
            current = root
            while current:
                if node.hydration > current.hydration:
                    current.right = self.add_node(node, current.right)
                else:
                    current.left = self.add_node(node, current.left)

    def find_node(self, root, value):
        while root:
            if value == root.value:
                return root
            else:
                if value > root.value:
                    self.find_node(root.left, value)
                else:
                    self.find_node(root.right, value)
        return None

    def level_order_traverse(self, current=None, node_list=None):
        if not current:
            current = self.root
        if not node_list:
            node_list = []
        while current:
            self.level_order_traverse(current.left, node_list)
            node_list.append(current)
            self.level_order_traverse(current.right, node_list)

        return node_list



def parse_options():
    parser = argparse.ArgumentParser(description='Calculate recipe')
    parser.add_argument('-w', "--workbook",  metavar='filepath', type=str,
                        help='file path')
    parser.add_argument('--sheet',  metavar='sheet', type=str,
                        help='sheet name')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    return args


def main():

    m = ChainManager()
    m.add_node()
    exit(0)

    options = parse_options()
    manager = ChainManager()

    bread = Bread(options)

    bread.analyze_hydration(bread.recipe)
    bread.analyze_flours(bread.recipe)
    bread.analyze_cooking_conditions(bread.recipe)
    new_hydration_percent = 80
    bread.change_hydration(new_hydration_percent, bread.recipe)
    print('Changed hydration to {}'.format(new_hydration_percent))
    print(bread.reindexed_recipe)
    #bread.scale_recipe(bread.recipe, times=2)
    #print('Scaled recipe:')
    #print(bread.reindexed_recipe)
    bread.to_xl()




if __name__ == "__main__":
    main()