#
# The code below uses a linear
# scan to find the unfinished node
# with the smallest distance from
# the source.
#
# Modify it to use a heap instead
# 

def heappopmin(heap, location):
    val = heap[0]
    new_top = heap.pop()
    #location[val] = None
    del location[val]
    if len(heap) == 0:
        return val
    location[new_top] = 0
    heap[0] = new_top
    down_heapify(heap, 0, location)
    return val

def parent(i): 
    return (i-1)/2
def left_child(i): 
    return 2*i+1
def right_child(i): 
    return 2*i+2
def is_leaf(L,i): 
    return (left_child(i) >= len(L)) and (right_child(i) >= len(L))
def one_child(L,i): 
    return (left_child(i) < len(L)) and (right_child(i) >= len(L))

def swap(heap, old, new, location):
    location[heap[old]] = new
    location[heap[new]] = old
    (heap[old], heap[new]) = (heap[new], heap[old])
    

def down_heapify(heap, i, location):
    while True:
        l = left_child(i)
        r = right_child(i)

        if l >= len(heap): 
            break

        v = heap[i][0]
        lv = heap[l][0]
            
        if r == len(heap):
            if v > lv:                
                swap(heap, i, l, location)
            break

        rv = heap[r][0]
        if min(lv, rv) >= v: 
            break

        if lv < rv:
            swap(heap, i, l, location)
            i = l
        else:
            swap(heap, i, r, location)
            i = r

def up_heapify(heap, i, location):
    # If i is root, all is well
    while i > 0: 
        # check heap property
        p = (i - 1) / 2
        if heap[i][0] < heap[p][0]:
            swap(heap, i, p, location)
            i = p
        else:
            break

def insert_heap(heap, v, location):
    heap.append(v)
    location[v] = len(heap) - 1
    up_heapify(heap, len(heap) - 1, location)
    return location[v]

def decrease_val(heap, location, old_val, new_val):
    i = location[old_val]
    heap[i] = new_val
    #location[old_val] = None
    del location[old_val]
    location[new_val] = i
    up_heapify(heap, i, location)
    return location[new_val]

def dijkstra(G, a):
    # Distance to the input node is zero
    first_entry = (0, a)
    heap = [first_entry]
    # location keeps track of items in the heap
    # so that we can update their value later
    location = {first_entry:0}
    # dist_so_far is kind of our 'frontier'
    # it keeps track of the nodes that we've seen so far
    # but aren't sure if we've found the shortest distance
    dist_so_far = {a:first_entry} 
    # find_dist keeps track of the nodes that we've seen
    # and know that is the shortest distance
    final_dist = {}
    while len(dist_so_far) > 0:
        # grab the minimum value from the heap
        dist, node = heappopmin(heap, location)
        # lock it down!
        final_dist[node] = dist
        del dist_so_far[node]

        # examine the neighbors
        for x in G[node]:
            if x in final_dist:
                # skip the ones we already have shortest
                # distances for
                continue

            new_dist = G[node][x] + final_dist[node]
            new_entry = (new_dist, x)
            if x not in dist_so_far:
                # add to the heap
                insert_heap(heap, new_entry, location)
                dist_so_far[x] = new_entry
            elif new_entry < dist_so_far[x]:
                # we found a better way to this node, update heap
                decrease_val(heap, location, dist_so_far[x], new_entry)
                dist_so_far[x] = new_entry
    return final_dist

############
# 
# Test

def make_link(G, node1, node2, w):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 0
    (G[node1])[node2] += w
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 0
    (G[node2])[node1] += w
    return G


def test():
    # shortcuts
    (a,b,c,d,e,f,g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    triples = ((a,c,3),(c,b,10),(a,b,15),(d,b,9),(a,d,4),(d,f,7),(d,e,3), 
               (e,g,1),(e,f,5),(f,g,2),(b,f,1))
    G = {}
    for (i,j,k) in triples:
        make_link(G, i, j, k)

    dist = dijkstra(G, a)
    #assert dist[g] == 8 #(a -> d -> e -> g)
    #assert dist[b] == 11 #(a -> d -> e -> g -> f -> b)
    print dist[g]
    print dist[b]

#test()
