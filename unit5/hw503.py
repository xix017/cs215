#
# Another way of thinking of a path in the Kevin Bacon game 
# is not about finding *short* paths, but by finding paths 
# that don't use obscure movies.  We will give you a 
# list of movies along with their obscureness score.  
#
# For this assignment, we'll approximate obscurity 
# based on the multiplicative inverse of the amount of 
# money the movie made.  Though, its not really important where
# the obscurity score came from.
#
# Use the the imdb-1.tsv and imdb-weights.tsv files to find
# the obscurity of the "least obscure" 
# path from a given actor to another.  
# The obscurity of a path is the maximum obscurity of 
# any of the movies used along the path.
#
# You will have to do the processing in your local environment
# and then copy in your answer.
#
# Hint: A variation of Dijkstra can be used to solve this problem.
#

# Change the 'None' values in this dictionary to be the obscurity score
# of the least obscure path between the two actors
answer = {(u'Boone Junior, Mark', u'Del Toro, Benicio'): None,
          (u'Braine, Richard', u'Coogan, Will'): None,
          (u'Byrne, Michael (I)', u'Quinn, Al (I)'): None,
          (u'Cartwright, Veronica', u'Edelstein, Lisa'): None,
          (u'Curry, Jon (II)', u'Wise, Ray (I)'): None,
          (u'Di Benedetto, John', u'Hallgrey, Johnathan'): None,
          (u'Hochendoner, Jeff', u'Cross, Kendall'): None,
          (u'Izquierdo, Ty', u'Kimball, Donna'): None,
          (u'Jace, Michael', u'Snell, Don'): None,
          (u'James, Charity', u'Tuerpe, Paul'): None,
          (u'Kay, Dominic Scott', u'Cathey, Reg E.'): None,
          (u'McCabe, Richard', u'Washington, Denzel'): None,
          (u'Reid, Kevin (I)', u'Affleck, Rab'): None,
          (u'Reid, R.D.', u'Boston, David (IV)'): None,
          (u'Restivo, Steve', u'Preston, Carrie (I)'): None,
          (u'Rodriguez, Ramon (II)', u'Mulrooney, Kelsey'): None,
          (u'Rooker, Michael (I)', u'Grady, Kevin (I)'): None,
          (u'Ruscoe, Alan', u'Thornton, Cooper'): None,
          (u'Sloan, Tina', u'Dever, James D.'): None,
          (u'Wasserman, Jerry', u'Sizemore, Tom'): None}

# Here are some test cases.
# For example, the obscurity score of the least obscure path
# between 'Ali, Tony' and 'Allen, Woody' is 0.5657
test = {(u'Ali, Tony', u'Allen, Woody'): 0.5657,
        (u'Auberjonois, Rene', u'MacInnes, Angus'): 0.0814,
        (u'Avery, Shondrella', u'Dorsey, Kimberly (I)'): 0.7837,
        (u'Bollo, Lou', u'Jeremy, Ron'): 0.4763,
        (u'Byrne, P.J.', u'Clarke, Larry'): 0.109,
        (u'Couturier, Sandra-Jessica', u'Jean-Louis, Jimmy'): 0.3649,
        (u'Crawford, Eve (I)', u'Cutler, Tom'): 0.2052,
        (u'Flemyng, Jason', u'Newman, Laraine'): 0.139,
        (u'French, Dawn', u'Smallwood, Tucker'): 0.2979,
        (u'Gunton, Bob', u'Nagra, Joti'): 0.2136,
        (u'Hoffman, Jake (I)', u'Shook, Carol'): 0.6073,
        (u'Kamiki, Ry\xfbnosuke', u'Thor, Cameron'): 0.3644,
        (u'Roache, Linus', u'Dreyfuss, Richard'): 0.6731,
        (u'Sanchez, Phillip (I)', u'Wiest, Dianne'): 0.5083,
        (u'Sheppard, William Morgan', u'Crook, Mackenzie'): 0.0849,
        (u'Stan, Sebastian', u'Malahide, Patrick'): 0.2857,
        (u'Tessiero, Michael A.', u'Molen, Gerald R.'): 0.2056,
        (u'Thomas, Ken (I)', u'Bell, Jamie (I)'): 0.3941,
        (u'Thompson, Sophie (I)', u'Foley, Dave (I)'): 0.1095,
        (u'Tzur, Mira', u'Heston, Charlton'): 0.3642}


########################################
def val(pair): return pair[0]
def id(pair): return pair[1]
def get_parent(pair): return pair[2]
# modified dijkstra to minimize
# the obsucurity instead of distance
import heapq
def dijkstra_min(G,v):
    first_entry = [0, v, None]
    heap = [first_entry]
    obs_so_far = {v:first_entry}
    final_obs = {}
    while len(final_obs) < len(G):
        # find the closest un-explored node
        while True:        
            if len(heap) == 0:
                return final_obs
            w = heapq.heappop(heap)
            node = id(w)
            obscurity = val(w)
            parent = get_parent(w)
            if node != 'REMOVED':
                del obs_so_far[node]
                break        
                    
        final_obs[node] = [obscurity, node, parent]
        
        for x in G[node]:
            if x not in final_obs:
                new_obscurity = max(obscurity, G[node][x])
                new_entry = [new_obscurity, x, node]
                
                if x not in obs_so_far:
                    obs_so_far[x] = new_entry
                    heapq.heappush(heap, new_entry)
                elif new_obscurity < val(obs_so_far[x]):
                    obs_so_far[x][1] = "REMOVED"
                    obs_so_far[x] = new_entry
                    heapq.heappush(heap, new_entry)
    return final_obs


# returns the obscurity score of the 
# least obscure score between two actors
def least_obscure(actor1, actor2):
    all_obs = dijkstra_min(actorG, actor1)    
    ret = all_obs.get(actor2)
    if ret!=None:    
        return ret[0]
    else:
        return None

# this might be considered an abuse of defaultdict
#
# create a defaultdict, where the factory creates another
# defaultdict.  The factor of this defaultdict creates entries
# with a MAX_WEIGHT value.
# This has the effect of giving every character to character mapping
# a default value of MAX_WEIGHT
from collections import defaultdict
MAX_WEIGHT = 1000
def new_entry():
    return defaultdict(lambda:MAX_WEIGHT)

def make_link(G, n1, n2, weight):
    if weight < G[n1][n2]:        
        G[n1][n2] = weight
        G[n2][n1] = weight

def make_link__(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

import csv
import string

actors = set()
G = {}
tsv = csv.reader(open("imdb-1.tsv"), delimiter='\t')
for (act, mov, year) in tsv:
    make_link__(G, mov, act)
    actors.add(act)

obscurity = {}
tsv = csv.reader(open("imdb-weight.tsv"), delimiter='\t')
for (mov, year, obs) in tsv:
    obscurity[mov] = string.atof(obs)


actorG = defaultdict(new_entry)

done = set()
for actor1 in actors:
    done.clear()
    done.add(actor1)
    for movie in G[actor1]:
        obsc = obscurity[movie]
        for actor2 in G[movie]:
            if actor2 not in done:
                make_link(actorG, actor1, actor2, obsc)

#print actorG['McClure, Marc (I)']['Dean, Loren']

for entry in answer:
    print entry
    answer[entry] = least_obscure(entry[0], entry[1])   
    
print answer
