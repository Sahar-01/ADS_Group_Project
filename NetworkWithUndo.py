class Node:
   def __init__(self, data):
      self.left = None
      self.right = None
      self.data = data  # Stores parent or size (negative for roots)

class NetworkWithUndo:
    def __init__(self, N):
        self.inArray = ArrayListWithUndo()
        for _ in range(N):
            self.inArray.append(Node(-1))  # Each node is its own root initially
        self.undos = Stack()
        self.undos.push(N)
        
    def getSize(self):
        return self.inArray.length()
        
    def add(self):
        N = self.getSize()
        self.inArray.append(Node(-1))
        self.undos.push(1)
        return N
    
    def root(self, i):
        path = []
        while self.inArray.get(i).data >= 0:  # Follow parent links
            path.append(i)
            i = self.inArray.get(i).data
            
        root = i
        for node in path:  # Path compression
            self.inArray.get(node).data = root
        return root
    
    def merge(self, i, j):
        root_i = self.root(i)
        root_j = self.root(j)
    
        if root_i == root_j:
            return
    
        size_i = -self.inArray.get(root_i).data
        size_j = -self.inArray.get(root_j).data
    
        if size_i < size_j:  # Attach smaller tree to larger tree
            self.inArray.get(root_i).data = root_j
            new_size = size_i + size_j
            self.inArray.get(root_j).data = -new_size
        else:
            self.inArray.get(root_j).data = root_i
            new_size = size_i + size_j
            self.inArray.get(root_i).data = -new_size
            
        self.undos.push(2)
    
    def undo(self):
        if self.undos.size == 0:
            return
        
        last_op = self.undos.pop()
        if last_op == 1:
            self.inArray.undo()
        elif last_op == 2:
            self.inArray.undo()
            self.inArray.undo()
    
    def toArray(self):
        return [node.data for node in self.inArray.toArray()]
            
    def __str__(self):
        return str(self.toArray()) + "\n-> " + str(self.undos)
