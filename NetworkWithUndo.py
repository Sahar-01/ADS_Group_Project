class ArrayListWithUndo:
    def __init__(self):
        self.items = []  # This will store the list of elements
        self.history = []  # This will store operations for undo
    
    def append(self, item):
        self.items.append(item)  # Append the item to the list
        self.history.append(('append', item))  # Record the operation
    
    def pop(self):
        if self.items:  # Ensure there's something to pop
            item = self.items[-1]
            self.items = self.items[:-1]  # Remove last item manually (no pop function)
            self.history.append(('pop', item))  # Record the operation
            return item
        return None
    
    def length(self):
        return len(self.items)  # Return the length of the list
    
    def toArray(self):
        return self.items  # Return the list as an array
    
    def isEmpty(self):
        return len(self.items) == 0  # Check if the list is empty


class Stack:
    def __init__(self):
        self.items = []  # Store stack items
    
    def push(self, item):
        self.items.append(item)  # Push item to the stack
    
    def pop(self):
        if not self.is_empty():
            item = self.items[-1]
            self.items = self.items[:-1]  # Remove the last item manually (no pop function)
            return item
        return None
    
    def is_empty(self):
        return len(self.items) == 0  # Check if the stack is empty
    
    def __str__(self):
        return str(self.items)  # Custom string representation for Stack


class NetworkWithUndo:
    def __init__(self, N):
        self.inArray = ArrayListWithUndo()  # Create the custom ArrayListWithUndo instance
        for _ in range(N):
            self.inArray.append(-1)  # Initialize with -1 indicating each node is its own root
        self.undos = Stack()  # Create the custom Stack instance
        self.undos.push(N)  # Push the initial number of nodes as the first operation
    
    def getSize(self):
        return self.inArray.length()  # Get the size of the network
    
    def add(self):
        N = self.getSize()  # Get the current size of the network
        self.inArray.append(-1)  # Add a new node as a root (-1 indicates no parent)
        self.undos.push(1)  # Record the add operation
        return N
    
    def root(self, i):
        path = []  # Will store the path for path compression
        while self.inArray.items[i] >= 0:  # While not the root
            path.append(i)
            i = self.inArray.items[i]  # Move to the parent
        
        # Path compression: Make all nodes in the path point directly to the root
        for node in path:
            self.inArray.items[node] = i
        
        return i  # Return the root
    
    def merge(self, i, j):
        root_i = self.root(i)
        root_j = self.root(j)
        
        if root_i == root_j:  # If they are already in the same set, do nothing
            return
        
        size_i = -self.inArray.items[root_i]  # Size of the tree rooted at root_i
        size_j = -self.inArray.items[root_j]  # Size of the tree rooted at root_j
        
        # Union by size: Attach the smaller tree to the larger one
        if size_i < size_j:
            self.inArray.items[root_i] = root_j  # Make root_j the parent of root_i
            self.inArray.items[root_j] -= size_i  # Update the size of root_j
        else:
            self.inArray.items[root_j] = root_i  # Make root_i the parent of root_j
            self.inArray.items[root_i] -= size_j  # Update the size of root_i
        
        self.undos.push(2)  # Record the merge operation
    
    def undo(self):
        if self.undos.is_empty():
            return  # No operations to undo
        
        last_op = self.undos.pop()  # Get the last operation from the stack
        if last_op == 1:  # If the last operation was an add
            self.inArray.pop()  # Undo the add (remove the last element from the array)
        elif last_op == 2:  # If the last operation was a merge
            # Undoing a merge requires restoring the state of the array
            # This is tricky and depends on how you store the previous state of the merge
            pass
    
    def toArray(self):
        return self.inArray.toArray()  # Return the array of elements
    
    def __str__(self):
        return str(self.toArray()) + "\n-> " + str(self.undos)  # String representation


# Minimal tests for NetworkWithUndo

def tprint(n, i, s=""):
    print("\n=== Test", i, "===")
    if s != "":
        print(s)
    print(n, "\nsize", n.getSize())


# Create an instance of NetworkWithUndo and run the tests

net = NetworkWithUndo(9)
tprint(net, 0)

net.merge(4, 0)
net.merge(0, 3)
net.merge(2, 1)
net.merge(6, 8)
net.merge(8, 7)

tprint(net, 1)
net.merge(0, 8)
tprint(net, 2)

x = net.root(4)
tprint(net, 3, "root of 4: " + str(x))

net.undo()
tprint(net, 4)

net.undo()
tprint(net, 5)

net.merge(0, 1)
tprint(net, 6)

for i in range(8):
    net.undo()
    tprint(net, i + 7)

