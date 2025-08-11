class GraphMax:
    def __init__(self, G):
        self.G = G
        self.matching = {}

    def bpm(self, u, visited):
        for v in self.G[u]["assigned"]:
            if not visited[v]:
                visited[v] = True
                if v not in self.matching or self.bpm(
                    self.matching[v]["assigned"], visited
                ):
                    self.matching[v] = {"assigned": u}
                    return

    def get_max_matching(self):
        self.matching = {}
        for u in self.G.keys():
            visited = {v: False for v in self.G}
            self.bpm(u, visited)

        for u in self.G:
            if u not in self.matching:
                self.matching[u] = {"assigned": None}

        return self.matching
