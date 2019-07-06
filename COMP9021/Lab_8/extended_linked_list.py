# Written by **** for COMP9021



from Lab_8.linked_list_adt import LinkedList


class ExtendedLinkedList(LinkedList):
    def __init__(self, L=None):
        super().__init__(L)

    def remove_duplicates(self):
        def getPre(LL,target):
            current=LL.head
            while(current!=None and current.next_node!=target):
                current=current.next_node
            return current
        def getLast(LL):
            current = LL.head
            while(current.next_node!=None):
                current=current.next_node
            return current

        usedSet=set()
        currentNode = self.head
        while(currentNode!=None):
            if currentNode.value in usedSet:
                if currentNode!=getLast(self):
                    getPre(self,currentNode).next_node = currentNode.next_node
                else:
                    getPre(self, currentNode).next_node = None
            else:
                usedSet.add(currentNode.value)
            currentNode = currentNode.next_node

    def MyReverse(self):
        if self.head == None or self.head.next_node==None:
            return self
        result = self.MyReverse(self.head.next)
        self.head.next.next = self.head
        self.head.next = None
        return result


