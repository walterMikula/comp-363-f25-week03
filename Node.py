class Node:
    
    def __init__(self, frequency: int, symbol: str | None = None):
        """Initialize a new node.

        Args:
            frequency (int): The frequency of the node.
            symbol (str, optional): The symbol associated with the node. Defaults to None.
        """
        self.__frequency = frequency
        self.__symbol = symbol
        self.__left = None
        self.__right = None


    def set_left(self, child) -> None:
        self.__left = child

    def set_right(self, child) -> None:
        self.__right = child


    def get_frequency(self) -> int:
        return self.__frequency

    def get_symbol(self) -> str:
        return self.__symbol

    def get_left(self):
        return self.__left

    def get_right(self):
        return self.__right

    def __str__(self) -> str:
        return f"({self.__symbol}:{self.__frequency})"

    def __repr__(self) -> str:
        return self.__str__()

    def __lt__(self, other: "Node") -> bool:
        return self.__frequency < other.__frequency

def create_forest(frequencies: list[int]) -> list[Node]:
    forest: list[Node] = []
    total_letters = 0

    i = 0
    while i < 26:
        f = frequencies[i]
        if f > 0:
            forest.append(Node(f, chr(ord("A") + i)))
            total_letters = total_letters + f
        i = i + 1

        forest.append(Node(total_letters + 1, " "))
        return forest

def filter_uppercase_and_spaces(input_string: str) -> str:
    return "".join(ch for ch in input_string.upper() if ch.isalpha() or ch == " ")

def get_smallest(forest: list[Node]) -> Node:
    smallest_index = 0
    i = 1
    size = len(forest)
    while i < size;
        if forest[i] < forest [smallest_index]:
            smallest_index = i
        i = i + 1
    return forest.pop(smallest_index)

def huffman(forest: list[Node]) -> Node:
    while len(forest) > 1:
        s1 = get_smallest(forest)
        s2 = get_smallest(forest)
        new_node =Node(s1.get_frequency() +s2.get_frequency())
        new_node.set_left(s1)
        new_node.set_right(s2)
        forest.append(new_node)
    return forest[0]

def count_frequencies(input_string: str)-> list[int]:
    frequencies: list[int] = [0] * 26
    i = 0
    n = len(input_string)
    while i < n:
        ch = input_string[i]
        if ch != " ":
            idx = ord(ch) - ord("A")
            if 0 <= idx < 26:
                frequencies[idx] = frequencies[idx] + 1
        i = i + 1
    return frequencies

def initialize_forest(frequencies: list[int]) -> list[Node]:
    
    return forest

def build_huffman_tree(frequencies: list[int]) -> Node:
    return 

def encoding_table(huffman_tree_root: Node) -> list[str]:
    return

def encode (input_string: str, encoding_table: list[str]) -> str:
    return
