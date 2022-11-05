class DFS:
    def __init__(self, graph) -> None:
        self.G = graph
        self.V = []

    def DFSUtil(self, v, visited):
        visited[v] = True
        self.V.append(v)

        for i in self.G[v]:
            if visited[i] == False:
                self.DFSUtil(i, visited)

    def DFS(self):
        visited = {v: False for v in list(self.G.keys())}

        for i in self.G:
            if visited[i] == False:
                self.DFSUtil(i, visited)

        return self.V

class BFS:
    def __init__(self, graph) -> None:
        self.G = graph
        self.V = []

    def BFS(self):
        visited = {v: False for v in list(self.G.keys())}

        for i in self.G:
            if not visited[i]:
                q = []
                visited[i] = True
                q.append(i)

                while len(q) > 0:
                    g_node = q.pop(0)
                    self.V.append(g_node)

                    for n in self.G[g_node]:
                        if not visited[n]:
                            visited[n] = True
                            q.append(n)

        return self.V

class Dijkstra:
    def __init__(self, graph) -> None:
        self.G = graph
        self.V = []

    def Dijkstra(self):
        return