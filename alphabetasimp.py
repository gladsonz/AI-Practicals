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
# Store all pruned nodes
pruned_nodes = []

# Get all leaf nodes in a pruned subtree
def get_pruned(node):
    if tree[node] == []:
        return [node]

    ans = []
    for child in tree[node]:
        ans += get_pruned(child)
    return ans


def alphabeta(node, alpha, beta, maxi):

    if tree[node] == []:
        print(node, "=", value[node])
        return value[node]

    if maxi:

        best = -math.inf

        for i, child in enumerate(tree[node]):

            best = max(best, alphabeta(child, alpha, beta, False))
            alpha = max(alpha, best)

            if alpha >= beta:

                for rem in tree[node][i+1:]:
                    pruned_nodes.extend(get_pruned(rem))

                break

        return best

    else:

        best = math.inf

        for i, child in enumerate(tree[node]):

            best = min(best, alphabeta(child, alpha, beta, True))
            beta = min(beta, best)

            if alpha >= beta:

                for rem in tree[node][i+1:]:
                    pruned_nodes.extend(get_pruned(rem))

                break

        return best


ans = alphabeta('A', -math.inf, math.inf, True)

print("\nPruned Nodes:", pruned_nodes)
print("Best Value =", ans)