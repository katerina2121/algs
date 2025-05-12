from automat import *


def prepare_mask_pattern(pattern: str, wild_card: str):
    subpatterns = []
    start_index_subpatterns = []
    current_start = 0
    pattern += wild_card
    for i in range(len(pattern)):
        if pattern[i] == wild_card:
            if i > 0 and pattern[i-1] != wild_card:
                subpatterns.append(pattern[current_start:i])
                start_index_subpatterns.append(current_start + 1)
            current_start = i
        else:
            if pattern[i-1] == wild_card:
                current_start = i
    print(f"Из шаблона получили {len(subpatterns)} безмасочных куска: {' '.join(subpatterns)}, которые встречаются в шаблоне на позициях {' '.join(map(str,start_index_subpatterns))}")
    return subpatterns, start_index_subpatterns


def process_text_masks(text: str, root: Node, subpatterns: list[str], start_index_subpatterns: list[int], pattern_len: int):
    c = [0] * (len(text) + 1)
    cur = root
    print("\nПоиск в тексте шаблона...")
    for i, char in enumerate(text):
        last_id = cur.id
        cur = getLink(cur, char, root)
        print(f"\n{i}) Переход на символ в тексте {char} -> переход в автомате с вершины с id = {last_id} на вершину с id = {cur.id}")
        print("Проверка на соответствие подшаблону:")
        node_up = cur
        while node_up != root:
            if node_up.isLeaf:
                for pattern_index in node_up.leafPatternNumber:
                    j = i - len(subpatterns[pattern_index]) + 2
                    print(f"Найден подшаблон № {pattern_index} - {subpatterns[pattern_index]}, который начинается с индекса {j}")
                    l_i = start_index_subpatterns[pattern_index]
                    c[j - l_i + 1] += 1
            print(f"Переход по сжатой суффиксной ссылке с вершины с id = {node_up.id} на вершину с id = {node_up.up.id}")
            node_up = node_up.up

    for i in range(len(c)):
        if c[i] == len(subpatterns) and i + pattern_len - 1 <= len(text):
            print(f"\nШаблон начинается с индекса {i}")


if __name__ == "__main__":
    text = input()
    pattern = input()
    wild_card = input()
    subpatterns, start_index_subpatterns = prepare_mask_pattern(pattern, wild_card)
    root = build_aho_corasick(subpatterns)
    process_text_masks(text, root, subpatterns, start_index_subpatterns, len(pattern))