# Implementation of a simple Stack and an ArrayList with undo functionality.

class Stack:
    """A simple stack implementation using a linked list representation."""
    
    def __init__(self):
        # Initialize an empty stack with size 0 and no elements.
        self.inList = None
        self.size = 0
        
    def push(self, v):
        """Push a value onto the stack."""
        self.size += 1
        # Store the new value and link it to the current stack.
        self.inList = (v, self.inList)
        
    def pop(self):
        """Pop the top value from the stack."""
        # Assert ensures the stack is not empty before popping.
        if self.size == 0: assert(0)
        self.size -= 1
        # Retrieve the top value and update the stack pointer.
        (v, ls) = self.inList
        self.inList = ls
        return v
    
    def __str__(self):
        """Return a string representation of the stack."""
        s = "["
        ls = self.inList
        for _ in range(self.size):
            (v, ls) = ls
            s += str(v)
            if ls != None: s += ", "
        return s + "]"
        
class ArrayList:
    """A dynamic array-like data structure."""
    
    def __init__(self):
        # Initialize with a fixed capacity array and count of elements.
        self.inArray = [0 for _ in range(10)]
        self.count = 0
        
    def get(self, i):
        """Get the element at index i."""
        return self.inArray[i]

    def set(self, i, e):
        """Set the element at index i to e."""
        self.inArray[i] = e

    def length(self):
        """Return the current number of elements."""
        return self.count

    def append(self, e):
        """Add an element to the end of the array."""
        self.inArray[self.count] = e
        self.count += 1
        # Resize the array if capacity is reached.
        if len(self.inArray) == self.count:
            self._resizeUp()

    def insert(self, i, e):
        """Insert an element at index i, shifting subsequent elements."""
        for j in range(self.count, i, -1):
            self.inArray[j] = self.inArray[j-1]
        self.inArray[i] = e
        self.count += 1
        if len(self.inArray) == self.count:
            self._resizeUp()
    
    def remove(self, i):
        """Remove the element at index i and shift subsequent elements."""
        self.count -= 1
        val = self.inArray[i]
        for j in range(i, self.count):
            self.inArray[j] = self.inArray[j+1]
        return val

    def _resizeUp(self):
        """Double the array size when capacity is exceeded."""
        newArray = [0 for _ in range(2 * len(self.inArray))]
        for j in range(len(self.inArray)):
            newArray[j] = self.inArray[j]
        self.inArray = newArray
        
    def toArray(self):
        """Return a list representation of the current elements."""
        return self.inArray[:self.count]

    def __str__(self):
        """Return a string representation of the array."""
        if self.count == 0: return "[]"
        s = "["
        for i in range(self.count-1): s += str(self.inArray[i]) + ", "
        return s + str(self.inArray[self.count-1]) + "]"

class ArrayListWithUndo(ArrayList):
    """Extension of ArrayList to support undo operations."""
    
    def __init__(self):
        # Initialize ArrayList and a stack for undo operations.
        super().__init__()
        self.undos = Stack()

    def set(self, i, v):
        """Set element at index i and store undo information."""
        self.undos.push(("set", i, self.inArray[i]))
        self.inArray[i] = v

    def append(self, v):
        """Append an element and store undo information."""
        self.undos.push(("rem", self.count, None))
        super().append(v)

    def remove(self, i):
        """Remove element at index i and store undo information."""
        if i < self.count:  # Check if i is within bounds
            self.undos.push(("ins", i, self.inArray[i]))
            super().remove(i)

    def insert(self, i, v):
        """Insert element at index i and store undo information."""
        if i <= self.count:  # Ensure valid index
            self.undos.push(("rem", i, None))
            super().insert(i, v)

    def undo(self):
        """Undo the last operation."""
        if self.undos.size == 0:
            return

        op, i, v = self.undos.pop()

        if op == "set":
            self.inArray[i] = v  # Restore previous value
        elif op == "rem":
            self.count -= 1  # Undo an append operation
        elif op == "ins":
            self.insert(i, v)  # Reinsert a removed element

    def __str__(self):
        """Return string representation of the list and undo stack."""
        return str(self.toArray()) + "\n-> " + str(self.undos)

# Minimal tests for ArrayListWithUndo

def tprint(ls, i):
    """Print test case results."""
    print("\n=== Test", i, "===\n", ls, "\nsize", ls.length())

ls = ArrayListWithUndo()
A = [2, 3, 4, 5, 5, 1, 4]
for x in A: 
    ls.append(x)
ls.set(4, 2)
ls.insert(3, 10)
ls.remove(0)
tprint(ls, 0)
for i in range(len(A) + 4):
        ls.undo()
    tprint(ls, i + 1)

