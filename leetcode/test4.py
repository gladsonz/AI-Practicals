import math 
tree = {
    'A':['B','C'],
    'B':['D','E'],
    'C':['F','G'],
    'D':[],
    'E':[],
    'F':[],
    'G':[]
}

value = {
    'D':3,
    'E':5,
    'F':2,
    'G':9
}
pruned_nodes = []

def get_all_nodes(node):
    if tree[node]==[]:
        return [node]
    else:
     ans=[node]
    for child in tree[node]:
                ans+=get_all_nodes(child)
    return ans


def alpha_beta(node, alpha , beta , maxi):
    if tree[node]==[]:
        print("Leaf node ",node," value = ",value[node])
        return value[node]
    

    if maxi:
        print("max player ")
        best = -math.inf
        for i, child in enumerate(tree[node]):
            print("Visiting node ",child)
            
            best=max(best, alpha_beta(child, alpha, beta, False))
            alpha = max(alpha, best)
            if beta <= alpha:
                for rem in tree[node][i+1:]:
                    pruned_nodes.extend(get_all_nodes(rem))
                    break

        return best
            
    else: 
        print("min player ")
        best = math.inf
        for i, child in enumerate(tree[node]):
            print("Visiting node ",child)
            best=min(best, alpha_beta(child, alpha, beta, True))
            beta = min(beta, best)
            if beta <= alpha:
                for rem in tree[node][i+1:]:
                    pruned_nodes.extend(get_all_nodes(rem))
                    break
        return best


ans = alpha_beta('A', -math.inf, math.inf, True)

print("\nPruned Nodes:", pruned_nodes)
print("Best Value =", ans)
