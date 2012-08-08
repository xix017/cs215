# Find Eulerian Tour
#
# Write a function that takes in a graph
# represented as a list of tuples
# and return a list of nodes that
# you would follow on an Eulerian Tour
#
# For example, if the input graph was
# [(1, 2), (2, 3), (3, 1)]
# A possible Eulerian tour would be [1, 2, 3, 1]


def find_eulerian_tour(graph):
    # your code here
    vertex = [edge[0] for edge in graph] + [edge[1] for edge in graph]
    vertex = {}.fromkeys(vertex).keys() 
    ret = None    
    for v in vertex:
        ret = dfs(graph, v, [], [])
        if ret <> None:            
            break
    return ret

def dfs(graph, node, visited, result):
    newresult = result + [node]
    dest = [edge for edge in graph if (edge[0] == node or edge[1] == node) and (edge not in visited)]
    
    if dest == []:        
        if len(visited) == len(graph):
            return newresult
        else:
            return None
    for edge in dest:
        newvisited = visited + [edge]
        if edge[0] == node:            
            tour = dfs(graph, edge[1], newvisited, newresult)
        else:
            tour = dfs(graph, edge[0], newvisited, newresult)
        if tour <> None:
            return tour
    return None
        

graph = [(0, 1), (1, 5), (1, 7), (4, 5), (4, 8), (1, 6), (3, 7), (5, 9), (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]
print find_eulerian_tour(graph)
