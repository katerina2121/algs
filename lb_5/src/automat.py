class Node:
    def __init__(self):
        self.son: dict = {}  # Массив сыновей
        self.go: dict = {} # Массив переходов
        self.parent: Node | None = None  # Вершина родитель
        self.suffLink: Node | None = None  # Суффиксная ссылка
        self.len_sufflink_chain: int = 0 # Длина цепочки из суффиксных ссылок до корня
        self.up: Node | None = None  # Сжатая суффиксная ссылка
        self.len_uplink_chain: int = 0 # Длина цепочки из сжатых суффиксных ссылок до корня
        self.charToParent: str | None = None  # Символ, ведущий к родителю
        self.isLeaf: bool = False  # Флаг, является ли вершина терминалом
        self.depth: int = 0 # Уровень, на котором находимя вершина
        self.leafPatternNumber: list[int] = []
        self.id: int = 0 # Идентификатор вершины

    def __str__(self):
        if not self.parent:
            return "Вершина - корень."
        sons_str = ", ".join(self.son.keys())
        res_str = f"Вершина c id {self.id}:\n - Находится на уровне {self.depth}"
        res_str += f"\n - У которой {len(self.son)} сыновей"
        if len(self.son)>0:
            res_str += f", от которых идут символы: {sons_str}."
        if self.charToParent:
            res_str += f"\n - Символ, ведущий к родителю(id родителя = {self.parent.id}) - {self.charToParent}"
        if self.isLeaf:
            res_str += f"\n - Является терминальной для паттерна(ов) под номером(ами) {self.leafPatternNumber}"
        return res_str


def getSuffLink(v: Node, root: Node) -> Node:
    """Функция для вычисления суффиксной ссылки"""
    if v.suffLink is None:  # Если суффиксная ссылка еще не вычислена
        if v == root or v.parent == root:
            v.suffLink = root
        else:
            v.suffLink = getLink(getSuffLink(v.parent, root), v.charToParent, root)
    v.len_sufflink_chain = v.suffLink.len_sufflink_chain + 1
    return v.suffLink


def getLink(v: Node, char: str, root: Node) -> Node:
    """Функция для вычисления перехода"""
    if char not in v.go:
        if char in v.son:
            v.go[char] = v.son[char]
        elif v == root:
            v.go[char] = root
        else:
            v.go[char] = getLink(getSuffLink(v, root), char, root)
    return v.go[char]


def getNodeUp(v: Node, root: Node) -> Node:
    """Функция для вычисления сжатой суффиксной ссылки"""
    if v.up is None:
        if getSuffLink(v,root).isLeaf:
            v.up = getSuffLink(v, root)
        elif getSuffLink(v, root) == root:
            v.up = root
        else:
            v.up = getNodeUp(getSuffLink(v,root), root)
    v.len_uplink_chain = v.up.len_uplink_chain + 1
    return v.up


def add_string(s: str, pattern_number: int, root: Node, num_vertices: int) -> int:
    """Добавляет строку в бор."""
    cur = root
    for char in s:
        if char not in cur.son:
            new_node = Node()
            new_node.parent = cur
            new_node.charToParent = char
            new_node.depth = cur.depth + 1
            num_vertices += 1
            new_node.id = num_vertices
            cur.son[char] = new_node
            print(f"Для символа {char} строим новое ребро и вершину с id = {num_vertices}")
        else: print(f"Для символа {char} уже построено ребро")
        cur = cur.son[char]

    cur.isLeaf = True
    cur.leafPatternNumber.append(pattern_number)
    print(f"Последнюю вершину с id = {cur.id} помечаем как терминальную для паттерна №{pattern_number}\n")
    return num_vertices

def build_aho_corasick(patterns: list[str]) -> Node:
    """Строит автомат Ахо-Корасик для заданных образцов."""
    root = Node()
    root.suffLink = root
    root.up = root
    root.charToParent = None
    root.parent = None
    num_vertices = 0
    for i, pattern in enumerate(patterns):
        print(f"Добавление паттерна {pattern} в бор...")
        num_vertices = add_string(pattern, i, root, num_vertices)

    print(f"Количество вершин в построенном боре: {num_vertices}")
    queue = [root]
    max_len_sufflink_chain = 0
    max_len_uplink_chain = 0
    print("\nПостроение суффиксных и сжатых суффиксных ссылок для всех вершин")
    while queue:
        v = queue.pop(0)
        for char, u in v.son.items():
            print(f"\nТЕКУЩАЯ ВЕРШИНА:\n{u}")
            print(f"\nCтроим суффиксную ссылку для текущей вершины...")
            node_sufflink = getSuffLink(u,root)
            max_len_sufflink_chain = max(max_len_sufflink_chain, u.len_sufflink_chain)
            print(f"Суффиксной ссылкой является вершина c id = {node_sufflink.id}")
            print(f"\nCтроим сжатую суффиксную ссылку для текущей вершины...")
            node_up = getNodeUp(u,root)
            max_len_uplink_chain = max(max_len_uplink_chain, u.len_uplink_chain)
            print(f"Сжатой суффиксной ссылкой является вершина c id = {node_up.id}")
            queue.append(u)
    print(f"\nПосле построения автомата получено:\nМаксимальная длина цепочки суффиксных ссылок = {max_len_sufflink_chain}\nМаксимальная длина цепочки сжатых суффиксных ссылок = {max_len_uplink_chain}")
    return root