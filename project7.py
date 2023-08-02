import hashlib
import time


class GenericHashChain:
    def __init__(self):
        self.chain = []
    def add_block(self, data):
        if len(self.chain) == 0:
            previous_hash = '0'  # 初始块的哈希值为0
        else:
            previous_block = self.chain[-1]
            previous_hash = previous_block['hash']
        block = {
            'data': data,
            'previous_hash': previous_hash,
            'hash': self._generate_hash(data, previous_hash)
        }
        self.chain.append(block)

    def _generate_hash(self, data, previous_hash):
        sha = hashlib.sha256()
        sha.update(data.encode('utf-8') + previous_hash.encode('utf-8'))
        return sha.hexdigest()



start = time.perf_counter()

ghc = GenericHashChain()

ghc.add_block('第一个块的内容')
ghc.add_block('第二个块的内容')
ghc.add_block('第三个块的内容')

for block in ghc.chain:
    print(block)

end = time.perf_counter()
print(end - start)
