import math
from heapq import heappush, heappop
from matrix import *


class Node:
    def __init__(self, matrix, bound, route):
        self.matrix = matrix  # Матрица стоимостей
        self.bound = bound  # Нижняя граница стоимости
        self.route = route  # Частичный маршрут (список кортежей (i, j))

    def __lt__(self, other):
        return self.bound < other.bound

    def __str__(self):
        return f"Узел с частичным маршрутом {self.route} и нижней границей стоимости {self.bound}"

    @staticmethod
    def clone_matrix(matrix):
        return [row.copy() for row in matrix]

    @staticmethod
    def reduce(matrix):
        print("РЕДУКЦИЯ:")
        print("Матрица до редукции:")
        print_matrix(matrix)
        n = len(matrix)
        total_reduction = 0
        print("Выполнение редукции по строкам...")
        for i in range(n):
            try:
                min_val = min(x for x in matrix[i] if not math.isinf(x))
            except ValueError:
                min_val = 0
            print(f"Минимальное значение в строке {i} = {min_val}")
            if min_val > 0:
                for j in range(n):
                    if not math.isinf(matrix[i][j]):
                        matrix[i][j] -= min_val
                total_reduction += min_val
        print("Выполнение редукции по столбцам...")
        for j in range(n):
            try:
                min_val = min(matrix[i][j] for i in range(n) if not math.isinf(matrix[i][j]))
            except ValueError:
                min_val = 0
            print(f"Минимальное значение в столбце {j} = {min_val}")
            if min_val > 0:
                for i in range(n):
                    if not math.isinf(matrix[i][j]):
                        matrix[i][j] -= min_val
                total_reduction += min_val
        print("Матрица после редукции:")
        print_matrix(matrix)
        print(f"Сумма минимумов = {total_reduction}")
        return total_reduction

    def get_cell_with_max_penalty(self):
        max_penalty = -1
        best_cell = None
        print("Нахождение ячейки с максимальным штрафом")
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] == 0:
                    # Вычисляем штраф как сумму минимальных элементов в строке и столбце (исключая текущий 0)
                    try:
                        row_min = min(x for k, x in enumerate(self.matrix[i]) if k != j and not math.isinf(x))
                    except ValueError:
                        row_min = 0

                    try:
                        col_min = min(self.matrix[k][j] for k in range(len(self.matrix)) if
                                      k != i and not math.isinf(self.matrix[k][j]))
                    except ValueError:
                        col_min = 0
                    penalty = row_min + col_min
                    print(
                    f"Для ячейки [{i},{j}] минимальный элемент в строке {row_min}, минимальный элемент в столбце {col_min}, тогда штраф = {penalty}")
                    if penalty > max_penalty:
                        max_penalty = penalty
                        best_cell = (i, j, penalty)
        print(f"Итог: максимальный штраф = {max_penalty} у ячейки [{best_cell[0]},{best_cell[1]}]")
        return best_cell


def find_next_start_city(edges, start_city):
    for i, edge in enumerate(edges):
        if edge[1] == start_city:
            return i
    return -1


def find_next_end_city(edges, end_city):
    for i, edge in enumerate(edges):
        if edge[0] == end_city:
            return i
    return -1


def get_close_edges(route):
    result = []
    edges = route.copy()

    while edges:
        length = 1
        start_city = edges[0][0]
        end_city = edges[0][1]
        edges.pop(0)

        index = find_next_start_city(edges, start_city)
        while index != -1:
            length += 1
            start_city = edges[index][0]
            edges.pop(index)
            index = find_next_start_city(edges, start_city)

        index = find_next_end_city(edges, end_city)
        while index != -1:
            length += 1
            end_city = edges[index][1]
            edges.pop(index)
            index = find_next_end_city(edges, end_city)

        if length >= 2:
            result.append((end_city, start_city))

    return result


def prepare_matrix_for_mst(matrix, route):
    current_matrix = [row.copy() for row in matrix]
    current_transitions = [int(x) for x in range(len(matrix))]
    for path in route:
        i, j = path[0], path[1]
        print(f"Стягиваем ребро {i} -> {j} в одну вершину...")
        i = current_transitions[i]
        j = current_transitions[j]
        current_matrix, current_transitions = merge_vertices(current_matrix, i, j, current_transitions)
    return current_matrix, current_transitions


