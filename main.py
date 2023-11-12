# Import necessary libraries and modules
from graph_manager import GraphManager  # Import the GraphManager class
import city_coordinates  # Module for getting city coordinates
import networkx as nx  # Library for creating and manipulating complex networks
import tkinter as tk  # GUI toolkit
import folium  # Library for creating interactive maps
from geopy.geocoders import Nominatim  # Geocoding library
import webbrowser  # Library for opening web browsers
from tkinter import Canvas  # Canvas widget for drawing
import csv  # Module for reading and writing CSV files

# CSV file containing city data
csv_file = "city_data.csv"

# Read the CSV file
with open(csv_file, mode='r') as file:
    reader = csv.reader(file)
    data = [row for row in reader]

# Create an instance of the GraphManager class


def create_graph():
    graph_manager = GraphManager()

    # Add cities and connections to the graph
    for row in data:
        if len(row) == 3:
            start_city, end_city, distance = row
            if start_city != None:
                graph_manager.add_city(start_city)
            if end_city != None:
                graph_manager.add_city(end_city)
            if int(distance) > 0:
                graph_manager.add_connection(
                    start_city, end_city, int(distance))
        elif len(row) == 1:
            city = row[0]
            graph_manager.add_city(city)
    return graph_manager

# Draw the graph using Folium and display it in a Tkinter window


def draw_graph(graph_manager):
    G = graph_manager.get_graph()

    # Create a Folium map centered at a specific location
    map_center = city_coordinates.get_coordinates("Kansas City, Missouri")
    m = folium.Map(location=map_center, zoom_start=3)

    # Create markers for cities
    for node in G.nodes():
        city_coords = city_coordinates.get_coordinates(node)
        if city_coords != [0, 0]:
            folium.Marker(location=city_coords, popup=node).add_to(m)

    # Create lines for connections
    for edge in G.edges():
        start, end = edge
        start_coords = city_coordinates.get_coordinates(start)
        end_coords = city_coordinates.get_coordinates(end)
        if start_coords != [0, 0] and end_coords != [0, 0]:
            folium.PolyLine([start_coords, end_coords], color="blue").add_to(m)

    # Save the map as an HTML file
    m.save("city_map.html")

    # Draw the graph in a Tkinter canvas
    G = graph_manager.get_graph()
    canvas = Canvas(root, width=900, height=800)
    canvas.pack()

    # Set the positions of nodes using spring layout
    pos = nx.spring_layout(G)

    # Draw nodes
    for node in G.nodes():
        x, y = pos[node]
        x, y = x * 300 + 400, y * 300 + 300  # Scale and position nodes
        canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="lightblue")
        canvas.create_text(x, y, text=node)

    # Draw edges
    for edge in G.edges():
        start, end = edge
        x1, y1 = pos[start]
        x2, y2 = pos[end]
        x1, y1 = x1 * 300 + 400, y1 * 300 + 300
        x2, y2 = x2 * 300 + 400, y2 * 300 + 300
        canvas.create_line(x1, y1, x2, y2, fill="blue")

# Function to display all cities on the map


def show_all_cities_on_map():
    draw_graph(graph_manager)
    webbrowser.open("city_map.html")

# Function to find the shortest path between two cities


def find_shortest_path():
    start_city = start_city_entry.get()
    end_city = end_city_entry.get()

    shortest_path, shortest_distance = graph_manager.get_shortest_path_with_intermediate_hops(
        start_city, end_city)

    if shortest_path:
        # Display the result in the Tkinter window
        result_label.config(
            text=f"Shortest Path: {shortest_path}\nShortest Distance: {shortest_distance:.2f} miles")

        # Create a Folium map with the shortest path highlighted
        map_center = city_coordinates.get_coordinates('Kansas City, Missouri')
        m = folium.Map(location=map_center, zoom_start=3)

        path_coords = [city_coordinates.get_coordinates(
            city) for city in shortest_path]
        folium.PolyLine(locations=path_coords, color="red").add_to(m)
        for city in shortest_path:
            city_coords = city_coordinates.get_coordinates(city)
            if city_coords != [0, 0]:
                folium.Marker(location=city_coords, popup=city).add_to(m)

        # Save and open the map in a web browser
        m.save("city_map_with_path.html")
        webbrowser.open("city_map_with_path.html")
    else:
        result_label.config(
            text=f"No path found from {start_city} to {end_city}.")

