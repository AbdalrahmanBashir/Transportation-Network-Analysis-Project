import networkx as nx


class GraphManager:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def add_city(self, city):
        self.graph.add_node(city)

    def add_connection(self, source, destination, distance, one_way=False):

        self.graph.add_edge(source, destination, distance=distance)
        if not one_way:
            self.graph.add_edge(destination, source, distance=distance)

    def get_shortest_path_with_intermediate_hops(self, source, destination):
        try:
            path = nx.shortest_path(
                self.graph, source, destination, weight='distance', method='dijkstra')

            total_distance = 0
            for i in range(len(path) - 1):
                total_distance += self.graph[path[i]][path[i + 1]]['distance']

            return path, total_distance
        except nx.NetworkXNoPath:
            return None, float('inf')

    def cities_reachable_within_distance(self, start_city, max_distance):
        max_distance = int(max_distance)  # Convert to integer
        reachable_cities = []
        for city in self.graph.nodes:
            if city != start_city:
                try:
                    distance = nx.shortest_path_length(
                        self.graph, start_city, city, weight='distance', method='dijkstra')
                    if distance <= max_distance:
                        reachable_cities.append((city, distance))
                except nx.NetworkXNoPath:
                    pass
        return reachable_cities

    def find_isolated_cities(self):
        isolated_cities = [city for city in self.graph.nodes if not any(
            nx.has_path(self.graph, city, other_city)
            for other_city in self.graph.nodes if other_city != city
        )]
        return isolated_cities

    def get_graph(self):
        return self.graph
