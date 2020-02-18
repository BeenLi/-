"""
    name : 归并排序
    author: 万力
    time : 2020/02/07
"""


class LNode:
    def __init__(self, elem, next_=None):
        self.elem = elem
        self.next = next_


class MergeSort:
    def __init__(self, head, func=None):
        self.head = head  # head是SSList链表的头结点
        self.func = func  # callback function : 以什么属性进行比较

    def filter(self):
        head = self.head  # LNode
        tmp = LNode(None)
        func = self.func
        irrelative = SLList()   # 存储不能比较的对象
        while head:
            if not func(head.elem):
                if head == self.head:  # 防止第一个元素就不是符合的实例
                    self.head = tmp.next = head.next
                else:
                    tmp.next = head.next    # 把不符合的元素从链表剔除出去
                irrelative.prepend(head.elem)
                head = tmp.next
            else:
                tmp, head = head, head.next
        return irrelative

    def sort_list(self, head):
        if not head or not head.next:
            return head
        tmp, slow, fast = None, head, head
        while fast and fast.next:
            tmp, slow, fast = slow, slow.next, fast.next
            if fast:
                fast = fast.next
            else:
                break
        tmp.next = None  # 把链表截断成head、slow

        l1 = self.sort_list(head)
        l2 = self.sort_list(slow)
        return self.merge(l1, l2)

    def merge(self, h1, h2):
        func = self.func
        new_head = h = LNode(None)  # 建立一个新的头结点
        while h1 and h2:
            if func(h1.elem) < func(h2.elem):
                h.next, h, h1 = h1, h1, h1.next
            else:
                h.next, h, h2 = h2, h2, h2.next
        h.next = h1 if h1 else h2
        return new_head.next

    def merge_sort(self):
        x2 = self.filter()              # x2是SSList类链表
        x1 = self.sort_list(self.head)  # x1是LNode类头结点
        p = x1
        if p:
            print("\n%-5s%-6s%-11s%-8s%-6s%-6s" % ("车牌号", "类型", "进场时间", "出场时间", "职工号码", "剩余次数/到期时间"))
            while p.next:
                print(p.elem.show())
                p = p.next

            print(p.elem.show())
            if x2.get_head():
                print("\n不符合比较的对象列表:", end="")
                x2.show_cars()
                p.next = x2.get_head()
        else:   # x1为空
            if x2.get_head():
                print("\n抱歉,您所排序的项目不符合排序条件")
                print("请查看系统里面的条目，如下:")
                x2.show_cars()
                return x2
        return SLList(x1)


class LinkedListError(ValueError):
    pass


class SLList:  # 带有头指针的单链表
    def __init__(self, head=None):
        self._head = head  # 初始化一个空表
        self._tail = None  # 带有尾部结点的链表

    def is_empty(self):
        return self._head is None

    def prepend(self, elem):  # 在表头加入元素
        if self._head is None:
            self._tail = self._head = LNode(elem)
        else:
            self._head = LNode(elem, self._head)

    def append(self, elem):  # 在表尾加元素
        if self._tail is None:
            self._tail = self._head = LNode(elem)
        else:
            self._tail.next = self._tail = LNode(elem)

    def pop(self):  # 弹出元素
        if self._head is None:
            raise LinkedListError("in pop")
        e = self._head.elem
        self._head = self._head.next
        return e

    def search(self, value, staffid=False):  # 如果按staffid查找，那么staffid=true;否则按车牌查找
        p = self._head
        card = []
        if staffid:  # 以员工号查找
            while p:
                try:
                    if p.elem.staffid == value:
                        card.append(p.elem)
                except AttributeError:
                    pass
                finally:
                    p = p.next  # 不管有没有这个属性都要执行
        else:
            while p:
                if p.elem.plate == value:
                    card.append(p.elem)
                p = p.next
        return card

    def show_cars(self):  # 浏览记录
        p = self._head
        if p:
            print("\n%-5s%-6s%-11s%-8s%-6s%-6s" % ("车牌号", "类型", "进场时间", "出场时间", "职工号码", "剩余次数/到期时间"))
            while p is not None:
                print(p.elem.show())
                p = p.next
        else:
            print("没有此种条目...")

    def get_head(self):  # 返回链表的头指针
        return self._head
