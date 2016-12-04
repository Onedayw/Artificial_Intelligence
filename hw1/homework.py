import Queue

def main():
    method, start, end, routes, heuristics = readFile("input.txt")
    if method == "BFS": 
        res = bfs(start, end, routes)
    elif method == "DFS": 
        res = dfs(start, end, routes, start+' 0\n', set(), set(), 1)
    elif method == "UCS": 
        res = ucs(start, end, routes)
    elif method == "A*": 
        res = a_star(start, end, routes, heuristics)
    else: res = ["Invalid method!"]
    f = open("output.txt", 'w')
    f.write(res)
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
    queue, visited, res, count = Queue.Queue(), set(), "", 1
    queue.put((start, start+' 0\n', count))
    while queue:
        path = queue.get()
        state = path[0]
        visited.add(state)
        if state == end:
            return path[1]
        if state in graph:
            for nextState in graph[state]:
                newNode = nextState[0]
                if newNode not in visited:
                    newPath = path[1]+newNode+' '+str(path[2])+'\n'
                    queue.put((nextState[0], newPath, path[2]+1))
    return ["No path is detected!"]
         
    
def dfs(state, end, graph, path, visited, frontier, count):
    visited.add(state)
    if state in graph:
        neighbors = set()
        for nextState in graph[state]:
            newNode = nextState[0]
            if newNode == end:
                return path+end+' '+str(count)+'\n'
            neighbors.add(newNode)
        for nextState in graph[state]:
            newNode = nextState[0]
            if newNode not in visited and newNode not in frontier:
                newPath = path+newNode+' '+str(count)+'\n'
                newFrontier = frontier.union(neighbors)
                p = dfs(newNode, end, graph, newPath, visited, newFrontier, count+1)
                if p: return p
    if not path:
        return ["No path is detected"]
    
    
def ucs(start, end, graph):
    queue, visited, time = Queue.PriorityQueue(), set(), 0
    queue.put((0, time, start+' 0\n', start))
    while queue:
        path = queue.get()
        state = path[3]
        visited.add(state)
        if state == end:
            return path[2]
        if state in graph:
            for nextNode in graph[state]:
                newNode = nextNode[0]
                if newNode not in visited: 
                    cost = path[0] + nextNode[1]
                    time += 1
                    newPath = path[2]+newNode+' '+str(cost)+'\n'
                    queue.put((cost, time, newPath, newNode))
    return ["No path is detected!"]
    
    
def a_star(start, end, graph, heus):
    queue, time, visited = Queue.PriorityQueue(), 0, {}
    queue.put((heus[start], time, start+' 0\n', start, 0))
    while queue:
        path = queue.get()
        state = path[3]
        visited[state] = path[4]
        if state == end:
            return path[2]
        if state in graph: 
            for nextNode in graph[state]:
                newNode = nextNode[0]
                if newNode not in visited or visited[newNode] > path[4]+nextNode[1]:
                    heu, cost = heus[newNode], path[4] + nextNode[1]
                    time += 1
                    newPath = path[2]+newNode+' '+str(cost)+'\n'
                    queue.put((cost+heu, time, newPath, newNode, cost))
    return ["No path is detected!"]
            
    
if __name__ == "__main__": 
    main()