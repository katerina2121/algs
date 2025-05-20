import math


def nearest_neighbor_algorithm(start: int, distance_matrix: list):
    num_cities = len(distance_matrix)
    unvisited = set(range(num_cities))
    print(f'Начинаем путь с вершины №{start}')
    unvisited.remove(start)

    total_cost = 0
    path = [start]
    current_city = start

    iteration = 1
    while unvisited:
        print(f'Итерация №{iteration}')

        # Находим ближайший непосещенный город
        nearest_city = None
        min_distance = math.inf

        for city in unvisited:
            distance = distance_matrix[current_city][city]
            print(f'Расстояние от города №{current_city} до города №{city} = {distance}')
            if 0 < distance < min_distance:
                nearest_city = city
                min_distance = distance

        if nearest_city is None:
            break

        unvisited.remove(nearest_city)
        path.append(nearest_city)
        total_cost += min_distance
        current_city = nearest_city

        print(f'Выбран путь {path[-2]} → {nearest_city}, длина: {min_distance}')
        print(f'Текущий путь: {path}, общая стоимость: {total_cost}\n')
        iteration += 1

    # Возвращаемся в начальный город
    return_cost = distance_matrix[current_city][start]
    if not math.isinf(return_cost) and return_cost > 0:
        total_cost += return_cost
        path.append(start)
        print(f'Возвращаемся в начальный город: {current_city} → {start}, длина: {return_cost}')

    print('Решение найдено!')
    return total_cost, path


if __name__ == "__main__":
    n = int(input())
    cost_matrix = []
    for i in range(n):
        row = list(map(int, input().split()))
        row[i] = math.inf
        cost_matrix.append(row)
    start = 0
    cost, way = nearest_neighbor_algorithm(start, cost_matrix)
    print(f"Длина пути: {cost}")
    print(f"Путь: {way[0]}", end="")

