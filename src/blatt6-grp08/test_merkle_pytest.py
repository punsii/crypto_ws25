#!/usr/bin/env python3
"""
Test script for Merkle tree implementation using pytest assertions
"""

import random

import merkle

EXAMPLE_VALUE = 74
EXAMPLE_TREE_VALUES = list(range(128))
EXAMPLE_PROOF_128 = [
    ("f369cb89fc627e668987007d121ed1eacdc01db9e28f8bb26f358b7d8c4f08ac", False),
    ("413065f380facd824c9cacd988e472d8ef2dca4c34c8191185ee51d58061b75c", True),
    ("1742f0540aad553b211ef52904b7a43d39d346fad800b331e2e597805bdd66a2", False),
    ("7cc5e0417110c0e99f4ea42db6a4059b4144a7a5e9dee1c93e1425b574d2b179", True),
    ("debeb53a138253b381037015e970cb6b656b5d59801c05185c173a18b55a27e3", False),
    ("dccba2156082b4fcb0a10426172bcf6d0b29df7bd515d78be45e19ddfda135a3", False),
    ("2f2ba8b3c57f00d639c48265900a9db0af04ad2abb9822670b0e822c9927a413", True),
]
EXAMPLE_ROOT_128 = "e65dfeb38aa330e7691b1abed7b9894f2114ce1c9bb19149cf9da5c5be4c834d"


def test_validate_example_proof():
    assert merkle.validateProof(EXAMPLE_VALUE, EXAMPLE_PROOF_128, EXAMPLE_ROOT_128)


def test_create_example_leaf():
    leaf = merkle.mkLeaf(EXAMPLE_VALUE)
    assert leaf.content == EXAMPLE_VALUE
    assert leaf.hashVal == merkle.HASHFUNC(str(EXAMPLE_VALUE).encode()).hexdigest()
    assert leaf.left is None
    assert leaf.right is None


def test_create_example_nodes():
    leaf = merkle.mkLeaf(EXAMPLE_VALUE)
    fakeNode0 = merkle.Node()
    fakeNode0.hashVal = EXAMPLE_PROOF_128[0][0]

    node1 = merkle.mkNode(leaf, fakeNode0)
    assert node1.left == leaf
    assert node1.right == fakeNode0
    assert leaf.parent == node1
    assert fakeNode0.parent == node1
    fakeNode1 = merkle.Node()
    fakeNode1.hashVal = EXAMPLE_PROOF_128[1][0]

    node2 = merkle.mkNode(fakeNode1, node1)
    assert node2.left == fakeNode1
    assert node2.right == node1
    assert fakeNode1.parent == node2
    assert node1.parent == node2
    fakeNode2 = merkle.Node()
    fakeNode2.hashVal = EXAMPLE_PROOF_128[2][0]

    node3 = merkle.mkNode(node2, fakeNode2)
    fakeNode3 = merkle.Node()
    fakeNode3.hashVal = EXAMPLE_PROOF_128[3][0]

    node4 = merkle.mkNode(fakeNode3, node3)
    fakeNode4 = merkle.Node()
    fakeNode4.hashVal = EXAMPLE_PROOF_128[4][0]

    node5 = merkle.mkNode(node4, fakeNode4)
    fakeNode5 = merkle.Node()
    fakeNode5.hashVal = EXAMPLE_PROOF_128[5][0]

    node6 = merkle.mkNode(node5, fakeNode5)
    fakeNode6 = merkle.Node()
    fakeNode6.hashVal = EXAMPLE_PROOF_128[6][0]

    node7 = merkle.mkNode(fakeNode6, node6)
    assert node7.left == fakeNode6
    assert node7.right == node6
    assert fakeNode6.parent == node7
    assert node6.parent == node7
    assert node7.hashVal == EXAMPLE_ROOT_128


def test_create_example_tree():
    tree = merkle.mkTree(EXAMPLE_TREE_VALUES)
    assert tree is not None
    assert tree.hashVal == EXAMPLE_ROOT_128


def test_create_example_proofs():
    tree = merkle.mkTree(EXAMPLE_TREE_VALUES)
    assert tree is not None

    example_proof = merkle.mkProof(tree, EXAMPLE_VALUE)
    assert example_proof == EXAMPLE_PROOF_128

    for i in EXAMPLE_TREE_VALUES:
        proof = merkle.mkProof(tree, i)
        assert proof is not None
        assert merkle.validateProof(i, proof, EXAMPLE_ROOT_128)


def test_create_random_proofs():
    values = random.sample(range(1, 2**32), 2**12)
    tree = merkle.mkTree(values)
    assert tree is not None

    for i in values:
        proof = merkle.mkProof(tree, i)
        assert proof is not None
        assert merkle.validateProof(i, proof, tree.hashVal)


def test_create_random_zk_proofs():
    values = random.sample(range(1, 2**32), 2**12)
    tree = merkle.mkZkTree(values)
    assert tree is not None

    for i in values:
        proof = merkle.mkProof(tree, i)
        assert proof is not None
        assert merkle.validateProof(i, proof, tree.hashVal)


def test_cannot_create_proofs():
    values = random.sample(range(1, 2**16), 2**12)
    non_existant_value = random.sample(range(2**17, 2**32), 2**12)
    tree = merkle.mkTree(values)
    assert tree is not None

    for i in non_existant_value:
        proof = merkle.mkProof(tree, i)
        assert proof is None


