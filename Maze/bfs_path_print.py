def print_bfs_path(childToParentMapping, goalCell):
    childToParentMapping = {(1, 0): {(0, 0)}, (0, 1): {(0, 0)}, (2, 0): {(1, 0)}, (2, 1): {(2, 0)}, (3, 1): {(2, 1)}, (2, 2): {(2, 1)}, (2, 3): {(2, 2)}, (3, 3): {(2, 3)}}
    goalCell = (3,3)
    curr = goalCell
    path = []
    path.append(goalCell)
    while curr != (0,0):
        val = childToParentMapping[curr]
        curr = list(val)[0]
        path.append(curr)
    return path

print(print_bfs_path('a', 'b'))