def merge_vertices(matrix, i, j, old_transitions):
    n = len(matrix)
    if i == j or i >= n or j >= n:
        return matrix

    new_size = n - 1
    new_matrix = [[math.inf] * new_size for _ in range(new_size)]

    merged_idx = min(i, j)

    for new_row in range(new_size):
        for new_column in range(new_size):
            if (new_row < merged_idx or merged_idx < new_row < max(i,j)) and (new_column < merged_idx or merged_idx < new_column < max(i,j)):
                new_matrix[new_row][new_column] = matrix[new_row][new_column]
            elif (new_row < merged_idx or merged_idx < new_row < max(i,j)) and new_column == merged_idx:
                new_matrix[new_row][new_column] = matrix[new_row][i]
            elif (new_row < merged_idx or merged_idx < new_row < max(i,j)) and new_column >= max(i,j):
                new_matrix[new_row][new_column] = matrix[new_row][new_column + 1]
            elif new_row == merged_idx and (new_column < merged_idx or merged_idx < new_column < max(i,j)):
                new_matrix[new_row][new_column] = matrix[j][new_column]
            elif new_row == merged_idx and new_column == merged_idx:
                new_matrix[new_row][new_column] = math.inf
            elif new_row == merged_idx and new_column >= max(i,j):
                new_matrix[new_row][new_column] = matrix[j][new_column + 1]
            elif new_row >= max(i,j) and (new_column < merged_idx or merged_idx < new_column < max(i,j)):
                new_matrix[new_row][new_column] = matrix[new_row + 1][new_column]
            elif new_row >= max(i, j) and new_column == merged_idx:
                new_matrix[new_row][new_column] = matrix[new_row + 1][i]
            elif new_row >= max(i, j) and new_column >= max(i,j):
                new_matrix[new_row][new_column] = matrix[new_row + 1][new_column + 1]
    new_transitions = old_transitions.copy()
    for k in range(len(new_transitions)):
        if new_transitions[k] == max(i,j):
            new_transitions[k] = merged_idx
        if new_transitions[k] > max(i,j):
            new_transitions[k] -= 1
    return new_matrix, new_transitions


def process_transitions(transitions):
    num = set(transitions)
    result = [""]*len(num)
    for i in range(len(transitions)):
        result[transitions[i]] += str(i)
    return result


def minimum_spanning_tree(matrix, transitions_v):
    vertices = set(int(x) for x in range(len(matrix)))
    if len(vertices) <= 1:
        return 0.0

    total_cost = 0.0
    visited = set()
    start = next(iter(vertices))
    print("Построение МОД:")
    priority_queue = [(0.0, start)]

    while priority_queue and len(visited) < len(vertices):
        weight, u = heappop(priority_queue)
        print(f"Извлекаем из очереди вершину {transitions_v[u]} с весом {weight}")
        if u in visited:
            print("Вершина уже отмечена как посещенная, переходим к следующей...")
            continue
        total_cost += weight
        print(f"Итовую строимость увеличиваем на {weight} и получаем стоимость = {total_cost}")
        visited.add(u)
        for v in vertices - visited:
            edge_weight = matrix[u][v]
            if edge_weight != math.inf:
                print(f"Добавляем смежную вершину {transitions_v[v]} с весом перехода {edge_weight} в очередь")
                heappush(priority_queue, (edge_weight, v))
    print(f"Итоговый вес МОД: {total_cost}")
    return total_cost if len(visited) == len(vertices) else math.inf

