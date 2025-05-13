import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import random

# Create graph
G = nx.Graph()

# Define nodes
nodes = ["pol", "pol2", "pol3", "pol4", "pol5", "pol12", "pol6", "pol7", "pol8", "pol9", "pol10", "pol11",
         "hos", "hos2", "hos3", "hos4", "hos5", "hos6", "hos7", "hos8", "hos9", "hos10", "hos11", "hos12",
         "acc", "acc2", "acc3", "acc4", "acc5", "acc6", "polhos", "polhos2", "polhos3", "polhos4", "polhos5", "hosacc"]

# Define edges with weights
edges = [("acc", "acc2", 3), ("acc2", "pol", 2), ("acc2", "pol2", 3), ("acc2", "hos", 2), ("pol2", "pol3", 3), 
         ("pol2", "polhos", 2), ("pol2", "polhos2", 3), ("pol3", "polhos3", 2), ("polhos3", "hos3", 2), ("polhos", "pol4", 2), 
         ("hos", "hos2", 2), ("hos2", "pol8", 2), ("polhos2", "pol5", 2), ("polhos2", "hos5", 2), ("polhos2", "hos4", 3), 
         ("pol5", "pol7", 2), ("pol7", "polhos4", 3), ("pol7", "acc3", 3), ("acc3", "pol6", 2), ("pol6", "hos4", 3), 
         ("hos4", "hos5", 2), ("hos5", "pol12", 2), ("pol9", "hos9", 3), ("pol6", "hos6", 3), ("hos6", "pol12", 2), ("pol8", "pol7", 3), 
         ("pol8", "pol9", 2), ("pol8", "acc4", 2), ("pol8", "hosacc", 2), ("hosacc", "hos10", 3), ("pol8", "hos9", 3), 
         ("pol8", "polhos5", 3), ("polhos5", "hos8", 2), ("polhos5", "pol10", 2), ("hos9", "hos10", 2), ("hos10", "acc5", 2), 
         ("acc5", "hos12", 2), ("hos12", "pol11", 2), ("pol11", "acc6", 2), ("hos11", "hos10", 3), ("hos11", "hosacc", 3),
         ("pol9", "hos7", 2), ("pol9", "polhos5", 3), ("hos9", "polhos5", 3), ("polhos", "polhos2", 3), ("polhos", "pol3", 2), 
         ("polhos2", "pol3", 2)] 

# Add nodes and weighted edges
G.add_nodes_from(nodes)
G.add_weighted_edges_from(edges)

# Random traffic congestion: increase weights on some edges
for u, v, w in list(G.edges(data='weight')):
    if random.random() < 0.3:  # 30% chance of congestion
        extra = random.randint(1, 5)
        G[u][v]['weight'] += extra
        print(f"Traffic: Increased weight of edge ({u}, {v}) by {extra}")

# Update edge labels to reflect new weights
updated_edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}

# Graph layout
pos = nx.spring_layout(G, seed=42)

# Generalized path finder (hospital or police)
def find_nearest_target(start_node, prefix):
    target_nodes = [n for n in G.nodes if n.startswith(prefix)]
    paths = {}

    for target in target_nodes:
        try:
            path = nx.shortest_path(G, source=start_node, target=target, weight='weight')
            length = nx.shortest_path_length(G, source=start_node, target=target, weight='weight')
            paths[target] = (length, path)
        except nx.NetworkXNoPath:
            continue

    if paths:
        nearest = min(paths, key=lambda k: paths[k][0])
        return nearest, paths[nearest][0], paths[nearest][1]
    else:
        return None, None, None

# Animation function
def animate_path(path, start_node, end_node, dist, label, color):
    fig, ax = plt.subplots(figsize=(10, 8))

    # Node color logic
    color_map = []
    for node in G.nodes:
        if node.startswith('acc'):
            color_map.append('red')
        elif node.startswith('hos'):
            color_map.append('green')
        elif node.startswith('pol'):
            color_map.append('blue')
        else:
            color_map.append('gray')

    # Draw static elements
    nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=1000, ax=ax)
    nx.draw_networkx_labels(G, pos, font_weight='bold', ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, edge_color='gray', alpha=0.3, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=updated_edge_labels, ax=ax)

    # Prepare path edges and moving dot coordinates
    path_edges = list(zip(path, path[1:]))
    animated_edges = []
    dot, = ax.plot([], [], 'o', color=color, markersize=12)

    def update(num):
        if num < len(path_edges):
            edge = path_edges[num]
            animated_edges.append(edge)
            nx.draw_networkx_edges(G, pos, edgelist=animated_edges, edge_color=color, width=3, ax=ax)
            # Move dot along the edge
            x1, y1 = pos[edge[0]]
            x2, y2 = pos[edge[1]]
            x = x1 + (x2 - x1) * 0.5
            y = y1 + (y2 - y1) * 0.5
            dot.set_data(x, y)

    ani = animation.FuncAnimation(fig, update, frames=len(path_edges)+1, interval=700, repeat=False)
    plt.title(f"{label}: {start_node} ➝ {end_node} (Distance: {dist})")
    plt.show()

# Process all accident nodes
accident_nodes = [node for node in G.nodes if node.startswith("acc")]

for acc in accident_nodes:
    # Hospital path
    hos_name, hos_dist, hos_path = find_nearest_target(acc, "hos")
    if hos_path:
        print(f"[Hospital] {acc} ➝ {hos_name} | Distance: {hos_dist} | Path: {' -> '.join(hos_path)}")
        animate_path(hos_path, acc, hos_name, hos_dist, "To Hospital", "red")
    
    # Police path
    pol_name, pol_dist, pol_path = find_nearest_target(acc, "pol")
    if pol_path:
        print(f"[Police] {acc} ➝ {pol_name} | Distance: {pol_dist} | Path: {' -> '.join(pol_path)}")
        animate_path(pol_path, acc, pol_name, pol_dist, "To Police", "blue")
