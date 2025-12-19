#!/usr/bin/env python3
"""
Test script for Merkle tree implementation using pytest assertions
"""

import merkle

def test_merkle_tree_valid_input_2_elements():
    """Test creating Merkle tree with 2 elements"""
    data = ['apple', 'banana']
    tree = merkle.mkTree(data)
    assert tree is not None, "Failed to create tree with 2 elements"

    root = merkle.getMerkleRoot(tree)
    assert root is not None, "Failed to get merkle root"
    assert isinstance(root, str), "Root should be a string"

def test_merkle_tree_valid_input_4_elements():
    """Test creating Merkle tree with 4 elements"""
    data = ['a', 'b', 'c', 'd']
    tree = merkle.mkTree(data)
    assert tree is not None, "Failed to create tree with 4 elements"

    root = merkle.getMerkleRoot(tree)
    assert root is not None, "Failed to get merkle root"
    assert isinstance(root, str), "Root should be a string"

def test_merkle_tree_invalid_input_non_power_of_2():
    """Test that creating Merkle tree with non-power-of-two elements fails"""
    data = ['a', 'b', 'c']
    tree = merkle.mkTree(data)
    assert tree is None, "Should have failed for non-power-of-two input"

def test_merkle_tree_with_proofs():
    """Test proof generation and validation"""
    data = ['apple', 'banana', 'cherry', 'date']
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
        assert validation_result is True, f"Proof for '{element}' should validate correctly"

def test_merkle_tree_proof_negative_validation():
    """Test that proofs cannot be incorrectly validated (negative test)"""
    data = ['apple', 'banana', 'cherry', 'date']
    tree = merkle.mkTree(data)
    assert tree is not None, "Failed to create tree for negative proof tests"

    root = merkle.getMerkleRoot(tree)
    assert root is not None, "Failed to get merkle root"

    # Generate proof for 'apple'
    apple_proof = merkle.mkProof(tree, 'apple')
    assert apple_proof is not None, "Failed to generate proof for 'apple'"

    # Try to validate 'apple' proof against 'cherry' - this should fail
    validation_result = merkle.validateProof('cherry', apple_proof, root)
    assert validation_result is False, "Proof for 'apple' should not validate for 'cherry'"
