import hashlib
import random
from typing import Any, List, Tuple

HASHFUNC = hashlib.sha256
HASH_SEPERATOR = "||"

# Beispiel für Merkle tree proof

# tree = mkTree(range(128))
# prf = mkProof(tree, 74)
prf_128 = [
    ("f369cb89fc627e668987007d121ed1eacdc01db9e28f8bb26f358b7d8c4f08ac", False),
    ("413065f380facd824c9cacd988e472d8ef2dca4c34c8191185ee51d58061b75c", True),
    ("1742f0540aad553b211ef52904b7a43d39d346fad800b331e2e597805bdd66a2", False),
    ("7cc5e0417110c0e99f4ea42db6a4059b4144a7a5e9dee1c93e1425b574d2b179", True),
    ("debeb53a138253b381037015e970cb6b656b5d59801c05185c173a18b55a27e3", False),
    ("dccba2156082b4fcb0a10426172bcf6d0b29df7bd515d78be45e19ddfda135a3", False),
    ("2f2ba8b3c57f00d639c48265900a9db0af04ad2abb9822670b0e822c9927a413", True),
]
# root_128 = getMerkleRoot(tree)
root_128 = "e65dfeb38aa330e7691b1abed7b9894f2114ce1c9bb19149cf9da5c5be4c834d"


class Node:
    def __init__(self):
        self.left: Node | None = None
        self.right: Node | None = None
        self.hashVal: str = ""
        self.content: int | None = None
        self.parent: Node | None = None

    def __str__(self):
        if self.content is None:
            return (
                "Node: "
                + self.hashVal
                + "\n left: "
                + self.left.__str__()
                + "\n right: "
                + self.right.__str__()
            )
        else:
            return "Leaf: " + str(self.content)

    def __repr__(self):
        return self.__str__()


def nodeHash(left: str | None, right: str | None) -> str:
    if not left or not right:
        return ""
    h = HASHFUNC()
    h.update(left.encode())
    h.update(HASH_SEPERATOR.encode())
    h.update(right.encode())
    return h.hexdigest()


def mkNode(left: Node, right: Node) -> Node:
    node = Node()
    node.left = left
    node.right = right
    node.hashVal = nodeHash(left.hashVal, right.hashVal)

    left.parent = node
    right.parent = node

    return node


def mkLeaf(content: int) -> Node:
    leaf = Node()
    leaf.content = content
    leaf.hashVal = HASHFUNC(str(content).encode()).hexdigest()
    return leaf


def mkTree(valList: List) -> Node | None:
    n = len(valList)
    if not (n & (n - 1) == 0) or n == 0:
        # "The number of elements in our MerkleTree must be a power of 2"
        return None

    currentLayer: List[Node] = []
    for val in valList:
        currentLayer.append(mkLeaf(val))

    while len(currentLayer) > 1:
        nextLayer: List[Node] = []
        while currentLayer:
            left = currentLayer.pop(0)
            right = currentLayer.pop(0)
            nextLayer.append(mkNode(left, right))
        currentLayer = nextLayer
    return currentLayer.pop()


def getMerkleRoot(tree: Node) -> str:
    return tree.hashVal


def find_leaf_node(tree: Node | None, element: int) -> Node | None:
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


def mkProof(tree: Node, element: Any) -> List[Tuple[str, bool]] | None:
    node = find_leaf_node(tree, element)
    if node is None:
        return None

    proof = []
    while node.parent:
        if node.parent.left == node:
            assert isinstance(node.parent.right, Node)
            proof.append((node.parent.right.hashVal, False))
        else:
            assert isinstance(node.parent.left, Node)
            proof.append((node.parent.left.hashVal, True))
        node = node.parent
    return proof


def validateProof(element: Any, proof: List[Tuple[str, bool]], root_hash: str):
    # Recalculate the hashes based on the provided hashes in the prove.
    cur_hash = HASHFUNC(str(element).encode()).hexdigest()
    # iterate over all tuples
    for next_hash, is_left in proof:
        # swap left and right if necessary and calculate next hash
        (left, right) = (next_hash, cur_hash) if is_left else (cur_hash, next_hash)
        cur_hash = nodeHash(left, right)

    # if the provided hashes allow us to correctly recalculate the root hash, we can be sure that the element is part of the tree
    return cur_hash == root_hash


def mkZkTree(valList):
    n = len(valList)
    if not (n & (n - 1) == 0) or n == 0:
        # "The number of elements in our ZKMerkleTree must be a power of 2"
        # This will be checked again in mkTree, but we can return early here
        return None

    # When searching for an element in the tree we do not want to find our random filler leafs.
    # This magic string is used to make sure that the random content cannot match the "real" contents.
    # A better solution would be to add a "isFillerNode" flag to the Nodes
    # or to have separate classes for "Root", "Node", "Leaf" and "ZKLeaf" which all inherit from a "BaseNode" class.
    MAGIC = "ThisValueShouldNotBePresentInTheContent"

    # Interleave a list of normal values with a list of random values.
    # This will result in a merkle tree where the right leaves always contain random values.
    zkValList = []
    for i in range(len(valList)):
        zkValList.append(valList[i])
        # For each element, append a salt that will be the corresponding next (right) node
        zkValList.append(MAGIC + str(random.randint(1, 2**32)))

    return mkTree(zkValList)
