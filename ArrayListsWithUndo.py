# ArrayList and Stack code to use

class Stack():
    def __init__(self):
        self.inList = None
        self.size = 0
        
    def push(self, v):
        self.size += 1
        self.inList = (v,self.inList)
        
    def pop(self):
        if self.size == 0: assert(0)
        self.size -= 1
        (v,ls) = self.inList
        self.inList = ls
        return v
    
    def __str__(self):
        s = "["
        ls = self.inList
        for _ in range(self.size):
            (v,ls) = ls
            s += str(v)
            if ls!=None: s += ", "
        return s+"]"
        
class ArrayList:
    def __init__(self):
        self.inArray = [0 for i in range(10)]
        self.count = 0
        
    def get(self, i):
        return self.inArray[i]

    def set(self, i, e):
        self.inArray[i] = e

    def length(self):
        return self.count

    def append(self, e):
        self.inArray[self.count] = e
        self.count += 1
        if len(self.inArray) == self.count:
            self._resizeUp()

    def insert(self, i, e):
        for j in range(self.count,i,-1):
            self.inArray[j] = self.inArray[j-1]
        self.inArray[i] = e
        self.count += 1
        if len(self.inArray) == self.count:
            self._resizeUp()
    
    def remove(self, i):
        self.count -= 1
        val = self.inArray[i]
        for j in range(i,self.count):
            self.inArray[j] = self.inArray[j+1]
        return val

    def _resizeUp(self):
        newArray = [0 for i in range(2*len(self.inArray))]
        for j in range(len(self.inArray)):
            newArray[j] = self.inArray[j]
        self.inArray = newArray
        
    def toArray(self):
        return self.inArray[:self.count]

    def __str__(self):
        if self.count == 0: return "[]"
        s = "["
        for i in range(self.count-1): s += str(self.inArray[i])+", "
        return s+str(self.inArray[self.count-1])+"]" 

class ArrayListWithUndo(ArrayList):
    def __init__(self):
        # already implemented
        super().__init__()
        self.undos = Stack()

    def set(self, i, v):
        # Push undo operation to set back the original value
        self.undos.push(("set", i, self.inArray[i]))
        self.inArray[i] = v

    def append(self, v):
        # Record the undo operation before appending
        self.undos.push(("rem", self.count, None))
        super().append(v)

    def remove(self, i):
        # Record undo operation with the value being removed
        if i < self.count:  # Check if i is within bounds
            self.undos.push(("ins", i, self.inArray[i]))
            super().remove(i)

    def insert(self, i, v):
        # Record the undo operation before inserting
        if i <= self.count:  # Ensure valid index
            # Record the undo operation before inserting
            self.undos.push(("rem", i, None))
            super().insert(i, v)

    def undo(self):
        if self.undos.size == 0:
            return

        op, i, v = self.undos.pop()

        if op == "set":
            # Restore previous value
            self.inArray[i] = v
        elif op == "rem":
            # Remove the last element (append undo)
            self.count -= 1
        elif op == "ins":
            # Insert the removed value back to its original position
            self.insert(i, v)


    def __str__(self):
        # already implemented
        return str(self.toArray())+"\n-> "+str(self.undos)
        
# minimal tests ArrayListWithUndo

def tprint(ls,i):
    print("\n=== Test",i,"===\n",ls,"\nsize",ls.length())

ls = ArrayListWithUndo()
A = [2,3,4,5,5,1,4]
for x in A: ls.append(x)
ls.set(4,2)
ls.insert(3,10)
ls.remove(0)
tprint(ls,0)
for i in range(len(A)+4):
    ls.undo()
    tprint(ls,i+1)
