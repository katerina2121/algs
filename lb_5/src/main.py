from automat import *


def process_text(text: str, root: Node, patterns: list[str]) -> list[tuple[int, int]]:
    cur = root
    results = []
    print("\nПоиск в тексте паттернов...")
    for i, char in enumerate(text):
        last_id = cur.id
        cur = getLink(cur, char, root)
        print(f"\n{i})Переход на символ в тексте {char} -> переход в автомате с вершины с id = {last_id} на вершину с id = {cur.id}")
        print("Проверка на соответствие паттерну:")
        node_up = cur
        while node_up != root:
            if node_up.isLeaf:
                for pattern_index in node_up.leafPatternNumber:
                    j = i - len(patterns[pattern_index]) + 1
                    results.append((j, pattern_index))
                    print(f"Найден паттерн №{pattern_index} - {patterns[pattern_index]}, который начинается с индекса {j}")
            print(f"Переход по сжатой суффиксной ссылке с вершины с id = {node_up.id} на вершину с id = {node_up.up.id}")
            node_up = node_up.up

    return results


if __name__ == "__main__":
    text = input()
    n = int(input())
    patterns = []
    for i in range(n):
        patterns.append(input())
    root = build_aho_corasick(patterns)
    results = process_text(text, root, patterns)
    result_sorted = sorted(results, key=lambda x: (x[0], x[1]))

    print("Найденные образцы:")
    for position, pattern_index in result_sorted:
        print(f"{position + 1} {pattern_index + 1}")
