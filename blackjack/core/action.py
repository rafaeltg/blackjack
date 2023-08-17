from enum import IntEnum

class ActionsEnum(IntEnum):
    hit = 1
    stand = 2
    double_down = 3
    split = 4
    surrender = 5
    
    def __str__(self) -> str:
        return f"{self.value} ({self.name})"
