import pandas as pd 
import networkx as nx
import heapq

DF = pd.read_csv("data/merged_data.csv")

def parse_request(request):
    return request.form.get("senderAccountNumber"), request.form.get("receiverAccountNumber")

def dijkstra_manual(source, destination, df):
    graph = {}
    for _, row in df.iterrows():
        src, dest, weight = row["source"], row["destination"], row["weight"]

        if src not in graph:
            graph[src] = []
        if dest not in graph:  # Ensure all nodes are in the graph
            graph[dest] = []
        graph[src].append((dest, weight))

    if source not in graph or destination not in graph:
        return "Source or Destination not found in graph"

    pq = [(0, source)]
    min_cost = {node: float('inf') for node in graph}
    min_cost[source] = 0

    while pq:
        current_cost, current_node = heapq.heappop(pq)

        if current_node == destination:
            return current_cost

        if current_cost > min_cost[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            new_cost = current_cost + weight
            if new_cost < min_cost[neighbor]:
                min_cost[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor))

    return float('inf')  # Return inf if no path exists

def get_minimum_charges(request):
    senderAcc, receiverAcc = parse_request(request)

    df = DF[["FromBIC", "ToBIC", "Charges"]]
    df = df.rename(columns={"FromBIC": "source", "ToBIC": "destination", "Charges": "weight"})

    return dijkstra_manual(senderAcc, receiverAcc, df)

def get_minimum_time(request):
    senderAcc, receiverAcc = parse_request(request)

    df = DF[["FromBIC", "ToBIC", "TimeTakenInMinutes"]]
    df = df.rename(columns={"FromBIC": "source", "ToBIC": "destination", "TimeTakenInMinutes": "weight"})

    return dijkstra_manual(senderAcc, receiverAcc, df)
