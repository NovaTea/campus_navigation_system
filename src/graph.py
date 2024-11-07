import csv
from collections import defaultdict

class Graph:
    def __init__(self):
        self.adj_list = defaultdict(dict)

    def add_edge(self, start, end, distance, time, accessible):
        self.adj_list[start][end] = {
            'distance': distance,
            'time': time,
            'accessible': accessible
        }
        self.adj_list[end][start] = {
            'distance': distance,
            'time': time,
            'accessible': accessible
        }

    def load_from_csv(self, file_path):
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                start = row['start']
                end = row['end']
                distance = int(row['distance'])
                time = int(row['time'])
                accessible = row['accessible'].lower() == 'true'
                self.add_edge(start, end, distance, time, accessible)

    def get_neighbors(self, node):
        return self.adj_list[node] if node in self.adj_list else {}