def make_children(min_node):
    row, column, left_penalty = min_node.get_cell_with_max_penalty()
    print("\nСОЗДАНИЕ ЛЕВОГО ПОТОМКА...")
    print(f"В левом потомке исключаем дугу {row} -> {column}")
    left_matrix = [row.copy() for row in min_node.matrix]
    left_matrix[row][column] = math.inf
    Node.reduce(left_matrix)
    left_bound = min_node.bound + left_penalty
    left_route = min_node.route.copy()
    left_child = Node(left_matrix, left_bound, left_route)
    print(f"ИТОГ: Для маршрута {left_route}, не проходящего через дугу {row} -> {column} нижняя оценка длины маршрута = {left_bound}")

    print("\nСОЗДАНИЕ ПРАВОГО ПОТОМКА...")
    print(f"В маршрут правого потомка включаем дугу {row} -> {column}")
    right_matrix = [row.copy() for row in min_node.matrix]
    print(f"Запрещаем обратную дугу {column} -> {row}")
    right_matrix[column][row] = math.inf
    print(f"Запрещаем выезжать из города {row} и въезжать в город {column}, то есть дуги ", end="")
    for i in range(len(right_matrix)):
        right_matrix[row][i] = math.inf
        right_matrix[i][column] = math.inf
        print(f"{row} -> {i}, {i} -> {column}", end="")
        if i != len(right_matrix):
            print(", ", end="")
    right_route = min_node.route.copy()
    right_route.append((row, column))
    close_edges = get_close_edges(right_route)
    print(f"\nЗапрещаем дуги, которые могут создать подциклы, то есть дуги ", end="")
    for curr_row, curr_edge in close_edges:
        right_matrix[curr_row][curr_edge] = math.inf
        print(f"{curr_row} -> {curr_edge}; ", end="")
    print()
    right_penalty = Node.reduce(right_matrix)
    print("ДОБАВЛЕНИЕ ОЦЕНКИ НА ОСНОВЕ МОД")
    matrix_for_mst, transitions = prepare_matrix_for_mst(right_matrix, right_route)
    vertices = process_transitions(transitions)
    print("Матрица для построения МОД:")
    print_matrix(matrix_for_mst)
    mst_bound = minimum_spanning_tree(matrix_for_mst, vertices)
    right_bound = min_node.bound + right_penalty + mst_bound
    right_child = Node(right_matrix, right_bound, right_route)
    print(f"ИТОГ: Для маршрута {left_route}, проходящего через дугу {row} -> {column} нижняя оценка длины маршрута = {right_bound}")
    return left_child, right_child


def little_algorithm(matrix):
    root_matrix = Node.clone_matrix(matrix)
    min_bound = Node.reduce(root_matrix)
    root = Node(root_matrix, min_bound, [])
    print(f"Создаем начальный узел, соответствующий пустому маршруту с нижней оценкой длины маршрута {min_bound}")
    priority_queue = []
    heappush(priority_queue, (root.bound, root))

    record = None

    while priority_queue:
        print(f"\nИзвлекаем из очереди с приоритетом узел с наименьшей нижней оценкой длины маршрута:")
        _, min_node = heappop(priority_queue)
        print(f"ТЕКУЩИЙ УЗЕЛ: min_node")

        if record is not None and record['length'] <= min_node.bound:
            print(f"Нижняя оценка текущего маршрута больше, чем существующее решение-рекорд, поэтому переходим дальше...")
            continue

        # Если маршрут почти завершен (n-2 ребра)
        if len(min_node.route) == len(matrix) - 2:
            print("Маршрут почти завершен, добавляем последние два ребра ", end="")
            for row in range(len(matrix)):
                for column in range(len(matrix)):
                    if not math.isinf(min_node.matrix[row][column]):
                        print(f"{row}->{column}, ", end="")
                        min_node.bound += min_node.matrix[row][column]
                        min_node.route.append((row, column))
            print()

            if record is None or record['length'] > min_node.bound:
                if record:
                    print(f"Длина текущего маршрута, равная {min_node.bound} оказалась меньше длины решения-рекорда, равной {record['length']}. Обновляем рекорд...")
                else:
                    print("Получили первый маршрут, проходящий через все города, и приравниваем его к рекорду...")
                print(f"Новый рекорд - маршрут {min_node.route} с длиной {min_node.bound}")
                record = {'length': min_node.bound, 'route': min_node.route}
        else:
            print(f"Создание потомков узла...")
            left_child, right_child = make_children(min_node)

            # Добавляем потомков в очередь
            heappush(priority_queue, (left_child.bound, left_child))
            heappush(priority_queue, (right_child.bound, right_child))

    return record


def format_route(route, n):
    if not route:
        return []

    route_map = {}
    for u, v in route:
        route_map[u] = v

    # Начинаем с города 0
    current = 0
    ordered_route = [current]

    # Строим маршрут по цепочке
    while len(ordered_route) < n:
        current = route_map.get(current)
        if current is None:
            break
        ordered_route.append(current)

    return ordered_route

if __name__ == "__main__":
    n = int(input())
    cost_matrix = []
    for i in range(n):
        row = list(map(int,input().split()))
        row[i] = math.inf
        cost_matrix.append(row)
    result = little_algorithm(cost_matrix)
    if result:
        n = len(cost_matrix)
        ordered_route = format_route(result['route'], n)

        print(" ".join(map(str, ordered_route)))
        print(float(result['length']))
