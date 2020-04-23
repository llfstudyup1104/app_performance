class Node(object):
    def __init__(self):
        self.value = None
        self.next = None
    
    def __str__(self):
        return str(self.value)

class Solution(object):
    def __init__(self):
        pass 
    
    def reverse_iteration(self, pHead):
        if not pHead or not pHead.next:
            return pHead
        
        last = None
        while pHead:
            tmp = pHead.next # 缓存当前节点的向后指针，待下次迭代用
            pHead.next = last # 这一步是反转的关键，相当于把当前的向前指针作为当前节点的向后指针
            last = pHead # 作为下次迭代时的（当前节点的）向前指针
            pHead = tmp # 作为下次迭代时的（当前）节点
        return last # 返回头指针，头指针就是迭代到最后一次时的head变量（赋值给了last）


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
    
    newhead = Solution()
    print(f'The new head is {newhead.reverse_loop(head)}')


if __name__ == '__main__':
    main()