def test_merkle_tree_valid_input_2_elements():
    """Test creating Merkle tree with 2 elements"""
    data = ["apple", "banana"]
    tree = merkle.mkTree(data)
    assert tree is not None, "Failed to create tree with 2 elements"

    root = merkle.getMerkleRoot(tree)
    assert root is not None, "Failed to get merkle root"
    assert isinstance(root, str), "Root should be a string"


def test_zk_merkle_tree_valid_input_2_elements():
    """Test creating Merkle tree with 2 elements"""
    data = ["apple", "banana"]
    tree = merkle.mkZkTree(data)
    assert tree is not None, "Failed to create tree with 2 elements"

    root = merkle.getMerkleRoot(tree)
    assert root is not None, "Failed to get merkle root"
    assert isinstance(root, str), "Root should be a string"


def test_merkle_tree_valid_input_4_elements():
    """Test creating Merkle tree with 4 elements"""
    data = ["a", "b", "c", "d"]
    tree = merkle.mkTree(data)
    assert tree is not None, "Failed to create tree with 4 elements"

    root = merkle.getMerkleRoot(tree)
    assert root is not None, "Failed to get merkle root"
    assert isinstance(root, str), "Root should be a string"


def test_zk_merkle_tree_valid_input_4_elements():
    """Test creating Merkle tree with 4 elements"""
    data = ["a", "b", "c", "d"]
    tree = merkle.mkZkTree(data)
    assert tree is not None, "Failed to create tree with 4 elements"

    root = merkle.getMerkleRoot(tree)
    assert root is not None, "Failed to get merkle root"
    assert isinstance(root, str), "Root should be a string"


def test_merkle_tree_invalid_input_non_power_of_2():
    """Test that creating Merkle tree with non-power-of-two elements fails"""
    data = ["a", "b", "c"]
    tree = merkle.mkTree(data)
    assert tree is None, "Should have failed for non-power-of-two input"


def test_zk_merkle_tree_invalid_input_non_power_of_2():
    """Test that creating Merkle tree with non-power-of-two elements fails"""
    data = ["a", "b", "c"]
    tree = merkle.mkZkTree(data)
    assert tree is None, "Should have failed for non-power-of-two input"


def test_merkle_tree_with_proofs():
    """Test proof generation and validation"""
    data = ["apple", "banana", "cherry", "date"]
    tree = merkle.mkTree(data)
    assert tree is not None, "Failed to create tree for proof tests"

    root = merkle.getMerkleRoot(tree)
    assert root is not None, "Failed to get merkle root"

    # Test proof generation for each element
    for element in data:
        proof = merkle.mkProof(tree, element)
        assert proof is not None, f"Failed to generate proof for '{element}'"
        assert isinstance(proof, list), f"Proof for '{element}' should be a list"
        assert len(proof) > 0, f"Proof for '{element}' should not be empty"

        # Test proof validation
        validation_result = merkle.validateProof(element, proof, root)
        assert (
            validation_result is True
        ), f"Proof for '{element}' should validate correctly"


def test_zk_merkle_tree_with_proofs():
    """Test proof generation and validation"""
    data = ["apple", "banana", "cherry", "date"]
    tree = merkle.mkZkTree(data)
    assert tree is not None, "Failed to create tree for proof tests"

    root = merkle.getMerkleRoot(tree)
    assert root is not None, "Failed to get merkle root"

    # Test proof generation for each element
    for element in data:
        proof = merkle.mkProof(tree, element)
        assert proof is not None, f"Failed to generate proof for '{element}'"
        assert isinstance(proof, list), f"Proof for '{element}' should be a list"
        assert len(proof) > 0, f"Proof for '{element}' should not be empty"

        # Test proof validation
        validation_result = merkle.validateProof(element, proof, root)
        assert (
            validation_result is True
        ), f"Proof for '{element}' should validate correctly"


def test_merkle_tree_proof_negative_validation():
    """Test that proofs cannot be incorrectly validated (negative test)"""
    data = ["apple", "banana", "cherry", "date"]
    tree = merkle.mkTree(data)
    assert tree is not None, "Failed to create tree for negative proof tests"

    root = merkle.getMerkleRoot(tree)
    assert root is not None, "Failed to get merkle root"

    # Generate proof for 'apple'
    apple_proof = merkle.mkProof(tree, "apple")
    assert apple_proof is not None, "Failed to generate proof for 'apple'"

    # Try to validate 'apple' proof against 'cherry' - this should fail
    validation_result = merkle.validateProof("cherry", apple_proof, root)
    assert (
        validation_result is False
    ), "Proof for 'apple' should not validate for 'cherry'"


def test_zk_merkle_tree_proof_negative_validation():
    """Test that proofs cannot be incorrectly validated (negative test)"""
    data = ["apple", "banana", "cherry", "date"]
    tree = merkle.mkZkTree(data)
    # Note: This is a bit hack, since we cannot be sure 100% that the value is not one of the random placeholder values
    assert tree is not None, "Failed to create tree for negative proof tests"

    root = merkle.getMerkleRoot(tree)
    assert root is not None, "Failed to get merkle root"

    # Generate proof for 'apple'
    apple_proof = merkle.mkProof(tree, "apple")
    assert apple_proof is not None, "Failed to generate proof for 'apple'"

    # Try to validate 'apple' proof against 'cherry' - this should fail
    validation_result = merkle.validateProof("cherry", apple_proof, root)
    assert (
        validation_result is False
    ), "Proof for 'apple' should not validate for 'cherry'"
