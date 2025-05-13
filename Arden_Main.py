import math
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Emergency vehicle speed (in km/h)
speed_kmh = 60  

# Function to calculate response time (in minutes)
def calculate_response_time(distance, speed=speed_kmh):
    return (distance / speed) * 60  # Convert to minutes

# Define graph
G = nx.Graph()

# Nodes categorized
hospitals = ["hos", "hos2", "hos3", "hos4", "hos5", "hos6", "hos7", "hos8", "hos9", "hos10", "hos11", "hos12", "polhos", "polhos2", "polhos3", "polhos4", "polhos5", "hosacc"]
police_stations = ["pol", "pol2", "pol3", "pol4", "pol5", "pol12", "pol6", "pol7", "pol8", "pol9", "pol10", "pol11", "polhos", "polhos2", "polhos3", "polhos4", "polhos5"]
accidents = ["acc", "acc2", "acc3", "acc4", "acc5", "acc6", "hosacc"]

# Define edges (without weights)
edges = [("acc", "acc2"), ("acc2", "pol"), ("acc2", "pol2"), ("acc2", "hos"), ("pol2", "pol3"), 
         ("pol2", "polhos"), ("pol2", "polhos2"), ("pol3", "polhos3"), ("polhos3", "hos3"), ("polhos", "pol4"), 
         ("hos", "hos2"), ("hos2", "pol8"), ("polhos2", "pol5"), ("polhos2", "hos5"), ("polhos2", "hos4"), 
         ("pol5", "pol7"), ("pol7", "polhos4"), ("pol7", "acc3"), ("acc3", "pol6"), ("pol6", "hos4"), 
         ("hos4", "hos5"), ("hos5", "pol12"), ("pol9", "hos9"), ("pol6", "hos6"), ("hos6", "pol12"), ("pol8", "pol7"), 
         ("pol8", "pol9"), ("pol8", "acc4"), ("pol8", "hosacc"), ("hosacc", "hos10"), ("pol8", "hos9"), 
         ("pol8", "polhos5"), ("polhos5", "hos8"), ("polhos5", "pol10"), ("hos9", "hos10"), ("hos10", "acc5"), 
         ("acc5", "hos12"), ("hos12", "pol11"), ("pol11", "acc6"), ("hos11", "hos10"), ("hos11", "hosacc"),
         ("pol9", "hos7"), ("pol9", "polhos5"), ("hos9", "polhos5"), ("polhos", "polhos2"), ("polhos", "pol3"), 
         ("polhos2", "pol3") ] 

# Add nodes and edges to the graph
G.add_nodes_from(hospitals + police_stations + accidents)
G.add_edges_from(edges)

# BFS function to find shortest unweighted path
def bfs_shortest_path(graph, start, targets):
    queue = deque([(start, 0)])
    visited = set()
    shortest_paths = {}
    
    while queue:
        node, distance = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        if node in targets:
            shortest_paths[node] = distance
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                queue.append((neighbor, distance + 1))
    return shortest_paths

# DFS function to find paths
def dfs_paths(graph, start, targets, visited=None, distance=0):
    if visited is None:
        visited = set()
    visited.add(start)
    paths = {}
    if start in targets:
        paths[start] = distance
    for neighbor in graph.neighbors(start):
        if neighbor not in visited:
            paths.update(dfs_paths(graph, neighbor, targets, visited.copy(), distance + 1))
    return paths

# Merge Sort function
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        merge_sort(left)
        merge_sort(right)
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i][1] < right[j][1]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

# User inputs accident location
accident_input = input("Enter accident node (e.g., acc2): ").strip()

if accident_input in accidents:
    hospital_times_bfs = bfs_shortest_path(G, accident_input, hospitals)
    police_times_bfs = bfs_shortest_path(G, accident_input, police_stations)
    
    hospital_times_dfs = dfs_paths(G, accident_input, hospitals)
    police_times_dfs = dfs_paths(G, accident_input, police_stations)

    hospital_list_bfs = [(h, calculate_response_time(t)) for h, t in hospital_times_bfs.items()]
    police_list_bfs = [(p, calculate_response_time(t)) for p, t in police_times_bfs.items()]
    
    merge_sort(hospital_list_bfs)
    merge_sort(police_list_bfs)
    
    print("\n🚑 Hospital Response Times (BFS Sorted):")
    for h, t in hospital_list_bfs:
        print(f"{h} - {t:.2f} min")
    
    print("\n🚔 Police Station Response Times (BFS Sorted):")
    for p, t in police_list_bfs:
        print(f"{p} - {t:.2f} min")
    
    print("\nNearest Rescue Centers (BFS):")
    if hospital_list_bfs:
        print(f"🚑 Nearest Hospital: {hospital_list_bfs[0][0]} - Response Time: {hospital_list_bfs[0][1]:.2f} min")
    else:
        print("No hospital found.")
    
    if police_list_bfs:
        print(f"🚔 Nearest Police Station: {police_list_bfs[0][0]} - Response Time: {police_list_bfs[0][1]:.2f} min")
    else:
        print("No police station found.")
else:
    print("Invalid accident location.")

pos = nx.spring_layout(G)  # Positioning layout
nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=800)

# Highlight hospitals, police stations, and accident nodes
node_colors = {
    **{node: "red" for node in hospitals},  # Hospitals - Red
    **{node: "blue" for node in police_stations},  # Police Stations - Blue
    **{node: "orange" for node in accidents}  # Accidents - Orange
}

# Apply colors
colors = [node_colors.get(node, "lightblue") for node in G.nodes()]
nx.draw(G, pos, node_color=colors, with_labels=True, edge_color="gray", node_size=1000)

plt.show()