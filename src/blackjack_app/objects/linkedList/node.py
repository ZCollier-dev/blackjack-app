class Node:
    
    # next - next node in chain
    # data - data in current node
    
    def __init__(self, data):
        self.next = None # New node
        self.data = data
        
    def enqueue(self, data):
        if self.data is None:
            self.data = data
        elif self.next is None:
            self.next = Node(data)
        else:
            self.next.enqueue(data)
            
    def dequeue(self):
        return self.next
    
    def view(self):
        
        if self.next is None:
            return f"{self.data}" # sometimes the best answer is the simplest
        else:
            return f"{self.data}," + self.next.view()