import igraph
from igraph import Graph, plot
import numpy as np

from api import get_friends

def get_network(users_ids, as_edgelist=True):
    vertices = set()
    graph = {}

    for user_id in users_ids:
        vertices.add(user_id)

        friends = get_friends(user_id)

        if not 'error' in friends:
            for user_friend in friends['response']['items']:
                vertices.add(user_friend)

    vertices = [vert for vert in vertices]

    if as_edgelist:
        edges = []

        for user_id in vertices:
            friends = get_friends(user_id)

            if not 'error' in friends:
                for user_friend in friends['response']['items']:
                    if user_friend in vertices:
                        edges.append((user_id, user_friend))

        return vertices, edges

    else:
        matrix = [[0 for _ in range(len(vertices))] for _ in range(len(vertices))]

        for user_id in vertices:
            friends = get_friends(user_id)

            if not 'error' in friends:
                for user_friend in friends['response']['items']:
                    if user_friend in vertices:
                        matrix[vertices.index(user_id)][vertices.index(user_friend)] = 1

        return vertices, matrix

def plot_graph(graph):
    edges = graph.get_edgelist()
    vertices = list(set(vert[0] for vert in edges))

    N = len(vertices)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=1000,
        area=N**3,
        repulserad=N**3)

    g.simplify(multiple=True, loops=True)
    communities = g.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()

    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)

    plot(g, **visual_style)
