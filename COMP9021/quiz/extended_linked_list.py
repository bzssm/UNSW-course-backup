# Written by **** for COMP9021



from quiz.linked_list_adt import LinkedList


class ExtendedLinkedList(LinkedList):
    def __init__(self, L=None):
        super().__init__(L)

    def rearrange(self):
        def getlastnode(LL):
            now = LL.head
            while now.next_node != None:
                now = now.next_node
            return now

        def getevennum(LL):
            now = LL.head
            i = 0
            while now != None:
                if now.value % 2 == 0:
                    i += 1
                now = now.next_node
            return i

        def getprenode(LL, node):
            now = LL.head
            while now.next_node != node:
                now = now.next_node
            return now

        current_node = self.head
        while current_node != None:
            if current_node.value % 2 != self.head.value % 2:
                break
            current_node = current_node.next_node
        if current_node == None:
            return
        current_node = self.head

        for _ in range(getevennum(self)):
            while current_node.value % 2 != 0:
                current_node = current_node.next_node
            if current_node == self.head:
                getlastnode(self).next_node = current_node
                self.head = current_node.next_node
                current_node.next_node = None
            else:
                getprenode(self, current_node).next_node = current_node.next_node
                current_node.next_node = None
                getlastnode(self).next_node = current_node
            current_node = self.head

