class Ram:
    def __init__(self) -> None:
        self.registers: dict = {}

    def assign(self, address: int, value: int) -> None:
        self.registers[address] = value

    def get(self, address: int) -> int:
        if address in self.registers:
            return self.registers[address]
        return 0
