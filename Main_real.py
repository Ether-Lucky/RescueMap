import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.patches import Wedge, Circle

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

# Graph layout
pos = nx.spring_layout(G, seed=42, k=0.7, iterations=100)


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

def draw_custom_nodes(ax, pos, G):
    radius = 0.03  # consistent radius for all nodes

    for node in G.nodes:
        x, y = pos[node]
        if node == "hosacc":
            wedge1 = Wedge((x, y), radius, 0, 180, facecolor='red', edgecolor='black')
            wedge2 = Wedge((x, y), radius, 180, 360, facecolor='green', edgecolor='black')
            ax.add_patch(wedge1)
            ax.add_patch(wedge2)
        elif node.startswith("polhos"):
            wedge1 = Wedge((x, y), radius, 0, 180, facecolor='blue', edgecolor='black')
            wedge2 = Wedge((x, y), radius, 180, 360, facecolor='green', edgecolor='black')
            ax.add_patch(wedge1)
            ax.add_patch(wedge2)
        else:
            if node.startswith("acc"):
                color = 'red'
            elif node.startswith("hos"):
                color = 'green'
            elif node.startswith("pol"):
                color = 'blue'
            else:
                color = 'gray'
            circle = Circle((x, y), radius, facecolor=color, edgecolor='black')
            ax.add_patch(circle)

def animate_path(path, start_node, end_node, dist, label, color):
    fig, ax = plt.subplots(figsize=(10, 8))

    # Draw all edges faintly
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, edge_color='gray', alpha=0.3, ax=ax)
    # Draw edge labels
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): w for u, v, w in edges}, ax=ax)
    # Draw custom nodes with consistent sizes and colors
    draw_custom_nodes(ax, pos, G)
    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_weight='bold', ax=ax)

    path_edges = list(zip(path, path[1:]))
    animated_edges = []

    def update(num):
        if num < len(path_edges):
            animated_edges.append(path_edges[num])
            nx.draw_networkx_edges(G, pos, edgelist=animated_edges, edge_color=color, width=3, ax=ax)

    ani = animation.FuncAnimation(fig, update, frames=len(path_edges)+1, interval=700, repeat=False)
    plt.title(f"{label}: {start_node} ➔ {end_node} (Distance: {dist})")

    # Zoom in the accident node
    if start_node in pos and end_node in pos:
        x1, y1 = pos[start_node]
        x2, y2 = pos[end_node]
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        zoom_range = 0.4  # Adjust zoom level here
        ax.set_xlim(mid_x - zoom_range, mid_x + zoom_range)
        ax.set_ylim(mid_y - zoom_range, mid_y + zoom_range)

    plt.show()

# Tkinter GUI
accident_nodes = [node for node in G.nodes if node.startswith("acc")] + ["hosacc"]

def show_options_window():
    def process_selection():
        selected_acc = acc_var.get()
        severity = severity_var.get()

        if not selected_acc:
            messagebox.showerror("Error", "Please select an accident node.")
            return

        if severity == "major":
            hos_name, hos_dist, hos_path = find_nearest_target(selected_acc, "hos")
            if hos_path:
                animate_path(hos_path, selected_acc, hos_name, hos_dist, "To Hospital", "green")
        elif severity == "minor":
            pol_name, pol_dist, pol_path = find_nearest_target(selected_acc, "pol")
            if pol_path:
                animate_path(pol_path, selected_acc, pol_name, pol_dist, "To Police", "blue")

    option_win = tk.Toplevel()
    option_win.title("Select Accident Info")

    ttk.Label(option_win, text="Select Accident Node:").pack(pady=5)
    acc_var = tk.StringVar()
    acc_dropdown = ttk.Combobox(option_win, textvariable=acc_var, values=accident_nodes)
    acc_dropdown.pack(pady=5)

    severity_var = tk.StringVar()
    ttk.Radiobutton(option_win, text="Major", variable=severity_var, value="major").pack()
    ttk.Radiobutton(option_win, text="Minor", variable=severity_var, value="minor").pack()

    ttk.Button(option_win, text="Submit", command=process_selection).pack(pady=10)

def simulate_phone_gui():
    def add_digit(digit):
        current = phone_var.get()
        phone_var.set(current + digit)

    def clear_number():
        phone_var.set("")

    def handle_call():
        number = phone_var.get()
        if number == "911":
            root.withdraw()
            show_options_window()
        else:
            messagebox.showerror("Invalid", "Please dial 911 to proceed.")

    root = tk.Tk()
    root.title("Emergency Dialer")

    phone_var = tk.StringVar()
    display = ttk.Label(root, textvariable=phone_var, font=("Arial", 24), background="white", anchor="center")
    display.pack(padx=10, pady=10, fill='x')

    btn_frame = ttk.Frame(root)
    btn_frame.pack()

    # Create number buttons (1-9)
    for i in range(1, 10):
        btn = ttk.Button(btn_frame, text=str(i), command=lambda d=str(i): add_digit(d), width=5)
        btn.grid(row=(i - 1) // 3, column=(i - 1) % 3, padx=5, pady=5)

    # Row for Clear, 0, and Call buttons
    ttk.Button(btn_frame, text="Clear", command=clear_number, width=5).grid(row=3, column=0, padx=5, pady=5)
    ttk.Button(btn_frame, text="0", command=lambda: add_digit("0"), width=5).grid(row=3, column=1, padx=5, pady=5)
    ttk.Button(btn_frame, text="Call", command=handle_call, width=5).grid(row=3, column=2, padx=5, pady=5)

    root.mainloop()

simulate_phone_gui()
