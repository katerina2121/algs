from nearest_neighbor_algorithm import *
from little_algorithm import *
from matrix import *

if __name__ == "__main__":
    filename = "matrix.txt"
    print("Загрузить матрицу весов из файла? y/n")
    answer = input()
    flag_generate = True
    if answer == "y":
        try:
            dist_matrix = read_matrix_from_file(filename)
            print("Успешно загружена матрица:")
            print_matrix(dist_matrix)
            flag_generate = False
        except (ValueError, FileNotFoundError) as e:
            print("Не удалось загрузить, сгенерируем новую")
    if flag_generate:
        print("Введите размерность матрицы: ")
        n = int(input())
        print("Генерировать симметричную матрицу? y/n")
        answer = input()
        is_sym = True if answer == "y" else False
        print("Сгенерированная матрица:")
        dist_matrix = generate_weight_matrix(n, is_sym, 20)
        print_matrix(dist_matrix)
        print(f"Сохранить матрицу в файл {filename}? y/n")
        answer = input()
        if answer == "y":
            write_matrix_to_file(dist_matrix, filename)
            print("Матрица сохранена!")

    start = 0
    print("\033[3m\033[36m{}\033[0m".format("\nПРИБЛИЖЕННЫЙ АЛГОРИТМ: АЛГОРИТМ БЛИЖАЙШЕГО СОСЕДА"))
    cost, way = nearest_neighbor_algorithm(start, dist_matrix)
    print(f"Длина пути: {cost}")
    print(f"Путь: {way[0]}", end="")
    for i in range(1, len(way)):
        print('-', way[i], end='', sep='')
    print("\033[3m\033[36m{}\033[0m".format("\n\nТОЧНЫЙ АЛГОРИТМ: АЛГОРИТМА ЛИТТЛА С МОДИФИКАЦИЕЙ"))
    result = little_algorithm(dist_matrix)
    if result:
        n = len(dist_matrix)
        ordered_route = format_route(result['route'], n)
        print(f"Длина пути: {result['length']}")
        route = " ".join(map(str, ordered_route))
        print(f"Путь: {route}")
