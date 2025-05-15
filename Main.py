import matplotlib.pyplot as plt
import networkx as nx

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
         ("polhos2", "pol3", 2) ] 

# Add nodes and weighted edges
G.add_nodes_from(nodes)
G.add_weighted_edges_from(edges)

# Function to find the nearest hospital from a given accident node
def find_nearest_hospital(start_accident):
    # Get all hospital nodes (nodes that start with "hos")
    hospital_nodes = [node for node in G.nodes if node.startswith("hos")]
    
    # Find shortest paths to all hospital nodes
    shortest_paths = {}
    for hospital in hospital_nodes:
        try:
            path_length = nx.shortest_path_length(G, source=start_accident, target=hospital, weight='weight')
            shortest_paths[hospital] = path_length
        except nx.NetworkXNoPath:
            pass  # If no path exists, skip this hospital
    
    # Sort hospitals by shortest path length
    if shortest_paths:
        nearest_hospital = min(shortest_paths, key=shortest_paths.get)
        print(f"Nearest hospital to {start_accident} is {nearest_hospital} with distance {shortest_paths[nearest_hospital]}")
        return nearest_hospital, shortest_paths[nearest_hospital]
    else:
        print(f"No hospital found for {start_accident}")
        return None, None

# Example: Find the nearest hospital from "acc2"
find_nearest_hospital("acc2")

# Draw the graph
pos = nx.spring_layout(G)  # Positioning layout
nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='lightblue', edge_color='gray', node_size=1000)

# Draw edge labels (weights)
edge_labels = {(u, v): w for u, v, w in edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()
    


# def simulate_phone_gui():
#     def add_digit(digit):
#         current = phone_var.get()
#         phone_var.set(current + digit)

#     def clear_number():
#         phone_var.set("")

#     def handle_call():
#         number = phone_var.get()
#         if number == "911":
#             root.withdraw()
#             show_options_window()
#         else:
#             messagebox.showerror("Invalid", "Please dial 911 to proceed.")

#     root = tk.Tk()
#     root.title("Emergency Dialer")

#     phone_var = tk.StringVar()
#     display = ttk.Label(root, textvariable=phone_var, font=("Arial", 24), background="white", anchor="center")
#     display.pack(padx=10, pady=10, fill='x')

#     btn_frame = ttk.Frame(root)
#     btn_frame.pack()

#     # Create number buttons (1-9)
#     for i in range(1, 10):
#         btn = ttk.Button(btn_frame, text=str(i), command=lambda d=str(i): add_digit(d), width=5)
#         btn.grid(row=(i - 1) // 3, column=(i - 1) % 3, padx=5, pady=5)

#     # Row for Clear, 0, and Call buttons
#     ttk.Button(btn_frame, text="Clear", command=clear_number, width=5).grid(row=3, column=0, padx=5, pady=5)
#     ttk.Button(btn_frame, text="0", command=lambda: add_digit("0"), width=5).grid(row=3, column=1, padx=5, pady=5)
#     ttk.Button(btn_frame, text="Call", command=handle_call, width=5).grid(row=3, column=2, padx=5, pady=5)

#     root.mainloop()

# # Zoom in the accident node
# if start_node in pos:
#         x, y = pos[start_node]
#         zoom_range = 0.2  # You can adjust this value to zoom more or less
#         ax.set_xlim(x - zoom_range, x + zoom_range)
#         ax.set_ylim(y - zoom_range, y + zoom_range)