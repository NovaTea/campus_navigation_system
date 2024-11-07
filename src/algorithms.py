import heapq
from collections import deque

def bfs(graph, start, goal):
    visited = set()
    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()
        if node in visited:
            continue
        visited.add(node)

        for neighbor in graph.get_neighbors(node):
            if neighbor == goal:
                return path + [neighbor]
            queue.append((neighbor, path + [neighbor]))

    return None

def dfs(graph, start, goal):
    visited = set()
    stack = [(start, [start])]

    while stack:
        node, path = stack.pop()
        if node in visited:
            continue
        visited.add(node)

        for neighbor in graph.get_neighbors(node):
            if neighbor == goal:
                return path + [neighbor]
            stack.append((neighbor, path + [neighbor]))

    return None

def dijkstra(graph, start, goal):
    import heapq
    heap = [(0, start, [start])]
    visited = set()

    while heap:
        (cost, node, path) = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            return path

        for neighbor, attributes in graph.get_neighbors(node).items():
            if neighbor not in visited:
                distance = attributes['distance']
                heapq.heappush(heap, (cost + distance, neighbor, path + [neighbor]))

    return None
