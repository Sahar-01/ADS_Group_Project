class NetworkWithUndo:
    def __init__(self, N):
        # already implemented
        self.inArray = ArrayListWithUndo()
        for _ in range(N): 
            self.inArray.append(-1)
        self.undos = Stack()
        self.undos.push(N)

    def getSize(self):
        # already implemented
        return self.inArray.length()

    def add(self):
        new_node = self.getSize()  # New node index
        self.inArray.append(-1)  # New node starts as its own root (value -1)
        self.undos.push(1)  # Record the operation in the undo stack

    def root(self, i):
        if i < 0 or i >= len(self.inArray):
            raise IndexError(f"Node {i} is out of bounds.")
        
        visited = []
        while self.inArray[i] >= 0:
            visited.append(i)
            i = self.inArray[i]
        
        # Path compression
        for node in visited:
            self.inArray[node] = i
        
        return i

    def merge(self, i, j):
        root_i = self.root(i)
        root_j = self.root(j)
        
        # Ensure both i and j are root nodes
        if root_i == root_j:
            return

        size_i = -self.inArray[root_i]
        size_j = -self.inArray[root_j]

        # Merge smaller cluster into the larger one or if sizes are equal, merge j into i
        if size_i > size_j or (size_i == size_j and root_i < root_j):
            self.inArray[root_j] = root_i
            self.inArray[root_i] = -(size_i + size_j)
        else:
            self.inArray[root_i] = root_j
            self.inArray[root_j] = -(size_i + size_j)

    def undo(self):
        pass

    def toArray(self):
        # already implemented
        return self.inArray.toArray()
        
    def __str__(self):
        return str(self.toArray()) + "\n-> " + str(self.undos)
