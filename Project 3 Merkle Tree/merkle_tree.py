
import operator
import math
import hashlib
import random

leaf_count = 100000

class MerkleTreeNode:
    def __init__(self, node_id, hash_val, left_child, right_child, parent):
        self.node_id = node_id
        self.hash_val = hash_val
        self.left_child = left_child
        self.right_child = right_child
        self.parent = parent

class MerkleTree:
    def __init__(self, n, leaves, layers, cntlayers):
        self.n = n
        self.layers = []
        self.leaves = []
        self.cntlayers = int(math.log(n,2)+1)

    def fill_leaf(self, MerkleTreeNode):
        self.leaves.append(MerkleTreeNode)

    def construct_layers(self):
        i = 1
        for i in range(self.cntlayers):
            self.layers.append([])

    def fill_leaves(self):
        self.layers = self.layers + [self.leaves]

    def build_tree(self):
        self.fill_leaves()
        self.construct_layers()
        #build_tree
        len_layer = int(self.n/2)
        ctr = self.n #Node ID counter
        for i in range(1,self.cntlayers):
            if(len_layer==1):# Root Node
                ctr = ctr +1 #Node ID counter
                self.layers[i].append(MerkleTreeNode(ctr, 0, 0, 0, 0))
                hash_val1 = int(''.join(format(ord(x), 'b') for x in self.layers[i-1][0].hash_val))
                hash_val2 = int(''.join(format(ord(x), 'b') for x in self.layers[i-1][1].hash_val))
                temp = operator.xor(hash_val1,hash_val2)
                self.layers[i][0].hash_val = hashlib.sha256(str(temp).encode()).hexdigest()
                self.layers[i][0].left_child = self.layers[i-1][0].node_id
                self.layers[i][0].right_child = self.layers[i-1][1].node_id
                self.layers[i-1][0].parent = ctr
                self.layers[i-1][1].parent = ctr

            else: # Inner nodes
                k=0
                rng = len(self.layers[i-1]) # Child layer length
                for j in range(len_layer):
                    if k < rng:
                        ctr = ctr +1 #Node ID counter
                        self.layers[i].append(MerkleTreeNode(ctr, 0, 0, 0, 0))
                        hash_val1 = int(''.join(format(ord(x), 'b') for x in self.layers[i-1][k].hash_val))
                        hash_val2 = int(''.join(format(ord(x), 'b') for x in self.layers[i-1][k+1].hash_val))
                        temp = operator.xor(hash_val1,hash_val2)
                        # (SHA256.new(str(temp).encode())).hexdigest()
                        self.layers[i][j].hash_val = hashlib.sha256(str(temp).encode()).hexdigest()
                        self.layers[i][j].left_child = self.layers[i-1][k].node_id
                        self.layers[i][j].right_child = self.layers[i-1][k+1].node_id
                        self.layers[i-1][k].parent = ctr
                        self.layers[i-1][k+1].parent = ctr
                        k = k+2
                len_layer = int(len_layer/2)

    def find_root(self):
        return self.layers[self.cntlayers-1][0].hash_val

    def print_tree(self):
        for i in range(self.cntlayers):
            for j in range(len(self.layers[i])):
                print(self.layers[i][j].node_id, self.layers[i][j].hash_val, self.layers[i][j].left_child, self.layers[i][j].right_child, self.layers[i][j].parent)

    def find_node_from_id(self, node_id):
        for i in range(self.cntlayers):
            for j in range(len(self.layers[i])):
                temp = self.layers[i][j].node_id
                if (temp == node_id):
                    return self.layers[i][j]

    def find_path(self, node_id):
        path = []
        pivot = self.find_node_from_id(node_id)
        for i in range(self.cntlayers):
            parent = 0
            for j in range(len(self.layers[i])):
                if(pivot.parent == self.layers[i][j].node_id):
                    parent = self.layers[i][j]
                    if parent.left_child == pivot.node_id:
                        path.append(self.find_node_from_id(parent.right_child).hash_val)
                    else:
                        path.append(self.find_node_from_id(parent.left_child).hash_val)
                    pivot = parent
        return path

def root_from_path(path, node_hash):
    root = node_hash
    for i in range(len(path)):
        hash_val1 = int(''.join(format(ord(x), 'b') for x in path[i]))
        hash_val2 = int(''.join(format(ord(x), 'b') for x in root))
        temp = operator.xor(hash_val1, hash_val2)
        root = hashlib.sha256(str(temp).encode()).hexdigest()
    return root




tree1 = MerkleTree(leaf_count,[],[],0)
for i in range(leaf_count):
    tree1.fill_leaf(MerkleTreeNode(i+1,hashlib.sha256(str(i).encode()).hexdigest(),0,0,0))

tree1.build_tree()

root = tree1.find_root()
node_id = random.randrange(1,leaf_count)
node_hash = tree1.find_node_from_id(node_id).hash_val
path = tree1.find_path(node_id)
found_root = root_from_path(path,node_hash)


print("Number of Leaves: "+ str(leaf_count))
# tree1.print_tree()
print("Root of the Merkle tree: ")
print(root)
print("Hash Value of the Node with ID "+str(node_id)+": ")
print(node_hash)
print("Path of the Node with ID "+str(node_id)+":")
for i in path:
    print(i)
print("Found root with Path and Hash of the Node with ID "+str(node_id)+": ")
print(found_root)

