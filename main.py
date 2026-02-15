import tkinter as tk
from tkinter import messagebox
from collections import deque
import math
import random


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shortest Cycle Finder")
        self.root.geometry("1000x700")

        self.nodes = []
        self.edges = []
        self.node_counter = 0
        self.mode = 'node'
        self.selected_node = None

        # Liste des cycles à surligner (plusieurs)
        self.highlighted_cycles = []

        # Couleurs principales
        self.bg_color = "#f8f9fa"
        self.node_color = "#667eea"
        self.edge_color = "#64748b"
        self.select_color = "#fbbf24"

        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas
        canvas_frame = tk.Frame(main_frame, bg=self.bg_color)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg=self.bg_color, cursor="crosshair", width=700, height=700)
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Control panel
        control_frame = tk.Frame(main_frame, bg="white", width=250)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        control_frame.pack_propagate(False)

        title = tk.Label(control_frame, text="Graph Controls",
                         font=("Arial", 16, "bold"), bg="white", fg="#333")
        title.pack(pady=20)

        # Mode buttons
        mode_label = tk.Label(control_frame, text="Mode:",
                              font=("Arial", 12, "bold"), bg="white")
        mode_label.pack(pady=(10, 5))

        self.mode_buttons = {}
        modes = [
            ("Add Nodes", "node"),
            ("Add Edges", "edge"),
            ("Delete", "delete")
        ]

        for text, mode in modes:
            btn = tk.Button(control_frame, text=text,
                            command=lambda m=mode: self.set_mode(m),
                            font=("Arial", 11), width=18, height=2,
                            bg="#667eea" if mode == "node" else "white",
                            fg="white" if mode == "node" else "#667eea",
                            relief=tk.RAISED, bd=2)
            btn.pack(pady=5)
            self.mode_buttons[mode] = btn

        tk.Label(control_frame, text="", bg="white").pack(pady=10)

        find_btn = tk.Button(control_frame, text="Find Shortest Cycle",
                             command=self.find_shortest_cycle,
                             font=("Arial", 11, "bold"), width=18, height=2,
                             bg="#10b981", fg="white", relief=tk.RAISED, bd=2)
        find_btn.pack(pady=5)

        clear_btn = tk.Button(control_frame, text="Clear All",
                              command=self.clear_graph,
                              font=("Arial", 11, "bold"), width=18, height=2,
                              bg="#ef4444", fg="white", relief=tk.RAISED, bd=2)
        clear_btn.pack(pady=5)

        result_frame = tk.Frame(control_frame, bg="#f0f9ff", relief=tk.SOLID, bd=1)
        result_frame.pack(pady=20, padx=10, fill=tk.X)

        result_title = tk.Label(result_frame, text="Result:",
                                font=("Arial", 11, "bold"),
                                bg="#f0f9ff", fg="#667eea")
        result_title.pack(anchor=tk.W, padx=10, pady=(10, 5))

        self.result_label = tk.Label(result_frame, text="No cycle found yet",
                                     font=("Arial", 10), bg="#f0f9ff",
                                     wraplength=200, justify=tk.LEFT)
        self.result_label.pack(anchor=tk.W, padx=10, pady=(0, 10))

        # Instructions
        instr_frame = tk.Frame(control_frame, bg="#fff7ed", relief=tk.SOLID, bd=1)
        instr_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        instr_title = tk.Label(instr_frame, text="Instructions:",
                               font=("Arial", 11, "bold"),
                               bg="#fff7ed", fg="#ea580c")
        instr_title.pack(anchor=tk.W, padx=10, pady=(10, 5))

        instructions = [
            "• Add Nodes: Click on canvas",
            "• Add Edges: Click two nodes",
            "• Delete: Click node/edge",
            "• Find: Click the button"
        ]

        for instr in instructions:
            lbl = tk.Label(instr_frame, text=instr, font=("Arial", 9),
                           bg="#fff7ed", anchor=tk.W)
            lbl.pack(anchor=tk.W, padx=10, pady=2)

    def set_mode(self, mode):
        self.mode = mode
        self.selected_node = None

        for m, btn in self.mode_buttons.items():
            if m == mode:
                btn.config(bg="#667eea", fg="white")
            else:
                btn.config(bg="white", fg="#667eea")

        self.draw()

    def on_canvas_click(self, event):
        x, y = event.x, event.y

        if self.mode == 'node':
            self.add_node(x, y)
        elif self.mode == 'edge':
            self.handle_edge_click(x, y)
        elif self.mode == 'delete':
            self.handle_delete(x, y)

    def add_node(self, x, y):
        node = {'id': self.node_counter, 'x': x, 'y': y}
        self.nodes.append(node)
        self.node_counter += 1
        self.highlighted_cycles = []
        self.draw()

    def handle_edge_click(self, x, y):
        clicked_node = self.get_node_at(x, y)

        if clicked_node:
            if not self.selected_node:
                self.selected_node = clicked_node
            elif self.selected_node != clicked_node:
                if not self.edge_exists(self.selected_node, clicked_node):
                    self.edges.append({
                        'from': self.selected_node['id'],
                        'to': clicked_node['id']
                    })
                    self.highlighted_cycles = []
                self.selected_node = None
            self.draw()

    def handle_delete(self, x, y):
        clicked_node = self.get_node_at(x, y)

        if clicked_node:
            self.nodes = [n for n in self.nodes if n['id'] != clicked_node['id']]
            self.edges = [e for e in self.edges
                          if e['from'] != clicked_node['id']
                          and e['to'] != clicked_node['id']]
            self.highlighted_cycles = []
        else:
            clicked_edge = self.get_edge_at(x, y)
            if clicked_edge:
                self.edges.remove(clicked_edge)
                self.highlighted_cycles = []

        self.draw()

    def get_node_at(self, x, y):
        for node in self.nodes:
            dist = math.sqrt((node['x'] - x)**2 + (node['y'] - y)**2)
            if dist < 20:
                return node
        return None

    def get_edge_at(self, x, y):
        for edge in self.edges:
            from_node = next((n for n in self.nodes if n['id'] == edge['from']), None)
            to_node = next((n for n in self.nodes if n['id'] == edge['to']), None)

            if from_node and to_node:
                dist = self.distance_to_line(x, y, from_node['x'], from_node['y'], to_node['x'], to_node['y'])
                if dist < 5:
                    return edge
        return None

    def distance_to_line(self, x, y, x1, y1, x2, y2):
        A, B = x - x1, y - y1
        C, D = x2 - x1, y2 - y1
        dot = A * C + B * D
        len_sq = C * C + D * D
        if len_sq == 0:
            return math.sqrt(A * A + B * B)
        param = dot / len_sq
        if param < 0:
            xx, yy = x1, y1
        elif param > 1:
            xx, yy = x2, y2
        else:
            xx = x1 + param * C
            yy = y1 + param * D
        return math.sqrt((x - xx) ** 2 + (y - yy) ** 2)

    def edge_exists(self, node1, node2):
        return any((e['from'] == node1['id'] and e['to'] == node2['id']) or
                   (e['from'] == node2['id'] and e['to'] == node1['id'])
                   for e in self.edges)

    def draw(self):
        self.canvas.delete("all")

        # Liste de couleurs pour cycles (aléatoires pastel)
        cycle_colors = [
            "#e11d48", "#0ea5e9", "#10b981", "#f97316",
            "#a855f7", "#14b8a6", "#ec4899", "#84cc16"
        ]

        # Dessiner les arêtes avec couleur par cycle
        for edge in self.edges:
            color = self.edge_color
            width = 2

            # Si l’arête appartient à un cycle
            for idx, cycle in enumerate(self.highlighted_cycles):
                if self.is_edge_in_cycle(edge, cycle):
                    color = cycle_colors[idx % len(cycle_colors)]
                    width = 4
                    break

            from_node = next((n for n in self.nodes if n['id'] == edge['from']), None)
            to_node = next((n for n in self.nodes if n['id'] == edge['to']), None)
            if from_node and to_node:
                self.canvas.create_line(from_node['x'], from_node['y'],
                                        to_node['x'], to_node['y'],
                                        fill=color, width=width)

        # Dessiner les nœuds
        for node in self.nodes:
            color = self.node_color
            for idx, cycle in enumerate(self.highlighted_cycles):
                if node['id'] in cycle:
                    color = cycle_colors[idx % len(cycle_colors)]
                    break

            self.canvas.create_oval(node['x'] - 20, node['y'] - 20,
                                    node['x'] + 20, node['y'] + 20,
                                    fill=color, outline="white", width=3)
            self.canvas.create_text(node['x'], node['y'],
                                    text=str(node['id']),
                                    fill="white", font=("Arial", 14, "bold"))

        # Node selection (mode edge)
        if self.selected_node and self.mode == 'edge':
            self.canvas.create_oval(self.selected_node['x'] - 25,
                                    self.selected_node['y'] - 25,
                                    self.selected_node['x'] + 25,
                                    self.selected_node['y'] + 25,
                                    outline=self.select_color, width=3)

    def is_edge_in_cycle(self, edge, cycle):
        for i in range(len(cycle)):
            next_i = (i + 1) % len(cycle)
            if ((edge['from'] == cycle[i] and edge['to'] == cycle[next_i]) or
                (edge['from'] == cycle[next_i] and edge['to'] == cycle[i])):
                return True
        return False

    def find_shortest_cycle(self):
        if not self.nodes:
            messagebox.showinfo("Info", "Please add some nodes first!")
            return

        graph = self.build_graph()
        cycles = self.shortest_cycles(graph)

        if cycles:
            self.highlighted_cycles = cycles
            text = [f"Cycle {i+1} (len={len(c)}): {' → '.join(map(str, c))}" for i, c in enumerate(cycles)]
            self.result_label.config(text="\n".join(text))
        else:
            self.highlighted_cycles = []
            self.result_label.config(text="No cycle found!")

        self.draw()

    def build_graph(self):
        graph = {node['id']: [] for node in self.nodes}
        for edge in self.edges:
            graph[edge['from']].append(edge['to'])
            graph[edge['to']].append(edge['from'])
        return graph

    def shortest_cycles(self, graph):
        min_cycle_len = float('inf')
        all_min_cycles = []

        for start in graph:
            dist = {start: 0}
            parent = {start: None}
            queue = deque([start])

            while queue:
                u = queue.popleft()

                for v in graph[u]:
                    if v not in dist:
                        dist[v] = dist[u] + 1
                        parent[v] = u
                        queue.append(v)
                    elif parent[u] != v:
                        cycle_len = dist[u] + dist[v] + 1

                        path_u, path_v = [], []
                        node = u
                        while node is not None:
                            path_u.append(node)
                            node = parent[node]

                        node = v
                        while node is not None:
                            path_v.append(node)
                            node = parent[node]

                        cycle_set = set(path_u)
                        for i, node in enumerate(path_v):
                            if node in cycle_set:
                                idx = path_u.index(node)
                                cycle = path_u[:idx] + path_v[:i+1][::-1]
                                break

                        if cycle_len < min_cycle_len:
                            min_cycle_len = cycle_len
                            all_min_cycles = [cycle]
                        elif cycle_len == min_cycle_len:
                            norm = sorted(cycle)
                            if all(sorted(c) != norm for c in all_min_cycles):
                                all_min_cycles.append(cycle)
        return all_min_cycles

    def clear_graph(self):
        self.nodes = []
        self.edges = []
        self.node_counter = 0
        self.selected_node = None
        self.highlighted_cycles = []
        self.result_label.config(text="No cycle found yet")
        self.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
