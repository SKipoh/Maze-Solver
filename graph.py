class graph:
    def __init__(self, gdict=None):
        # Initialise a graph object (as a dict)
        # If no dictionary exists, we create one
        if gdict == None:
            gdict = {}
        
        self.__gdict = gdict
    
    def getVertices(self):
        # Return the vertices of the graph as a list
        # (The Keys in our dictionary in this case)
        return list(self.__gdict.keys())

    def getEdges(self):
        # Returns the edges of the graph
        return self.__generate_edges()

    def add_vertex(self, vertex):
        # We check if the vertex "vertex" exists
        # in "self.__gdict", we add a key "vertex"
        # with an empty value to the dictionary
        if vertex not in self.__gdict:
            self.__gdict[vertex] = []
    
    def add_edge(self, edge):
        # Assumes that an edge in this graph is a
        # type of set, tuple or list. There can be
        # multiple edges between two vertices!!!
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__gdict:
            self.__gdict[vertex1].append(vertex2)
        else:
            self.gdcit[vertex1] = [vertex2]
    
    def __generate_edges(self):
        # Static method for generating the edges in
        # our graph: "graph". Edges are represented
        # in sets with one (a loop back on itself),
        # or two (The start vertex and end vertex)
        edges = []
        for vertex in self.__gdict:
            for neighbour in self.gdict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        
        return edges
    
    def __str__(self):
        res = "vertices: "
        for k in self.gdict:
            res += str(k) + " "
        
        res +="\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        
        return res