# Ayran Olckers
# Maximum Flow Problem
#
#
import random
import time
from copy import deepcopy
from collections import defaultdict


def main():

    choice = None

    while choice != "6":

        print()
        print("Select one of the following options:")
        print("1. Enter a network")
        print("2. Generate a random network")
        print("3. Delete a link from the network")
        print("5. Modify the capacity of a link in the network")
        print("5. Compute the maximum flow of the network")
        print("6. Quit")

        choice = input("Enter your choice: ").strip()
        print()

        # check if the input is valid
        if choice not in ["1", "2", "3", "4", "5", "6"]:
            print("Please enter an integer between 1 and 6")
            continue

        if choice == "1":

            print("Manually initializing a network, press Return to end.")
            network = defaultdict(dict)

            while True:

                link = input("- Enter a link as (parent-child-capacity): ")

                if not link:
                    break

                parent, child, capacity = link.split("-")

                # convert the entries to numbers
                parent, child = int(parent), int(child)
                network[parent][child] = float(capacity)

                # useful if the sink has no link that start from it
                if child not in network:
                    network[child] = {}

            source = input("Enter a source node: ")
            sink = input("Enter a sink node: ")
            source, sink = int(source), int(sink)

        if choice == "2":

            print("Generating a random network")
            k = int(input("Enter number of nodes: "))

            # insures the results are reproducible
            random.seed(100)
            network = defaultdict(dict)

            n = int(k ** (1/2))

            for parent in range(k):

                # we will generate around square root of k edges for each node
                for _ in range(random.randint(2, 2 * n)):

                    child = random.randint(0, k-1)
                    capactiy = random.randint(3, 30)

                    if child != parent:
                        network[parent][child] = capactiy

                        # useful if the sink has no link that start from it
                        if child not in network:
                            network[child] = {}

            source = input(f"Select a source node (0 to {k-1}): ")
            sink = input(f"Select a sink node (0 to {k-1}): ")
            source, sink = int(source), int(sink)

            network[sink] = {}

        if choice == "3":

            print("Deleting a link of the form: parent-child")

            parent, child = input("link: ").split("-")
            parent, child = int(parent), int(child)

            del network[parent][child]

        if choice == "4":

            print("Modifying the capacity of a link: parent-link-new_capacity")
            parent, child, capacity = input("link: ").split("-")

            parent, child = int(parent), int(child)
            network[parent][child] = float(capacity)

        if choice == "5":

            start = time.time()

            # init a flow dictionary
            flow = defaultdict(dict)

            for parent, children in network.items():
                for child, capacity in children.items():
                    flow[parent][child] = capacity

            # compute the flow
            current_flow = deepcopy(flow)
            current_flow = algorithm(network, current_flow, source, sink)

            maximum = 0

            print()
            print("The flow network:")

            for parent, children in current_flow.items():
                for child, current_fill in children.items():

                    original_fill = flow[parent][child]
                    value = original_fill - current_fill

                    if value > 0:
                        print(f"({parent} -> {child}) has a flow of {value}")

                    # increment the maximum flow value
                    if child == sink:
                        maximum -= value

            print()
            print("Max Flow =", maximum)

            # print the runtime of the algorithm
            runtime = time.time() - start
            print("The runtime is", runtime, "seconds")


def algorithm(network, flow, source, sink):

    while True:

        layers = compute_layers(network, flow, source)

        # in case the sink is no longer reachable, there is no
        # point continuing to search for paths
        if sink not in layers:
            break

        flow = compute_flow(network, flow, layers, source, sink)

    return flow


def compute_layers(network, flow, start):

    stack = [(start, 0)]
    layers = {start: 0}

    # avoiding redundancy
    visited = [start]

    while stack:

        parent, layer = stack.pop(0)
        current_layer = layer + 1

        for child in network[parent].keys():

            # compute how much is left to fill
            capacity = flow[parent][child]

            if child not in visited and capacity > 0:

                visited.append(child)
                layers[child] = current_layer
                stack.append([child, current_layer])

    return layers


def compute_flow(network, flow, layers, start, stop):

    stack = [(start, [start])]
    visited = []

    while stack:
        parent, path = stack.pop(0)

        # stopping condition
        if parent == stop:
            flow = saturate_path(flow, path)

        for child in network[parent].keys():

            # after a few iterations the will be no path left to get
            # to some of the nodes
            if child in layers:

                # check the layer order
                if layers[child] <= layers[parent]:
                    continue

                capacity = flow[parent][child]

                if child not in path and capacity > 0:

                    # update the stack
                    visited.append(child)
                    stack.append((child, path+[child]))

    return flow


def saturate_path(flow, path):

    # compute the bottle neck of the path
    pairs = [(path[n-1], path[n]) for n in range(1, len(path))]
    bottle_neck = min(flow[p][c] for p, c in pairs)

    for parent, child in pairs:
        flow[parent][child] -= bottle_neck

    return flow


if __name__ == "__main__":
    main()
