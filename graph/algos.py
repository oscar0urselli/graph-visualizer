class DFS:
    def __init__(self, graph) -> None:
        self.G = graph
        self.V = []

    def DFSUtil(self, v, visited):
        visited[v] = True
        self.V.append((v, (255, 0, 0)))

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
                    self.V.append((g_node, (255, 0, 0)))

                    for n in self.G[g_node]:
                        if not visited[n]:
                            visited[n] = True
                            q.append(n)

        return self.V

class Dijkstra:
    def __init__(self, graph: dict) -> None:
        self.G = graph
        self.V = []

    def Dijkstra(self, start_node: str, end_node: str):
        path = []
        
        dist = {}
        previous = {}

        for k in self.G.keys():
            dist[k] = float('+inf')
            previous[k] = None

            self.V.append((k, (0, 255, 0)))

        dist[start_node] = 0
        Q = list(self.G.keys())

        while len(Q) > 0:
            u = self.min_weight_node(Q, dist)

            self.V.append((u, (194, 86, 50)))

            Q.remove(u)

            if dist[u] == float('+inf'):
                break

            for v in self.G[u]:
                alt = dist[u] + self.G[u][v]
                
                self.V.append((v, (36, 100, 120)))

                if alt < dist[v]:
                    dist[v] = alt
                    previous[v] = u

        path = []
        u = end_node
        while previous[u] != None:
            path.insert(0, u)
            u = previous[u]

        for i in [start_node] + path:
            self.V.append((i, (255, 0, 0)))

        return self.V

    def min_weight_node(self, Q, dist) -> str:
        min_node = None
        min_weight = float('+inf')

        for n in Q:
            if dist[n] < min_weight:
                min_node = n
                min_weight = dist[n]

        return min_node