# Function to display cities reachable within a specified distance


def display_cities_reachable_within_distance():
    start_city = start_city_entry.get()
    max_distance = max_distance_entry.get()

    # Get the list of reachable cities and their distances
    reachable_cities = graph_manager.cities_reachable_within_distance(
        start_city, max_distance)

    if reachable_cities:
        # Display the reachable cities in the Tkinter window
        result_label.config(
            text=f"{reachable_cities}")

        # Create a Folium map with reachable cities highlighted
        map_center = city_coordinates.get_coordinates(start_city)
        m = folium.Map(location=map_center, zoom_start=5)
        cities_to_display = [city[0] for city in reachable_cities]

        for city in cities_to_display:
            city_coords = city_coordinates.get_coordinates(city)
            folium.Marker(location=city_coords, popup=city).add_to(m)

        # Add a green marker for the start city
        folium.Marker(location=map_center, popup=start_city,
                      icon=folium.Icon(color='green')).add_to(m)

        # Fit the map to the bounds of the displayed cities
        m.fit_bounds([[24.396308, -125.000000], [49.384358, -66.934570]])

        # Save and open the map in a web browser
        m.save("reachable_cities_map.html")
        webbrowser.open("reachable_cities_map.html")

# Function to find and display isolated cities on the map


def find_isolated_cities():
    isolated_cities = graph_manager.find_isolated_cities()

    if isolated_cities:
        # Create a Folium map with isolated cities highlighted
        map_center = city_coordinates.get_coordinates('Kansas City, Missouri')
        m = folium.Map(location=map_center, zoom_start=3)

        for city in isolated_cities:
            city_coords = city_coordinates.get_coordinates(city)
            folium.Marker(location=city_coords, popup=city).add_to(m)

        # Save and open the map in a web browser
        m.save("isolated_cities_map.html")
        webbrowser.open("isolated_cities_map.html")


# Create the main Tkinter window
root = tk.Tk()
root.title("City Path Finder")

# Set up the initial option menu
option_var = tk.StringVar()
option_var.set("")

# Function to update the displayed widgets based on the selected option


def update_option():
    selected_option = option_var.get()

    # Hide all widgets
    for widget in root.winfo_children():
        widget.pack_forget()

    # Display widgets based on the selected option
    if selected_option == "Find Shortest Path":
        start_city_label.pack()
        start_city_entry.pack()
        end_city_label.pack()
        end_city_entry.pack()
        find_button.pack()
        result_label.pack()
    elif selected_option == "Show Cities Within Distance":
        start_city_label.pack()
        start_city_entry.pack()
        max_distance_label.pack()
        max_distance_entry.pack()
        show_button.pack()
        result_label.pack()
    elif selected_option == "Show All Cities on Map":
        show_all_cities_button.pack()
    elif selected_option == "Show All Isolated Cities":
        show_all_isolated_cities_button.pack()

    option_menu.pack()


# Set up the option menu
option_menu = tk.OptionMenu(root, option_var, "Find Shortest Path",
                            "Show Cities Within Distance", "Show All Cities on Map", "Show All Isolated Cities")
option_menu.pack()

# Initialize Tkinter widgets for various options
start_city_label = tk.Label(root, text="Start City:")
start_city_entry = tk.Entry(root)
end_city_label = tk.Label(root, text="End City:")
end_city_entry = tk.Entry(root)
find_button = tk.Button(root, text="Find Shortest Path",
                        command=find_shortest_path)
max_distance_label = tk.Label(root, text="Maximum Distance (in mile):")
max_distance_entry = tk.Entry(root)
show_button = tk.Button(
    root, text="Show Cities Within Distance", command=display_cities_reachable_within_distance
)
show_all_cities_button = tk.Button(
    root, text="Show All Cities on Map", command=show_all_cities_on_map)
show_all_isolated_cities_button = tk.Button(
    root, text="Show All Isolated Cities", command=find_isolated_cities)
result_label = tk.Label(root, text="")


# Set up the trace for the option menu to call the update_option function
option_var.trace("w", lambda name, index, mode, sv=option_var: update_option())

# Create a graph manager instance
graph_manager = create_graph()

# Run the Tkinter main loop
root.mainloop()
