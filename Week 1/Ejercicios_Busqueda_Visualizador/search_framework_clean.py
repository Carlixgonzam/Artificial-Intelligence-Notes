#!/usr/bin/env python3
"""
SEARCH ALGORITHM VISUALIZATION FRAMEWORK
=========================================

This file handles ALL the visualization and UI.
Students do NOT modify this file!

This framework:
1. Provides the grid and terrain setup
2. Imports student algorithm implementations
3. Calls student algorithms with appropriate parameters
4. Visualizes the results

Students only modify: student_algorithms.py
"""

import tkinter as tk
from tkinter import ttk
import time
import sys

# Import student implementations
try:
    
    #import student_algorithms_clean as student_algos
    import student_algorithms_clean as student_algos
except ImportError:
    print("ERROR: Cannot find student_algorithms_clean.py")
    print("Make sure student_algorithms_clean.py is in the same directory!")
    sys.exit(1)


class SearchVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Search Algorithms Visualizer - Student Framework")
        
        # Grid configuration
        self.grid_size = 20
        self.cell_size = 30
        self.animation_speed = 50  # milliseconds
        
        # Terrain types and costs
        self.TERRAIN_TYPES = {
            'normal': {'cost': 1, 'color': 'white'},
            'shallow': {'cost': 2, 'color': 'lightblue'},
            'deep': {'cost': 5, 'color': 'darkblue'},
            'wall': {'cost': float('inf'), 'color': 'black'}
        }
        
        # Colors for visualization
        self.colors = {
            'start': 'green',
            'goal': 'red',
            'explored': 'lightgray',
            'current': 'orange',
            'path': 'yellow',
            'frontier_goal': 'pink'  # For bidirectional search from goal
        }
        
        # Start and goal positions
        self.start = (1, 1)
        self.goal = (18, 18)
        
        # Initialize terrain grid
        self.terrain = [['normal' for _ in range(self.grid_size)] 
                       for _ in range(self.grid_size)]
        
        self.setup_ui()
        self.create_default_terrain()
        self.draw_grid()
    
    def setup_ui(self):
        """Setup the user interface"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)
        
        # Canvas for grid
        self.canvas = tk.Canvas(main_frame, 
                               width=self.grid_size * self.cell_size,
                               height=self.grid_size * self.cell_size,
                               bg='white')
        self.canvas.grid(row=0, column=0, rowspan=10, padx=(0, 10))
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding=10)
        control_frame.grid(row=0, column=1, sticky='n')
        
        # Algorithm buttons
        ttk.Label(control_frame, text="Select Algorithm:").pack()
        
        ttk.Button(control_frame, text="BFS - Breadth First", 
                  command=lambda: self.run_algorithm('bfs'), width=20).pack(pady=2)
        ttk.Button(control_frame, text="DFS - Depth First", 
                  command=lambda: self.run_algorithm('dfs'), width=20).pack(pady=2)
        ttk.Button(control_frame, text="UCS - Uniform Cost", 
                  command=lambda: self.run_algorithm('ucs'), width=20).pack(pady=2)
        ttk.Button(control_frame, text="Bidirectional Search", 
                  command=lambda: self.run_algorithm('bidirectional'), width=20).pack(pady=2)
        
        ttk.Separator(control_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Terrain selection
        ttk.Label(control_frame, text="Paint Terrain:").pack()
        self.terrain_var = tk.StringVar(value='wall')
        
        for terrain_name, terrain_info in self.TERRAIN_TYPES.items():
            if terrain_name != 'normal':
                ttk.Radiobutton(control_frame, text=f"{terrain_name.title()} (cost {terrain_info['cost']})",
                              variable=self.terrain_var, value=terrain_name).pack(anchor='w')
        
        ttk.Separator(control_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Utility buttons
        ttk.Button(control_frame, text="Clear Terrain", 
                  command=self.clear_terrain, width=20).pack(pady=2)
        ttk.Button(control_frame, text="Reset View", 
                  command=self.reset_grid, width=20).pack(pady=2)
        
        # Speed control
        ttk.Label(control_frame, text="Animation Speed:").pack(pady=(10, 0))
        speed_slider = ttk.Scale(control_frame, from_=0, to=200, 
                                orient='horizontal',
                                command=lambda v: setattr(self, 'animation_speed', float(v)))
        speed_slider.set(self.animation_speed)
        speed_slider.pack(fill='x')
        
        # Info panel
        info_frame = ttk.LabelFrame(main_frame, text="Information", padding=10)
        info_frame.grid(row=1, column=1, sticky='nsew', pady=(10, 0))
        
        self.info_text = tk.Text(info_frame, width=30, height=15, wrap='word')
        self.info_text.pack()
        
        # Mouse bindings for terrain painting
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        
        self.update_info(
            "Student Framework Loaded!\n\n"
            "Students implement algorithms in:\n"
            "student_algorithms_clean.py\n\n"
            "This file handles all visualization.\n\n"
            "Paint terrain by clicking/dragging.\n"
            "Then run an algorithm to see it work!"
        )
    
    def create_default_terrain(self):
        """Create some default obstacles for testing"""
        for i in range(5, 15):
            self.terrain[8][i] = 'shallow'
        for i in range(7, 10):
            for j in range(9, 12):
                self.terrain[i][j] = 'deep'
        for i in range(5, 15):
            self.terrain[3][i] = 'wall'
            self.terrain[16][i] = 'wall'
    
    def draw_grid(self):
        """Draw the grid on canvas"""
        self.canvas.delete('all')
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = i * self.cell_size
                y1 = j * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                if (i, j) == self.start:
                    color = self.colors['start']
                elif (i, j) == self.goal:
                    color = self.colors['goal']
                else:
                    terrain_type = self.terrain[i][j]
                    color = self.TERRAIN_TYPES[terrain_type]['color']
                
                self.canvas.create_rectangle(x1, y1, x2, y2, 
                                            fill=color, outline='gray')
                
                if (i, j) != self.start and (i, j) != self.goal:
                    terrain_type = self.terrain[i][j]
                    cost = self.TERRAIN_TYPES[terrain_type]['cost']
                    if cost > 1 and cost != float('inf'):
                        self.canvas.create_text(x1 + self.cell_size/2, 
                                               y1 + self.cell_size/2,
                                               text=str(cost),
                                               font=('Arial', 8, 'bold'),
                                               fill='white')
        
        self.canvas.update()
    
    def draw_cell(self, pos, color):
        """Draw a single cell with given color"""
        i, j = pos
        x1 = i * self.cell_size
        y1 = j * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')
        self.canvas.update()
    
    def draw_path(self, path):
        """Draw the final path"""
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            self.canvas.create_line(
                x1 * self.cell_size + self.cell_size/2,
                y1 * self.cell_size + self.cell_size/2,
                x2 * self.cell_size + self.cell_size/2,
                y2 * self.cell_size + self.cell_size/2,
                fill=self.colors['path'], width=3, arrow=tk.LAST
            )
        for pos in path:
            if pos != self.start and pos != self.goal:
                self.draw_cell(pos, self.colors['path'])
        self.canvas.update()
    
    def get_neighbors(self, pos):
        """
        Get neighbors for a position - provided to student algorithms
        
        Returns: list of (neighbor_position, cost) tuples
        """
        i, j = pos
        neighbors = []
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size:
                terrain_type = self.terrain[ni][nj]
                cost = self.TERRAIN_TYPES[terrain_type]['cost']
                if cost != float('inf'):
                    neighbors.append(((ni, nj), cost))
        return neighbors
    
    def calculate_path_cost(self, path):
        """Calculate total cost of a path"""
        total_cost = 0
        for i in range(1, len(path)):
            terrain_type = self.terrain[path[i][0]][path[i][1]]
            cost = self.TERRAIN_TYPES[terrain_type]['cost']
            total_cost += cost
        return total_cost
    
    def update_info(self, message):
        """Update the info panel"""
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, message)
    
    def reset_grid(self):
        """Reset visualization (keep terrain)"""
        self.draw_grid()
    
    def clear_terrain(self):
        """Clear all terrain back to normal"""
        self.terrain = [['normal' for _ in range(self.grid_size)] 
                       for _ in range(self.grid_size)]
        self.draw_grid()
    
    def on_click(self, event):
        """Handle mouse click for terrain painting"""
        i = event.x // self.cell_size
        j = event.y // self.cell_size
        if 0 <= i < self.grid_size and 0 <= j < self.grid_size:
            if (i, j) != self.start and (i, j) != self.goal:
                self.terrain[i][j] = self.terrain_var.get()
                self.draw_grid()
    
    def on_drag(self, event):
        """Handle mouse drag for terrain painting"""
        self.on_click(event)
    
    # =========================================================================
    # ALGORITHM RUNNERS - Call student implementations and visualize results
    # =========================================================================
    
    def run_algorithm(self, algorithm_name):
        """
        Run a student algorithm and visualize the results
        
        This is the KEY function that separates algorithm logic from visualization!
        """
        self.reset_grid()
        
        try:
            # Call the appropriate student algorithm
            if algorithm_name == 'bfs':
                self.run_bfs()
            elif algorithm_name == 'dfs':
                self.run_dfs()
            elif algorithm_name == 'ucs':
                self.run_ucs()
            elif algorithm_name == 'bidirectional':
                self.run_bidirectional()
        
        except NotImplementedError:
            self.update_info(f"Algorithm not implemented yet!\n\n"
                           f"Implement {algorithm_name} in:\n"
                           f"student_algorithms_clean.py")
        except Exception as e:
            self.update_info(f"Error running algorithm:\n\n{str(e)}\n\n"
                           f"Check your implementation in:\n"
                           f"student_algorithms_clean.py")
            import traceback
            traceback.print_exc()
    
    def run_bfs(self):
        """Run BFS and visualize"""
        self.update_info("Running BFS...\nCalling student implementation...")
        
        # Call student's PURE algorithm
        path, explored_nodes = student_algos.breadth_first_search(
            self.start,
            self.goal,
            self.get_neighbors
        )
        
        # Visualize the exploration
        for pos in explored_nodes:
            if pos != self.start and pos != self.goal:
                self.draw_cell(pos, self.colors['current'])
                time.sleep(self.animation_speed / 1000.0)
                self.draw_cell(pos, self.colors['explored'])
        
        # Visualize the path
        if path:
            self.draw_path(path)
            cost = self.calculate_path_cost(path)
            self.update_info(f"BFS Complete!\n\n"
                           f"Path length: {len(path)} steps\n"
                           f"Total cost: {cost}\n"
                           f"Nodes explored: {len(explored_nodes)}\n\n"
                           f"BFS finds shortest path by STEPS,\n"
                           f"not necessarily by cost!")
        else:
            self.update_info(f"BFS: No path found!\n"
                           f"Nodes explored: {len(explored_nodes)}")
    
    def run_dfs(self):
        """Run DFS and visualize"""
        self.update_info("Running DFS...\nCalling student implementation...")
        
        path, explored_nodes = student_algos.depth_first_search(
            self.start,
            self.goal,
            self.get_neighbors
        )
        
        for pos in explored_nodes:
            if pos != self.start and pos != self.goal:
                self.draw_cell(pos, self.colors['current'])
                time.sleep(self.animation_speed / 1000.0)
                self.draw_cell(pos, self.colors['explored'])
        
        if path:
            self.draw_path(path)
            cost = self.calculate_path_cost(path)
            self.update_info(f"DFS Complete!\n\n"
                           f"Path length: {len(path)} steps\n"
                           f"Total cost: {cost}\n"
                           f"Nodes explored: {len(explored_nodes)}\n\n"
                           f"DFS may not find optimal path!")
        else:
            self.update_info(f"DFS: No path found!\n"
                           f"Nodes explored: {len(explored_nodes)}")
    
    def run_ucs(self):
        """Run UCS and visualize"""
        self.update_info("Running UCS...\nCalling student implementation...")
        
        path, explored_nodes = student_algos.uniform_cost_search(
            self.start,
            self.goal,
            self.get_neighbors
        )
        
        for pos in explored_nodes:
            if pos != self.start and pos != self.goal:
                self.draw_cell(pos, self.colors['current'])
                time.sleep(self.animation_speed / 1000.0)
                self.draw_cell(pos, self.colors['explored'])
        
        if path:
            self.draw_path(path)
            cost = self.calculate_path_cost(path)
            self.update_info(f"UCS Complete!\n\n"
                           f"Path length: {len(path)} steps\n"
                           f"Total cost: {cost} (OPTIMAL!)\n"
                           f"Nodes explored: {len(explored_nodes)}\n\n"
                           f"UCS guarantees lowest COST path!")
        else:
            self.update_info(f"UCS: No path found!\n"
                           f"Nodes explored: {len(explored_nodes)}")
    
    
    def run_bidirectional(self):
        """Run Bidirectional Search and visualize"""
        self.update_info("Running Bidirectional Search...\n"
                       "Calling student implementation...")
        
        path, explored_dict = student_algos.bidirectional_search(
            self.start,
            self.goal,
            self.get_neighbors
        )
        
        # Visualize exploration from start (orange)
        for pos in explored_dict.get('start', []):
            if pos != self.start and pos != self.goal:
                self.draw_cell(pos, self.colors['current'])
                time.sleep(self.animation_speed / 1000.0)
                self.draw_cell(pos, self.colors['explored'])
        
        # Visualize exploration from goal (pink)
        for pos in explored_dict.get('goal', []):
            if pos != self.start and pos != self.goal:
                self.draw_cell(pos, self.colors['frontier_goal'])
                time.sleep(self.animation_speed / 1000.0)
                self.draw_cell(pos, self.colors['explored'])
        
        if path:
            self.draw_path(path)
            cost = self.calculate_path_cost(path)
            total_explored = len(explored_dict.get('start', [])) + len(explored_dict.get('goal', []))
            self.update_info(f"Bidirectional Complete!\n\n"
                           f"Path length: {len(path)} steps\n"
                           f"Total cost: {cost}\n"
                           f"Nodes explored: {total_explored}\n"
                           f"  From start: {len(explored_dict.get('start', []))}\n"
                           f"  From goal: {len(explored_dict.get('goal', []))}\n\n"
                           f"Searches met in the middle!")
        else:
            total_explored = len(explored_dict.get('start', [])) + len(explored_dict.get('goal', []))
            self.update_info(f"Bidirectional: No path found!\n"
                           f"Nodes explored: {total_explored}")


if __name__ == '__main__':
    root = tk.Tk()
    app = SearchVisualizer(root)
    root.mainloop()