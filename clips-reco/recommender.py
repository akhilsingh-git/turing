import pickle
from collections import defaultdict
from bipart_model import user_nodes, stream_nodes
import networkx as nx

G = pickle.load(open("network.sav", 'rb'))

def get_nodes_from_partition(G, partition):
    nodes = []
    for n in G.nodes():
        if G.nodes[n]['bipartite'] == partition:
            nodes.append(n)
    
    return nodes

def shared_partition_nodes(node1, node2):
    assert G.nodes[node1]['bipartite'] == G.nodes[node2]['bipartite']
    nbrs1 = G.neighbors(node1)
    nbrs2 = G.neighbors(node2)
    overlap = set(nbrs1).intersection(nbrs2)
    return overlap

def user_similarity( user1, user2):
    assert G.nodes[user1]['bipartite'] == 'Users'
    assert G.nodes[user2]['bipartite'] == 'Users'
    shared_nodes = shared_partition_nodes(user1, user2)
    return len(shared_nodes) / len(stream_nodes)

def most_similar_users(user):
    assert G.nodes[user]['bipartite'] == 'Users'
    user_node = set(user_nodes)
    user_node.remove(user)
    similarities = defaultdict(list)
    for n in user_node:
        similarity = user_similarity(user, n)
        similarities[similarity].append(n)
    max_similarity = max(similarities.keys())
    return similarities[max_similarity]

def recommend_video(from_user):
    from_streamers = set(G.neighbors(from_user))
    video_id = set()
    for to_user in most_similar_users(from_user):
        to_streamers = set(G.neighbors(to_user))
        video_id.update(from_streamers.difference(to_streamers))
    return(list(video_id))
