import math

def edge_d(a, b):
    '''
    Compute the edit distance between two words using dynamic programming
    Input: Word a, Word b
    Output: Graph of distances. A 2-dimensional array
    '''
    
    # Create graph nxm
    n = len(a)
    m = len(b)
    graph = []
    
    for i in range(n):
        graph.append([0] * m)
    
    # Call helper with graph
    return helper(a, b, graph)

def helper(a, b, graph):
    
    # Solve smallest subproblem 
    n = len(a)
    m = len(b)
    
    for i in range(n):
        graph[i][0] = i
    
    for i in range(m):
        graph[0][i] = i
        
    # Solve subproblems recursively
    for i in range(1, n):
        for j in range(1, m):
            diff = 1 if a[i] != b[j] else 0
            graph[i][j] = min(graph[i-1][j] + 1, graph[i][j-1] + 1, graph[i-1][j-1] + diff)
    return graph
    
print(edge_d('exopnential', 'polynomial'))