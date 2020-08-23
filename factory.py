# Factory class for choosing the type of algorithm to search through the maze
# In a seperate file so that it is easily expanded on, and makes reading the
# code in maze.py a bit easier
class SovlerFactory:
    def __init__(self):
        # We set a default search, so if the user doesn't specifiy one, it will
        # use Breadth first
        self.Default = "breadthfirst"
        # Also set a list of choices 
        self.Choices = ["breadthfirst", "depthfirst", "dijkstra", "astar", "leftturn"]

    
    def createSolver(self, type):
        if type == "leftturn":
            import leftturn
            return ["Left Turn Only", leftturn.solve]
        elif type == "depthfirst":
            import depthfirst
            return ["Depth First", depthfirst.solve]
        elif type == "dijkstra":
            import dijkstra
            return ["Dijkstra", dijkstra.solve]
        elif type == "astar":
            import astar
            return ["A Star", astar.solve]
        elif type == "breadthfirst":
            import breadthfirst
            return ["Breadth First", breadthfirst.solve]