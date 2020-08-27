class FibHeap:
    # Node class that makes up each Node, or binomial heap in this structure
    class Node:
        # Heap NODE Constructor
        def __init__(self, key, value):
            # Key is a unique identifier for each Node in the heap, so we can traverse to it
            self.key = key
            # Value is where we store the Maze.Node that the key refers too
            self.value = value
            # Degree is used to track the number of direct children of this Node (For the min
            # Node, this is the total number of "levels" to the heap)
            self.degree = 0
            # A node becomes marked (mark = True) if at least one of the Node's children was cut
            # since this Node was made a child of another Node
            self.mark = False
            self.parent = self.child = None
            # Previous & Next is used for the Doubly Linked List aspect of the heap and Priority
            # Queue. Next points to the next Heap Node in the Priority Queue, and Previous points 
            # to the Node that is "above" us in the queue
            self.previous = self.next = self


        # To check if this Node is single, we try to set ourselves to be the next Node in the
        # Priority Queue. This will Return False if there is no Next Node, and True otherwise
        def issingle(self):
            return self == self.next

        
        # Called when we want to insert a new Node into the Heap
        def insert(self, node):
            # First we check if we have been parsed nothing in node,
            if node == None:
                # And if we have, we do nothing
                return
            
            # Otherwise, we set the next Node's "previous" pointer
            # to be our current Node's previous
            self.next.previous = node.previous
            # Setting the Node's previous' next to be our current Node's next value
            node.previous.next = self.next
            # Updating next to be our current Node
            self.next = node
            # Setting our current Node's previous to be itself
            node.previous = self


        # Removing our Node from the Priority Queue
        def remove(self):
            # We set our Previous' "next" pointer to our next pointer
            self.previous.next = self.next
            # We set our next's Node's "previous" pointer to what our
            # previous pointer is
            self.next.previous = self.previous
            # We then set our own next and previous pointers to
            # ourselves effectively removing us from the queue
            self.next = self.previous = self


        # Function for adding a new child in to this Node
        def addchild(self, node):
            # First we check to see a child already exists
            if self.child == None:
                # If no child exists, we insert our Node as the child
                self.child = node
            else:
                # If one does exist, then we call insert on that child,
                # and keep traversing down to new children
                self.child.insert(node)
            
            # Set the node we're adding as a child's parent to be ourself
            node.parent = self
            # Setting the child node's mark to False because it doesn't have
            # any children that have been cut yet
            node.mark = False
            # and increasing our degree by 1
            self.degree += 1


        # Removing a child from the current Nod
        def removechild(self, node):
            # First, we check to see if the Node we are trying to remove has our
            # current Node (self) as it's parent
            if node.parent != self:
                # If not, then obviously we cannot remove it as a child
                raise AssertionError("Cannot remove child from a node that is not it's parent")
            
            # We call isSingle to check if the node has anything in it's "next" pointer
            if node.issingle():
                # If isSingle returns true, we then check if our child pointer contains the same
                # Node as the one we want to remove
                if self.child != node:
                    # If not, then we raise an error because we can't remove a Node that isn't
                    # the child of our current Node
                    raise AssertionError("Cannot remove a node that is not a child")
                # Otherwise, the Node IS a child, so we set our child pointer to nothing
                self.child = None
            else:
                # If the Node we want to remove doesn't have something in it's "next" pointer, we
                # then check if OUR current Node's child pointer is the Node we want to remove
                if self.child == node:
                    # If it is, then we set our child pointer to the Node we're removing's next
                    # pointer
                    self.child = node.next
                # We then call the Node's remove method
                node.remove()

            # We set the Node we want to remove#s parent pointer to None
            node.parent = None
            # We also set it's Mark flag to False
            node.mark = False
            # and finally, we subtract one from our current Node's degree count
            self.degree -= 1
    

    # Heap Constructor
    def __init__(self):
        # Pointer for the Min Node in the Heap, saves time trying to search for it
        self.minnode = None 
        # Total count of Nodes in the Heap
        self.count = 0
        # Pointer for the Heap Node with the most direct Children
        self.maxdegree = 0
    
    # Method for checking if the heap is empty
    def isempty(self):
        # We perform a check to see if the Heap's count is equal to zero,
        # Returns a true if it is 0, return False otherwise
        return self.count == 0
    
    # Method for inserting a new Node into the heap
    def insert(self, node):
        # Increase the Heap's total Node count
        self.count += 1
        # Calling the Heap's insertnode Method to add a Node
        self._insertnode(node)
    
    # Method for inserting a new Node into the heap
    def _insertnode(self, node):
        # We check if our Heap's minnode pointer is pointing at a Node
        if self.minnode == None:
            # If the pointer is empty, then, we set it to be our Node
            self.minnode = node
        else:
            # Otherwise, we call insert on whatever node our minPointer has
            self.minnode.insert(node)
            # We then see if the Node we want to insert has a smaller key than
            # the current Node...
            if node.key < self.minnode.key:
                # Then we set the Heap's minpointer to look at our new Node
                self.minnode = node
    
    # Method for returning the Node at the minnode pointer
    def minimum(self):
        # We first check if the minnode pointer is looking at something
        if self.minnode == None:
            # If nothing is there, we raise an error, as the Heap must be
            # empty
            raise AssertionError("Cannot return minimum of Empty Heap")
        # Finally, we return the contents of the minnonde Pointer
        return self.minnode

    # Method for merging two heaps together
    def merge(self, heap):
        # We try to insert the heap we want to merge into the Node our minnode pointer
        # is looking at
        self.minnode.insert(heap.minnode)
        # We then check to see if our Heap's minnode pointer is empty, or if our current
        # Heap's minnode pointer has a Node, and if the key in the current Heap's minnode
        # pointer is smaller than our current Heap's minnode pointer
        if self.minnode == None or (heap.minnode != None and heap.minnode.key < self.minnode.key):
            # If the new heap does have a smaller node, we move our current minnode pointer
            # to look at the new Heap's minnode
            self.minnode = heap.minnode
    
    def removeminimum(self):
        pass