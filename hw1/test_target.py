import Queue as Queue

def main():
    method, start, end, routes, heuristics = readFile("input.txt")
    if method == "BFS": res = bfs(start, end, routes)
    elif method == "DFS": res = dfs(start, end, routes, [], set(), set())
    elif method == "UCS": res = ucs(start, end, routes)
    elif method == "A*": res = a_star(start, end, routes, heuristics)
    else: res = ["Invalid method!"]
    f = open("output.txt", 'w')
    f.write('\n'.join(res))
    f.write('\n')
    f.close()

def readFile(fname):
    f = open(fname, 'r')
    method = f.readline().strip()
    start = f.readline().strip()
    end = f.readline().strip()
    n_routes, routes = int(f.readline().strip()), {}
    for i in range(n_routes):
        route = f.readline().split()
        if route[0] not in routes: routes[route[0]] = []
        routes[route[0]].append((route[1], int(route[2])))
    heuristics = {}
    if method == 'A*':
        n_heu = int(f.readline().strip())
        for i in range(n_heu):
            heuristic = f.readline().split()
            heuristics[heuristic[0]] = int(heuristic[1])
    f.close()
    return (method, start, end, routes, heuristics)
 
def bfs(start, end, graph):
    queue, visited, res = Queue.Queue(), set(), []
    queue.put([start])
    while queue:
        path = queue.get()
        state = path[-1]
        visited.add(state)
        if state == end:
            for i in range(len(path)):
                res.append(path[i]+' '+str(i))
            return res
        if state in graph:
            for nextState in graph[state]:
                if nextState[0] not in visited:
                    queue.put(path + [nextState[0]])
    return ["No path is detected!"]
           
def dfs(state, end, graph, path, visited, frontier):
    visited.add(state)
    if state in graph:
        neighbors, res = set(), []
        for nextState in graph[state]:
            if nextState[0] == end:
                path.append(state)
                path.append(end)
                for i in range(len(path)):
                    res.append(path[i]+' '+str(i))
                return res
            neighbors.add(nextState[0])
        for nextState in graph[state]:
            if nextState[0] not in visited and nextState[0] not in frontier:
                p = dfs(nextState[0], end, graph, path+[state], visited, frontier.union(neighbors))
                if p: return p
    if not path:
        return ["No path is detected"]
    
def ucs(start, end, graph):
    queue, visited, res, time = Queue.PriorityQueue(), set(), [], 0
    queue.put((0, time, [start], [0]))
    while queue:
        path = queue.get()
        state = path[2][-1]
        visited.add(state)
        if state == end:
            for i in range(len(path[3])):
                res.append(path[2][i]+' '+str(path[3][i]))
            return res
        if state in graph:
            for nextNode in graph[state]:
                cost = path[3][-1] + nextNode[1]
                time += 1
                queue.put((cost, time, path[2]+[nextNode[0]], path[3]+[cost]))
    return ["No path is detected!"]
    
def a_star(start, end, graph, heus):
    queue, res, time, sol, visited = Queue.PriorityQueue(), [], 0, [], {}
    queue.put((heus[start], time, [start], [0]))
    while not queue.empty():
        path = queue.get()
        state = path[2][-1]
        visited[state] = path[3][-1]
        if state == end:
            for i in range(len(path[3])):
                res.append(path[2][i]+' '+str(path[3][i]))
            return res
        if state in graph: 
            for nextNode in graph[state]:
                if nextNode[0] not in visited or visited[nextNode[0]] > path[3][-1]+nextNode[1]:
                    heu, cost = heus[nextNode[0]], path[3][-1] + nextNode[1]
                    time += 1
                    queue.put((cost+heu, time, path[2]+[nextNode[0]], path[3]+[cost]))
    return ["No path is detected!"]
    
        
            
if __name__ == "__main__": main()