# Use your code from earlier to change the Marvel graph
# to only have characters as nodes. Use 1.0/count as the 
# weight, where count is the number of comic books each 
# character appeared in together
#
# For each character in this list
# 'SPIDER-MAN/PETER PAR'
# 'GREEN GOBLIN/NORMAN '
# 'WOLVERINE/LOGAN '
# 'PROFESSOR X/CHARLES '
# 'CAPTAIN AMERICA'
# search your weighted graph. Find all the characters 
# where the shortest path by weight to that character 
# is different by weight from the shortest path measured 
# by counting the number of hops.
# 

import csv

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 0
    (G[node1])[node2] += 1
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 0
    (G[node2])[node1] += 1
    return G

tsv = csv.reader(open("uniq_edges.tsv"), delimiter='\t')

marvelG = {}
characters = set()
for (char, comic) in tsv: 
    if char not in characters: 
        characters.add(char)
    make_link(marvelG, char, comic)
    
charG = {}
for char1 in characters:
    for book in marvelG[char1]:
        for char2 in marvelG[book]:
            # don't want to double count
            # so make this check
            if char1 < char2:
                make_link(charG, char1, char2)

for char1 in charG:
    char1 = charG[char1]
    for char2 in char1:
        char1[char2] = 1.0 / char1[char2]

################        
# BFS - HOPS
from collections import deque

def bfs(G, node):
    final_dist = {node:(0, node, None)}
    open_list = deque([node])
    while len(open_list) > 0:
        node = open_list.popleft()
        dist, _, _ = final_dist[node]
        for neighbor in G[node]:
            if neighbor in final_dist:
                continue
            final_dist[neighbor] = (dist + 1, neighbor, node)
            open_list.append(neighbor)
    return final_dist

################
# dijkstras
from hw501 import *

def add_dist(dista, tupleb):
    # adds dista to the distance of tupleb
    # and increments the hop-count of tupleb
    return (dista + tupleb[0], 1 + tupleb[1])

def dijkstra(graph, node):
    first_entry = ((0, 0), node, None) #distance, node, parent/previous
    heap = [first_entry]
    location = {first_entry : 0} # index in heap
    
    dist_so_far = {node: first_entry} # node, short_path_so_far
    final_dist = {}
    while len(dist_so_far)>0:
        w = heappopmin(heap, location)
        node = w[1]
        dist = w[0]
        del dist_so_far[node]
        final_dist[node] = w
        
        for x in graph[node]:
            if x in final_dist:
                continue
            
            new_dist = add_dist(graph[node][x], dist)
            new_entry = (new_dist, x, node)
            if x not in dist_so_far:
                insert_heap(heap, new_entry, location)
                dist_so_far[x] = new_entry
            elif new_entry[0] < dist_so_far[x][0]:
                decrease_val(heap, location, dist_so_far[x], new_entry)
                dist_so_far[x] = new_entry 
    return final_dist


# given a `dist` object (a mapping of a node to the shortest distance
# to that node and its parent) and a `target` node, return the path
# needed to get to the target
def find_path(dist, target):
    node = target
    path = [target]
    while True:
        # `dist` object: distance, node, parent/previous
        prev = dist[node][2]
        if prev is None:
            return path
        path.append(prev)
        node = prev

# a list to store my answers in
answers = [] #store a tuple ((char1, char2), (char_path, hop_dist))

# the characters that the problem asks us to look at
chars = ['SPIDER-MAN/PETER PAR',
         'GREEN GOBLIN/NORMAN ',
         'WOLVERINE/LOGAN ',
         'PROFESSOR X/CHARLES ', 
         'CAPTAIN AMERICA']

for char1 in chars:
    # calculate the distance to each other character
    char_dist = dijkstra(charG, char1)
    # and calculate the hops required
    hop_dist = bfs(charG, char1)

    for char2 in char_dist:
        if char1 == char2:
            continue
        char_path = find_path(char_dist, char2)
        hop_path = find_path(hop_dist, char2)
        # if the weighted path is longer then the hop path, we need
        # to save it
        if len(char_path) > len(hop_path):
            answers.append(((char1, char2), (char_path, hop_path)))

# and now we print out the answer
print len(answers)