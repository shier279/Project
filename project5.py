import hashlib
import time

def calculate_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.digest()

def build_merkle_tree(data):
    leaf_nodes = [calculate_hash(d) for d in data]
    while len(leaf_nodes) & (len(leaf_nodes) - 1) != 0:
        leaf_nodes.append(b'\x00')
    nodes = leaf_nodes[:]
    while len(nodes) > 1:
        level_nodes = []
        for i in range(0, len(nodes), 2):
            left_node = nodes[i]
            right_node = nodes[i+1] if i+1 < len(nodes) else nodes[i]
            merged_node = calculate_hash(left_node + right_node)
            level_nodes.append(merged_node)
        nodes = level_nodes
    return nodes[0]

start = time.perf_counter()
data = [b'hello', b'world', b'foo', b'bar']
merkle_root = build_merkle_tree(data)
print("Merkle Root:", merkle_root.hex())
end = time.perf_counter()
print(end -start)
