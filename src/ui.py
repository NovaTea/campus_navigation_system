import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from src.graph import Graph
from src.algorithms import bfs, dfs, dijkstra

class CampusNavigationUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Navigation System")
        self.root.geometry("1200x900")
        
        self.map_image = Image.open("data/campus_map.png")
        self.map_image = self.map_image.resize((800, 800))
        self.map_photo = ImageTk.PhotoImage(self.map_image)

        self.location_coords = {
            "AdmissionsOffice": (520, 730),
            "TitanStore": (330, 515),
            "ClayesPerformanceArtCenter": (350, 603),
            "ComputerScience": (640, 485),
            "DanBlackHall": (380, 710),
            "Engineering": (600, 485),
            "EducationClassroom": (500, 545),
            "EastsideNorthParkingStructure": (730, 570),
            "EastsideSouthParkingStructure": (730, 620),
            "ParkingLotA": (200, 200),
            "GordonHall": (500, 670),
            "Humanities": (520, 620),
            "Kinesiology": (380, 480),
            "LangsdorfHall": (480, 715),
            "McCarthyHall": (410, 663),
            "NutwoodParkingStructure": (240, 695),
            "PollakLibrary": (425, 530),
            "StudentRecreationCenter": (260, 420),
        }

        self.start_node = None
        self.end_node = None

        self.canvas = tk.Canvas(root, width=800, height=800)
        self.canvas.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.canvas.create_image(0, 0, anchor="nw", image=self.map_photo)

        self.draw_nodes()

        self.graph = Graph()
        self.graph.load_from_csv("data/campus_map.csv")

        tk.Button(root, text="Find Path (BFS)", command=self.find_path_bfs).grid(row=1, column=0)
        tk.Button(root, text="Find Path (DFS)", command=self.find_path_dfs).grid(row=1, column=0, columnspan=2)
        tk.Button(root, text="Find Path (Dijkstra)", command=self.find_path_dijkstra).grid(row=1, column=1)

        self.path_details = tk.Label(root, text="", font=("Arial", 10), justify="left", wraplength=400)
        self.path_details.grid(row=0, column=2, columnspan=2, pady=20, padx=20)

    def draw_nodes(self):
        for location, (x, y) in self.location_coords.items():
            node = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="yellow", outline="black", tags="node")
            self.canvas.tag_bind(node, "<Button-1>", lambda event, loc=location: self.select_node(loc))
            self.canvas.create_text(x, y-10, text=location, font=("Arial", 8), fill="red")

    def select_node(self, location):
        if not self.start_node:
            self.start_node = location
            self.highlight_node(location, "red")
        elif not self.end_node:
            self.end_node = location
            self.highlight_node(location, "green")
        else:
            self.reset_selection()
            self.start_node = location
            self.highlight_node(location, "red")

    def highlight_node(self, location, color):
        x, y = self.location_coords[location]
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=color, outline="black", tags="highlight")

    def reset_selection(self):
        self.canvas.delete("path")
        self.canvas.delete("highlight")
        self.start_node = None
        self.end_node = None
        self.path_details.config(text="")

    def find_path_bfs(self):
        if self.start_node and self.end_node:
            self.draw_path(bfs)

    def find_path_dfs(self):
        if self.start_node and self.end_node:
            self.draw_path(dfs)

    def find_path_dijkstra(self):
        if self.start_node and self.end_node:
            self.draw_path(dijkstra)

    def draw_path(self, algorithm):
        path = algorithm(self.graph, self.start_node, self.end_node)

        self.canvas.delete("path")
        self.path_details.config(text="")

        total_distance = 0
        total_time = 0
        details = []

        if path:
            for i in range(len(path) - 1):
                start, end = path[i], path[i + 1]
                x1, y1 = self.location_coords[start]
                x2, y2 = self.location_coords[end]
                self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=3, tags="path")

                edge = self.graph.adj_list[start][end]
                distance = edge['distance']
                time = edge['time']
                accessible = "Yes" if edge['accessible'] else "No"
                
                total_distance += distance
                total_time += time
                details.append(f"{start} -> {end}:\n  Distance: {distance} m\n  Time: {time} min\n  Accessible: {accessible}\n")

            details_text = "\n".join(details)
            total_text = f"\nTotal Distance: {total_distance} m\nTotal Time: {total_time} min"
            self.path_details.config(text=details_text + total_text)
            
            x_start, y_start = self.location_coords[self.start_node]
            x_end, y_end = self.location_coords[self.end_node]
            self.canvas.create_oval(x_start-5, y_start-5, x_start+5, y_start+5, fill="red", tags="path")
            self.canvas.create_oval(x_end-5, y_end-5, x_end+5, y_end+5, fill="green", tags="path")
        else:
            messagebox.showinfo("Result", "No path found.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CampusNavigationUI(root)
    root.mainloop()
