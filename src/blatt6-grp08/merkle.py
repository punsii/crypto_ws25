import hashlib
import math

hash_separator = "||"

# Beispiel für Merkle tree proof

# tree = mkTree(range(128))
# prf = mkProof(tree, 74)
prf_128 =  [('f369cb89fc627e668987007d121ed1eacdc01db9e28f8bb26f358b7d8c4f08ac', False),
            ('413065f380facd824c9cacd988e472d8ef2dca4c34c8191185ee51d58061b75c', True),
            ('1742f0540aad553b211ef52904b7a43d39d346fad800b331e2e597805bdd66a2', False),
            ('7cc5e0417110c0e99f4ea42db6a4059b4144a7a5e9dee1c93e1425b574d2b179', True),
            ('debeb53a138253b381037015e970cb6b656b5d59801c05185c173a18b55a27e3', False),
            ('dccba2156082b4fcb0a10426172bcf6d0b29df7bd515d78be45e19ddfda135a3', False),
            ('2f2ba8b3c57f00d639c48265900a9db0af04ad2abb9822670b0e822c9927a413', True)]
# root_128 = getMerkleRoot(tree)
root_128 = 'e65dfeb38aa330e7691b1abed7b9894f2114ce1c9bb19149cf9da5c5be4c834d'

class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.hashVal = None
        self.content = None
        self.parent = None

    def __str__(self):
        if self.content == None:
            return "Node: " + self.hashVal + "\n left: " + \
                   self.left.__str__() + "\n right: " + self.right.__str__()
        else:
            return "Leaf: " + str(self.content)

    def __repr__(self):
        return self.__str__()

def mkNode(l, r):
    return None

def mkLeaf(content):
    return None

def mkTree(valList):
    return None

def getMerkleRoot(tree):
    return tree.hashVal


def find_leaf_node(tree, element):
    """
    Findet ein Element in einem Baum oder gibt None zurück
    """
    if tree is None:
        return None

    # If this is a leaf node
    if tree.content is not None:
        if tree.content == element:
            return tree
        else:
            return None

    # If this is an internal node, search in children
    left_result = find_leaf_node(tree.left, element)
    if left_result:
        return left_result

    right_result = find_leaf_node(tree.right, element)
    if right_result:
        return right_result

    return None

def mkProof(tree, element):
    return None

def validateProof(element, proof, root_hash):
    return None

def mkZkTree(valList):
    return None
