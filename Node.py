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
    while i < size:
        if forest[i] < forest[smallest_index]:
            smallest_index = i
        i = i + 1
    return forest.pop(smallest_index)


def huffman(forest: list[Node]) -> Node:
    while len(forest) > 1:
        s1 = get_smallest(forest)
        s2 = get_smallest(forest)
        new_node = Node(s1.get_frequency() + s2.get_frequency())
        new_node.set_left(s1)
        new_node.set_right(s2)
        forest.append(new_node)
    return forest[0]


def count_frequencies(input_string: str) -> list[int]:
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
    forest: list[Node] = [] # creates an empty list for the forest
    total_letters = 0
    i = 0
    while i < 26: # too loop over all 26 letters in the alphabet
        f = frequencies[i] # get the frequency of [i]
        if f > 0: # if the frequency is > 0 then create a node
            forest.append(Node(f, chr(ord("A") + i))) # add the node to the forest with the correct symbol
            total_letters = total_letters + f # increment frequency 
        i = i + 1 # moves on to count the next letter and will increment until it goes thorugh a-z

    # Add the space node with frequency greater than total letters
    forest.append(Node(total_letters + 1, " "))
    return forest


def build_huffman_tree(frequencies: list[int]) -> Node:
    forest = initialize_forest(frequencies) # makes a huffman tree from the frequencies
    return huffman(forest)


def encoding_table(huffman_tree_root: Node) -> list[str]:
    # Prepare a 27-slot table: 0–25 for A–Z, 26 for space
    table: list[str] = [""] * 27

    # DFS to fill codes
    def dfs(node: Node, path: str) -> None: # using recusion to iterate throight the huffman tree
        sym = node.get_symbol()
        left = node.get_left()
        right = node.get_right()

        if sym is not None: # gets the current node sym, and its childten
            if sym == " ": # it it is a space put it in slot 26 (last slot)
                table[26] = path
            else:
                idx = ord(sym) - ord("A") # if not a space get the index and put in the table
                if 0 <= idx < 26:
                    table[idx] = path
            return

        if left is not None: # stop of ther is no left child and add 0 bc left on a huffman tree means 0
            dfs(left, path + "0")
        if right is not None: # stop if there is no right child and add 1 to the code because 1 signifies a right movement in teh forect
            dfs(right, path + "1")

    dfs(huffman_tree_root, "") # starts recursion from teh root
    return table


def encode(input_string: str, encoding_table: list[str]) -> str:
    # Assumes input_string already filtered to A–Z and spaces
    encodedChar = [] # collects the encoded chars and puts them in an array
    i = 0
    n = len(input_string)
    while i < n: # loop through every character in teh message length n
        ch = input_string[i] # get the character at index i
        if ch == " ":
            encodedChar.append(encoding_table[26]) # append to index 26 if space
        else:
            idx = ord(ch) - ord("A") # get the code for the character and append 
            if 0 <= idx < 26:
                encodedChar.append(encoding_table[idx])
        i = i + 1 # moves to the next char
    return "".join(encodedChar) # makes it a sinlgly string of all the encoded chars


def decode(encoded_string: str, huffman_root: Node) -> str:
    result = [] # empty list to collect teh decoded message
    node = huffman_root # start at the root to traverse the huffman
    i = 0
    n = len(encoded_string)
    while i < n: # loop until there is nothing left to read
        bit = encoded_string[i]
        if bit == "0": # if the code is 0 then move to the left child 
            node = node.get_left()
        else:
            node = node.get_right() # moove to the right child if not 0

        if node.get_symbol() is not None:# ifa leaf node
            result.append(node.get_symbol()) # add it to the output list
            node = huffman_root # reset at the root for the next char
        i = i + 1 # move onto the next code
    return "".join(result)


if __name__ == "__main__":
    message = "HELLO WORLD"
    clean = filter_uppercase_and_spaces(message)
    print("Original:", clean)

    # Count and build tree
    freqs = count_frequencies(clean)
    root = build_huffman_tree(freqs)
    table = encoding_table(root)

    print("\nEncoding table:")
    i = 0
    while i < 26:
        if table[i] != "":
            print(chr(ord("A") + i), ":", table[i])
        i = i + 1
    if table[26] != "":
        print("SPACE :", table[26])

    # Encode + decode
    encoded = encode(clean, table)
    decoded = decode(encoded, root)

    print("\nEncoded Message:", encoded)
    print("Decoded back to origional message:", decoded)
    