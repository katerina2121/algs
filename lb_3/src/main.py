import sys


def distance_between_prefixes(i: int, j: int, str1: str, str2: str, current_row: list, previous_row: list,
                              cost_replace: int, cost_insert: int, cost_delete: int, cost_replace2: int) -> int:
    replace2_cost = sys.maxsize
    replace2_possible = False

    if i >= 2:
        replace2_cost = previous_row[i - 2] + cost_replace2
        replace2_possible = True

    insertion_cost = previous_row[i] + cost_insert
    deletion_cost = current_row[i - 1] + cost_delete

    if str1[i - 1] == str2[j - 1]:
        substitution_cost = previous_row[i - 1]
    else:
        substitution_cost = previous_row[i - 1] + cost_replace

    # Формируем вывод
    output_lines = [
        f"Для префиксов строки 1 до {i} символа (i = {i}) и строки 2 до {j} символа (j = {j}):",
        f"  стоимость, если последняя операция вставка = {insertion_cost}",
        f"  стоимость, если последняя операция удаление = {deletion_cost}",
        f"  стоимость, если последняя операция замена = {substitution_cost}"
    ]

    # Добавляем информацию о replace2_cost только если операция возможна
    if replace2_possible:
        output_lines.append(f"  стоимость, если последняя операция замена двух символов на один = {replace2_cost}")
    else:
        output_lines.append("  операция замены двух символов на один невозможна")

    min_cost = min(insertion_cost, deletion_cost, substitution_cost, replace2_cost)
    output_lines.append(f"МИНИМАЛЬНАЯ СТОИМОСТЬ = {min_cost}\n")

    # Промежуточный вывод
    print('\n'.join(output_lines))
    return min_cost


def editorial_distance(str1: str, str2: str, cost_replace: int, cost_insert: int, cost_delete: int, cost_replace2: int) -> int:
    len1, len2 = len(str1), len(str2)
    current_row = [cost_delete * x for x in range(1 + len1)]
    print("Заполнение первой строки матрицы редакционных расстояний(операция удаления)")
    print("Первая строка: " + ' '.join(map(str,current_row)))
    for j in range(1, len2 + 1):
        previous_row = current_row
        current_row = [j * cost_insert]  + [0] * len1
        print(f"Для строки {j} первый столбец заполняется стоимостью операций вставки = {current_row[0]}")
        for i in range(1, len1 + 1):
            current_row[i] = distance_between_prefixes(i, j, str1, str2, current_row, previous_row, cost_replace, cost_insert, cost_delete, cost_replace2)
    print("ИТОГОВАЯ СТОИМОСТЬ ОПЕРАЦИЙ")
    return current_row[len1]


def sequence_of_operations(str1: str, str2: str, cost_replace: int, cost_insert: int, cost_delete: int, cost_replace2: int) -> str:
    len1, len2 = len(str1), len(str2)
    matrix = [[0] * (len1 + 1) for _ in range(len2 + 1)]
    print("Заполнение первой строки матрицы редакционных расстояний(операция удаления)")
    for i in range(len1 + 1):
        matrix[0][i] = i * cost_delete
    print("Первая строка: " + ' '.join(map(str,matrix[0])))

    print("Заполнение первого столбца матрицы редакционных расстояний(операция вставки)")
    column = ""
    for j in range(len2 + 1):
        matrix[j][0] = j * cost_insert
        column += str(matrix[j][0]) + " "
    print("Первый столбец: " + column + "\n")

    for j in range(1, len2 + 1):
        for i in range(1, len1 + 1):
            matrix[j][i] = distance_between_prefixes(i, j, str1, str2, matrix[j], matrix[j-1], cost_replace, cost_insert, cost_delete, cost_replace2)

    result = []

    list_str1 = [" ", " "] + list(str1)
    list_str2 = [" "] + list(str2)
    print("Получена матрица редакционных расстояний")
    print(" ".join(list_str1))
    for j in range(len2 + 1):
        string_matrix = f"{list_str2[j]} "
        for i in range(len1 + 1):
            string_matrix += str(matrix[j][i]) + " "
        print(string_matrix)

    print("\nВосстановление операций, начиная с конца")
    i, j = len1, len2
    while i > 0 or j > 0:
        if i == 0:
            result.append('I')
            j -= 1
            print(f"Операция: вставка(I), перемещаемся на позицию j = {j} i = {i}")
        elif j == 0:
            result.append('D')
            i -= 1
            print(f"Операция: удаление(D), перемещаемся на позицию j = {j} i = {i}")
        else:
            current = matrix[j][i]
            if str1[i - 1] == str2[j - 1] and current == matrix[j - 1][i - 1]:
                result.append('M')
                i -= 1
                j -= 1
                print(f"Операция: совпадение(M), перемещаемся на позицию j = {j} i = {i}")
            elif current == matrix[j - 1][i - 1] + cost_replace:
                result.append('R')
                i -= 1
                j -= 1
                print(f"Операция: замена(R), перемещаемся на позицию j = {j} i = {i}")
            elif i >= 2 and current == matrix[j - 1][i - 2] + cost_replace2:
                result.append('T')
                i -= 2
                j -= 1
                print(f"Операция: замена двух символов на один(Т), перемещаемся на позицию j = {j} i = {i}")
            elif current == matrix[j][i - 1] + cost_delete:
                result.append('D')
                i -= 1
                print(f"Операция: удаление(D), перемещаемся на позицию j = {j} i = {i}")
            else:
                result.append('I')
                j -= 1
                print(f"Операция: вставка(I), перемещаемся на позицию j = {j} i = {i}")

    print("\nИТОГОВАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ ОПЕРАЦИЙ")
    return ''.join(reversed(result))

if __name__ == "__main__":
    print("Редакционное расстояние - нахождение минимальной стоимости операций")
    cost_replace, cost_insert, cost_delete, cost_replace2 = map(int, input().split(' '))
    str1 = input()
    str2 = input()
    print(editorial_distance(str1, str2, cost_replace, cost_insert, cost_delete, cost_replace2))
    print("\nРедакционное расстояние - нахождение последовательности операций")
    print(sequence_of_operations(str1, str2, cost_replace, cost_insert, cost_delete, cost_replace2))

