def mean(l):
    return sum(l, 0.)/len(l)

def centrality_mean(G, v):
    dists = {}
    next = [v]

    cdist = 0
    while next:
        nnext = set()
        for n in next:
            if n not in dists:
                dists[n] = cdist
                for neighbour in G[n].keys():
                    if neighbour not in dists:
                        nnext.add(neighbour)
        cdist += 1
        next = nnext

    return mean(dists.values())

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

def make_graph(fn):
    actors = set()
    lines = open(fn).readlines()

    G = {}
    for line in lines:
        act, mov, year = [a.strip() for a in line.split("\t")]
        make_link(G, act, (mov,year))
        actors.add(act)

    dists = {}

    count = 0
    for a in sorted(actors)[:]:
        dists[a] = centrality_mean(G, a)
        count +=1
        print "%d %s: %f" % (count, a, dists[a])        

    rv = sorted([(v,k) for k,v in dists.iteritems()])
    for i in range(20):
        print "%i: %s, %f" % (i+1, rv[i][1], rv[i][0])


make_graph("imdb-1.tsv")
