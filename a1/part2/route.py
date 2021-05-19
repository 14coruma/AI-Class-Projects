#!/usr/local/bin/python3
import argparse
import networkx as nx
import math
import heapq
import copy

def total_distance(src, graph):
    item, history = src
    if len(history) == 0:
        return 0
    dist = graph.adj[item][history[-1]]["length"]
    for i, hist_item in enumerate(history):
        if (i+1) >= len(history):
            return dist
        dist += graph.adj[hist_item][history[i+1]]["length"]
    return dist

def total_hours(src, graph, speed=False):
    item, history = src
    if len(history) == 0:
        return 0
    time = graph.adj[item][history[-1]]["length"] / \
        (graph.adj[item][history[-1]]["speed_limit"] + 5)
    for i, hist_item in enumerate(history):
        if (i+1) >= len(history):
            return time
        nxt = history[i+1]
        mph = graph.adj[hist_item][nxt]["speed_limit"] + 5
        time += graph.adj[hist_item][nxt]["length"] / mph
    return time

def total_accidents(src, graph):
    item, history = src
    p = 0.000001
    if len(history) == 0:
        return 0
    accident_chance = p * graph.adj[item][history[-1]]["length"] * \
        graph.adj[item][history[-1]]["speed_limit"]
    for i, hist_item in enumerate(history):
        if (i+1) >= len(history):
            return accident_chance
        accident_chance += p * graph.adj[hist_item][history[i+1]]["length"] * \
            graph.adj[hist_item][history[i+1]]["speed_limit"]
    return accident_chance

def find_most_recent(src, dest, graph):
    """
    Get the h_x(s) of the most recent state with coordinates, less the distance it took to get there
    """
    item, history = src
    dist = graph.adj[item][history[-1]]["length"]
    for i in range(len(history)-1, -1, -1):
        if i > 0: 
            if history[i] in h_x_cache:
                return max(h_x_cache[history[i]] - dist, 0)
            dist += graph.adj[history[i]][history[i-1]]["length"]
    return 0

h_x_cache = {}
def h_x(src, dest, cost_func, graph):
    """
    heuristic to the goal
    """
    item, history = src
    if item in h_x_cache:
        return h_x_cache[item]
    if cost_func == "segments":
        return 1  # is there an actual heuristic that works?
    elif cost_func == "distance":
        if "latitude" not in graph.nodes[item]:
            # location does not have lat/long
            # use the previous location as next best guess
            r = find_most_recent(src, dest, graph)

        r = bird_flies_distance(item, dest, graph)
    elif cost_func == "time":
        if "latitude" not in graph.nodes[item]:
            # location does not have lat/long
            # use the previous location as next best guess
            est_dist = find_most_recent(src, dest, graph)
        else:
            est_dist = bird_flies_distance(item, dest, graph)
        r = est_dist / 70  # over max speed
    elif cost_func == "cycling":
        p = 0.000001
        if "latitude" not in graph.nodes[item]:
            # location does not have lat/long
            # use the previous location as next best guess
            est_dist = find_most_recent(src, dest, graph)
        else:
            est_dist = bird_flies_distance(item, dest, graph)

        r = p * est_dist * 20  # under min speed
    else:
       raise Exception("unsupported cost function '{}'".format(cost_func))

    h_x_cache[item] = r
    return r

def g_x(src, dest, cost_func, graph):
    """
    Cost so far
    """
    item, history = src
    if cost_func == "segments":
        return len(history)+1  # simple number of segments count
    elif cost_func == "distance":
        return total_distance(src, graph)
    elif cost_func == "time":
        return total_hours(src, graph, speed=True)
    elif cost_func == "cycling":
        return total_accidents(src, graph)
    else:
        raise Exception("unsupported cost function '{}'".format(cost_func))

def f_x(src, dest, cost, graph):
    return g_x(src, dest, cost, graph) + h_x(src, dest, cost, graph)

def is_goal(src, dest):
    item, history = src
    return item == dest

def gen_children(src, dest, cost_func, graph):
    item, history = src
    new_hist = copy.deepcopy(history)
    new_hist.append(item)
    for neighbor in list(graph.adj[item]):
        if neighbor not in history:
            yield (neighbor, new_hist), g_x((neighbor, new_hist), dest, cost_func, graph)

