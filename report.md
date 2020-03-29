
Title
-----

In order to solve the maximum flow problem in an efficient yet easy to implement way, we resorted to use Dinic's algorithm.

The principle of the algorithm is to find the shortest paths in the network leading from the source to the sink and avoiding back tracking, then progressively fill those paths with their bottleneck values. This is done over and over until no more valid paths exist.

The implementation it self is fairly modular and divides the tasks into functions. The main function serves as an interface to the user. algorithm is a function that wraps around compute_layers and compute_flow, which do the heavy lifting of diving the network into layers based of how close the nodes are from the source ; and finding all possible shortest paths and filling them up to their bottleneck, respectively.

Data structure
--------------

The most suitable data structure we found for the problem was to represent both the network and the flow as dictionaries of dictionaries (we took advantage of pythonl's built in defaultdict data type).

Each key in the network dictionary is node, the value attached to it being a dictionary that has the children of that node as keys and their capacity as values.

The flow dictionary is fairly similar except that the final values of the dictionary are the maximum flow currently passing from the node rather than its capacity.

Pseudocode
----------

main:
This function is tasked with prompting the user with a list of the possible actions. The user then chooses the action he wants to perform using its index. Basic input validation is provided.

Option 1: enter a network manually link by link
Option 2: generate a random network with a given number of nodes
Option 3: delete a link from the network
Option 4: modifies the capacity of a link from the network 
Option 5: computes the maximum flow and the correspondent graph
Option 6: quit the program

algorithm:
This function in a high level implementation of Dinic's algorithm. It computes the layers of the graph and the flow until they converge into a solution..

compute_layers:
This function is a breadth first search that labels the nodes according to the clossest layer they are part of. For example, the source node is the only node in layer 0, it children are he only nodes on layer 1... etc.

compute_flow:
This function is tasked with computing the computing all possible shortest paths from the source to the sink. It then calls saturate_path to fill those paths with the maximum flow possible, corresponding to the bottleneck of that path.

saturate_path:
Fills a given path with the maximum flow possible, corresponding to the bottleneck of that path. 

Performance
-----------

Various network sizes were tested using the random generation option ; they yielded the following runtimes:

6 nodes:  0.0009975433349609375 seconds
12 nodes: 0.003989219665527344 seconds
24 nodes: 0.00698399543762207 seconds
48 nodes: 0.005983829498291016 seconds
9999 nodes: 225.35471773147583 seconds

Note: these are my times times here as it will differ from machine to machine.

Conclusion
----------

The Big-O complexity is based on my computer times. The algorithm runs in O(V^2E) time and is similar to the Edmonds–Karp algorithm, which runs in O(VE^2) time, in that it uses shortest augmenting paths



