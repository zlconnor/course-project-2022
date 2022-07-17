import operator
import hashlib
import math
import random

class MerkleTreeNode:
    def __init__(self, node_id, hash_val, left_child, right_child, parent):
        self.node_id = node_id
        self.hash_bal=hash_val
        self.left_child = left_child
        self.right_child = right_child
        self.parent = parent

class MerkleTree:
    def __init__(self, n, leaves, layers, layer_num):
        self.n = n
        self.layers = []
        self.leaves = []
        self.layer_num = int(math.log(n,2)+1)
    
    def fill_leaf(self,MerkleTreeNode):
        self.leaves.append(MerkleTreeNode)
    
    def shape_layers(self):
        i=1
        for i in range(self.layer_num):
            self.layers.append([])
    
    def fill_leaves(self):
        self.layers+=[self.leaves]
    
    def construct_tree(self):
        self.fill_leaves()
        self.shape_layers()

        len_layer=int(self.n/2)
        node_id_count=self.n
        for i in range(1,self.layer_num):
            if len_layer==1:# 如果是根结点
                node_id_count+=1
                self.layers[i].append(MerkleTreeNode(node_id_count,0,0,0,0))
                hash_val1 = int(''.join(format(ord(x), 'b') for x in self.layers[i-1][0].hash_val))
                hash_val2 = int(''.join(format(ord(x), 'b') for x in self.layers[i-1][1].hash_val))
                tmp=operator.xor(hash_val1,hash_val2)
                self.layers[i][0].hash_val = hashlib.sha256(str(tmp).encode()).hexdigest()
                self.layers[i][0].left_child = self.layers[i-1][0].node_id
                self.layers[i][0].right_child = self.layers[i-1][1].node_id
                self.layers[i-1][0].parent = node_id_count
                self.layers[i-1][1].parent = node_id_count
            else: # 如果是内部结点
                k=0
                rng = len(self.layers[i-1]) # Child layer length
                for j in range(len_layer):
                    if k < rng:
                        node_id_count+=1
                        self.layers[i].append(MerkleTreeNode(node_id_count, 0, 0, 0, 0))
                        hash_val1 = int(''.join(format(ord(x), 'b') for x in self.layers[i-1][k].hash_val))
                        hash_val2 = int(''.join(format(ord(x), 'b') for x in self.layers[i-1][k+1].hash_val))
                        tmp = operator.xor(hash_val1,hash_val2)
                        self.layers[i][j].hash_val = hashlib.sha256(str(tmp).encode()).hexdigest()
                        self.layers[i][j].left_child = self.layers[i-1][k].node_id
                        self.layers[i][j].right_child = self.layers[i-1][k+1].node_id
                        self.layers[i-1][k].parent = node_id_count
                        self.layers[i-1][k+1].parent = node_id_count
                        k += 2
                len_layer = int(len_layer/2)
    def find_root(self):
                return self.layers[self.layer_num-1][0].hash_val
    
    def print_tree(self):
        for i in range(self.layer_num):
            for j in range(len(self.layers[i])):
                print(self.layers[i][j].node_id, self.layers[i][j].hash_val, self.layers[i][j].left_child, self.layers[i][j].right_child, self.layers[i][j].parent)

    def find_node_from_id(self, node_id):
        for i in range(self.layer_num):
            for j in range(len(self.layers[i])):
                tmp = self.layers[i][j].node_id
                if (tmp == node_id):
                    return self.layers[i][j]
    
    def find_path(self, node_id):
        path = []
        pivot = self.find_node_from_id(node_id)
        for i in range(self.layer_num):
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
            tmp = operator.xor(hash_val1, hash_val2)
            root = hashlib.sha256(str(tmp).encode()).hexdigest()
        return root

if __name__ == "__main__":
    num_of_leaves=8
    MT=MerkleTree(num_of_leaves,[],[],0)
    for i in range(num_of_leaves):
        MT.fill_leaf(MerkleTreeNode(i+1,hashlib.sha256(str(i).encode()).hexdigest(),0,0,0))
    MT.construct_tree()

    root=MT.find_root()
    node_id=random.rangerange(1,num_of_leaves)
    node_hash=MT.find_node_from_id(node_id).hash_val
    path=MT.find_path(node_id)
    root_found=MT.root_from_path(path,node_hash)

    print("Number of Leaves: ",str(num_of_leaves))
    MT.print_tree()
    print("Root of the Merkle Tree: ")
    print(root)
    print("Hash Value of the Node with ID "+str(node_id))
    print(node_hash)





