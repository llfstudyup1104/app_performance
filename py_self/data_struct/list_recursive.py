class Node(object):
    def __init__(self):
        self.value = None
        self.next = None

    def __str__(self):
        return str(self.value)


class Solution(object):
    def __init__(self):
        pass

    def reverse_recursion(self, head):
        if not head or not head.next:
            return head
        new_head = self.reverse_recursion(head.next)
        head.next.next = head
        head.next = None
        return new_head


def main():
    three = Node()
    three.value = 3
    two = Node()
    two.value = 2
    two.next = three
    one = Node()
    one.value = 1
    one.next = two
    head = Node()
    head.value = 0
    head.next = one

    new_head = Solution()
    print(f'The new head is {new_head.reverse_recursion(head)}')


if __name__ == '__main__':
    main()
