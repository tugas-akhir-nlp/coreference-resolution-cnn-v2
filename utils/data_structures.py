from typing import Set, Dict, List


class UFDS:
    def __init__(self):
        self.nodes: Set[int] = set()
        self.parent: Dict[int, int] = {}

    def init_id(self, *nodes: int) -> None:
        for node in nodes:
            if node not in self.nodes:
                self.nodes.add(node)
                self.parent[node] = node

    def root(self, x: int) -> int:
        self.init_id(x)

        if self.parent[x] == x:
            return x
        else:
            self.parent[x] = self.root(self.parent[x])
            return self.parent[x]

    def join(self, x: int, y: int) -> None:
        self.init_id(x, y)

        self.parent[self.root(x)] = self.root(y)

    def is_same(self, x: int, y: int) -> bool:
        self.init_id(x, y)

        return self.root(x) == self.root(y)

    def get_chain_list(self) -> List[List[int]]:
        chain_parents = [x for x in self.nodes if self.root(x) == x]

        chain_list = [
            [y for y in self.nodes if self.is_same(x, y)]
            for x in chain_parents
        ]

        return chain_list

    def get_chain_dict(self) -> Dict[int, List[int]]:
        chain_parents = [x for x in self.nodes if self.root(x) == x]

        chain_dict = {
            x: [y for y in self.nodes if self.is_same(x, y)]
            for x in chain_parents
        }

        return chain_dict