def search(src, dest, cost, graph):
    src = (src, [])
    visited_g_costs = {}
    fringe = []
    i = 0
    heapq.heappush(fringe, (f_x(src, dest, cost, graph), i, src))
    i += 1
    while len(fringe) != 0:
        priority, _, pop = heapq.heappop(fringe)
        if i % 1000 == 0:
            print("exploring:", pop[0], len(fringe))
        if len(pop[1]) != len(set(pop[1])):
            raise Exception("cyclic search path")
        if is_goal(pop, dest):
            return pop
        for child, g_x_cost in gen_children(pop, dest, cost, graph):
            if child[0] not in visited_g_costs or child[0] in visited_g_costs and visited_g_costs[child[0]] > g_x_cost:
                h = h_x(child, dest, cost, graph)
                visited_g_costs[child[0]] = g_x_cost
                new_item = (h + g_x_cost, i, child)
                heapq.heappush(fringe, new_item)
            i += 1
    if len(fringe) == 0:
        return None

def load_cities(g: nx.Graph):
    cities = []
    with open("city-gps.txt", "r") as f:
        for line in f.readlines():
            name, latitude, longitude = line.split(" ")
            _, state = name.split(",")
            g.add_node(name, longitude=float(longitude),
                           latitude=float(latitude), state=state)
    return cities

def build_graph(cost_func):
    graph = nx.Graph()
    cities = load_cities(graph)
    for city in cities:
        graph.add_node(city)
    with open("road-segments.txt", "r") as f:
        for line in f.readlines():
            src, dest, length, speed_limit, name = line.split(" ")
            length = int(length)
            speed_limit = int(speed_limit)
            name = name.strip()
            if cost_func == "segments":
                graph.add_edge(src, dest, length=length,
                            speed_limit=speed_limit, name=name, weight=1)
            elif cost_func == "distance":
                graph.add_edge(src, dest, length=length,
                               speed_limit=speed_limit, name=name, weight=length)
            elif cost_func == "time":
                graph.add_edge(src, dest, length=length,
                               speed_limit=speed_limit, name=name, weight=length / (speed_limit+5))
            elif cost_func == "cycling":
                p = 0.000001
                graph.add_edge(src, dest, length=length,
                               speed_limit=speed_limit, name=name, weight=p * length * speed_limit)
            else:
                raise Exception(
                    "unsupported cost function '{}'".format(cost_func))
    return graph

def bird_flies_distance(src, goal, graph):   
    def haversine(lat1, lat2, long1, long2, t=False):
        # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude#19412565
        R = 3963  # radius of earth in miles
        dLat = math.radians(lat1) - math.radians(lat2)
        dLon = math.radians(long1) - math.radians(long2)
        a = math.sin(dLat/2) * math.sin(dLat/2) + \
            math.cos(math.radians(lat2)) * math.cos(math.radians(lat1)) * \
            math.sin(dLon/2) * math.sin(dLon/2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        if t:
            return R * c
        return math.floor(R * c) // 2

    def triangle_hav(lat1, lat2, long1, long2):
        a = haversine(lat1, lat2, long1, long1, t=True) ** 2
        b = haversine(lat1, lat1, long1, long2, t=True) ** 2
        return math.floor(math.sqrt(a + b)) // 2

    def pythag(lat1, lat2, long1, long2):
        a = (lat1 - lat2) ** 2
        b = (long1 - long2) ** 2
        return math.sqrt(a + b)

    if "latitude" not in graph.nodes[src]:
        return 0
    src_lat = graph.nodes[src]["latitude"]
    src_long = graph.nodes[src]["longitude"]
    goal_lat = graph.nodes[goal]["latitude"]
    goal_long = graph.nodes[goal]["longitude"]
    return pythag(src_lat, goal_lat, src_long, goal_long)


def print_result(result, goal, graph):
    item, history = result
    prnt = ""
    prnt += str(len(history))
    prnt += " "
    prnt += str(total_distance(result, graph))
    prnt += " "
    prnt += str(total_hours(result, graph))
    prnt += " "
    prnt += str(total_accidents(result, graph))
    for hist in history:
        prnt += " " + hist
    prnt += " " + goal
    print(prnt)

if __name__ == "__main__":
    cost_functions = ["segments", "distance", "time", "cycling", "statetour"]
    parser = argparse.ArgumentParser()
    parser.add_argument("src_city", type=str)
    parser.add_argument("dest_city", type=str)
    parser.add_argument("cost_func", type=str, choices=cost_functions)
    
    args = parser.parse_args()
    graph = build_graph(args.cost_func)

    goal = search(args.src_city, args.dest_city, args.cost_func, graph)
    print_result(goal, args.dest_city, graph)
