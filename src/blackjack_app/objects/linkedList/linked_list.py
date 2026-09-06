from blackjack_app.objects.linkedList.node import Node

# head - first node in chain

class LinkedList:
    def __init__(self, init_data=None):
        if init_data is None:
            self.head = None
        else:
            self.head = Node(init_data) # not the problem
        self.size = 0

    def enqueue(self, data):
        if self.head is None:
            self.head = Node(data)
        elif self.head.data is None:
            self.head.data = data
        else:
            self.head.enqueue(data)

        self.size += 1

    def dequeue(self):
        if self.head is not None and self.head.data is not None:
            data = self.head.data
            self.head = self.head.dequeue()
            self.size -= 1
            return data
        else:
            return False

    def clear(self):
        self.head = None
        self.size = 0

    def view(self):
        if self.head is not None and self.head.data is not None:
            return self.head.view()
        else:
            return ""
