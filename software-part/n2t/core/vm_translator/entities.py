class Stack:
    def __init__(self) -> None:
        self.sp = 256
        self.elems = []
        self.type = "stack"
        self.log_len = 0

    def pop(self) -> int:
        if self.log_len == 0:
            raise IndexError("stack is empty")
        else:
            self.log_len -= 1
            self.sp -= 1
            return self.elems[self.log_len]

    def push(self, item: int) -> None:
        self.elems.append(item)
        self.log_len += 1
        self.sp += 1
