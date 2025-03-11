#include <iostream>
#include <vector>
#include <time.h>

class Square{
public:
    int x;
    int y;
    int size;
    Square(int x, int y, int size) : x(x), y(y), size(size) {};
    friend std::ostream& operator<<(std::ostream& os, const Square& square){
    	os << "Квадрат с координатами верхнего левого угла x = " << square.x << ", y = " << square.y << " и размером стороны  " << square.size;
    	return os;
	}
};

class Desk {
public:
    int N; // Размер сетки
    int num_occupied; // количество занятых ячеек
    bool** occupied; // Динамический массив для хранения состояния ячеек
    
    // Конструктор
    Desk(int n) : N(n), num_occupied(0) {
        // Инициализация двумерного массива
        occupied = new bool*[N];
        for (int i = 0; i < N; ++i) {
            occupied[i] = new bool[N]{false}; // Инициализируем все ячейки как свободные
        }
    }
    
    // Деструктор
    ~Desk() {
        for (int i = 0; i < N; ++i) {
            delete[] occupied[i]; // Освобождаем память
        }
        delete[] occupied;
    }
    
    void placeSquare(const Square& square) {
        if (square.x + square.size > N || square.y + square.size > N) {
            throw std::out_of_range("Square exceeds desk boundaries");
        }
        for (int i = square.x; i < square.x + square.size; ++i) {
            for (int j = square.y; j < square.y + square.size; ++j) {
                occupied[i][j] = true;
                ++num_occupied;
            }
        }
    }
    
    void removeSquare(const Square& square) {
        if (square.x + square.size > N || square.y + square.size > N) {
            throw std::out_of_range("Square exceeds desk boundaries");
        }
        for (int i = square.x; i < square.x + square.size; ++i) {
            for (int j = square.y; j < square.y + square.size; ++j) {
                occupied[i][j] = false;
                --num_occupied;
            }
        }
    }
    
    bool canPlace(int x, int y, int size) const {
        if (x + size > N || y + size > N) {
            return false;
        }
        for (int i = x; i < x + size; ++i) {
            for (int j = y; j < y + size; ++j) {
                if (occupied[i][j])
                    return false;
            }
        }
        return true;
    }

    // Проверка на заполненность (все ячейки)
    bool isFull() const {
        return num_occupied == N * N; 
    }
    
    // Нахождение максимального пустого квадрата, который можно вставить
    Square findEmptySquare() {
        // Найдем первую(наиболее верхнюю и левую) свободную ячейку
        int firstEmptyX = -1, firstEmptyY = -1;
        for (int i = 0; i < N; ++i){
            for (int j = 0; j < N; ++j){
                if (!occupied[i][j]){
                    firstEmptyX = i;
                    firstEmptyY = j;
                    break;
                }
            }
            if (firstEmptyX != -1) break;
        }
        // Если есть хотя бы одна пустая клетка, то пытаемся вставить квадрат наибольшего размера
        int maxCoord, possibleSide;
        if (firstEmptyX != -1 && firstEmptyY != -1){
            maxCoord = std::max(firstEmptyX, firstEmptyY);
            possibleSide = N - maxCoord;
            while (!canPlace(firstEmptyX, firstEmptyY, possibleSide)){
                --possibleSide;
            }
            return {firstEmptyX, firstEmptyY,possibleSide};
        }
        return {0, 0, 0};
    }
    friend std::ostream& operator<<(std::ostream& os, const Desk& desk){
        for (int i = 0; i < desk.N; ++i){
            for (int j = 0; j < desk.N; ++j){
                os << desk.occupied[i][j] << ' ';
            }
            os << std::endl;
        }
        return os;
    }
};

class State{
public:
    std::vector<Square> currentResult; //уже добавленные квадраты
    Desk currentDesk; // текущее состояние занятости доски
    int minSquares;  // текущее минимальное количество квадратов
    std::vector<Square> bestResult; //квадраты,участвующие в расстановке, соответствующей minSquares

    State(int N) : currentDesk(Desk(N)), minSquares(N * N + 1), currentResult({}), bestResult({}) {}

    void addSquare(Square square){
        currentDesk.placeSquare(square);
        currentResult.push_back(square);
        std::cout << "Добавлено:" << square << std::endl;
    }

    void removeLastSquare(){
        std::cout << "Удалено:" << currentResult.back() << std::endl;
        currentDesk.removeSquare(currentResult.back());
        currentResult.pop_back();
    }

    std::vector<Square> find_solution(){
        //Оптимизация 1 - для любого квадрата со стороной - простым числом(он в мктод всегда таким уже подаётся) заранее ставим оптимальные 3 квадрата
        int lsize = (currentDesk.N + 1) / 2, ssize = (currentDesk.N) / 2;
        addSquare({0, 0, lsize});
        addSquare({lsize, 0, ssize});
        addSquare({0, lsize, ssize});
        bool flag = true;
        while (currentResult.size() > 3 || flag){
            flag = false;
            while (!currentDesk.isFull()){
                // Оптимизация - отсечение заведомо проигрышного решения
                if (currentResult.size() >= minSquares){
                    break;
                    std::cout << "Текущее решение хуже имеющегося лучшего\n";
                } 
                // Оптимизация 2 - нахождение наибольшего свободного квадрата
                Square finding_square = currentDesk.findEmptySquare();
                addSquare(finding_square);
            }
             
            // Оставляем лучший результат из текущего и имеющегося лучшего
            if (currentResult.size() < minSquares) {
                std::cout << "Текущий результат оказался лучше - было " <<  minSquares << " квадратов в расстановке,стало - " << currentResult.size() << "\n";
                minSquares = currentResult.size();
                bestResult = currentResult;
            }
            std::cout << *this;
            removeLastSquare();

            // Убираем все квадраты со стороной 1, потому что их никак не уменьшить
            while (!currentResult.empty() && currentResult[currentResult.size()-1].size == 1){
                removeLastSquare();
            }
            //Если возможно, то у последнего не единичного квадрата у меньшаем сторону на 1 и дальшем рассматриваем такой вариант
            if (currentResult.size() > 3){
                Square last_square = currentResult.back();
                currentDesk.removeSquare(last_square);
                currentDesk.placeSquare({last_square.x, last_square.y, last_square.size - 1});
                currentResult[currentResult.size()-1].size -= 1;
                std::cout << "У квадрата с координатами x = " << currentResult.back().x << ", y = " << currentResult.back().y << " уменьшаем сторону на 1 и она становится равна: " << currentResult.back().size << std::endl;
            }
        }
        return bestResult;
    }
    friend std::ostream& operator<<(std::ostream& os, const State& state){
        os << "\nОдно из решений:\n";
        os << "Минимальное количество квадратов: " << state.minSquares << "\n";
        os << "Текущие рассматриваемые квадраты:\n";
        int N = 1;
        for (const auto& square : state.currentResult) {
            os << N << ") " << square << "\n"; // Использует оператор вывода для класса Square
            ++N;
        }
        os << "\n";
        return os;
    }
    
};

//Функция нахождения первого простого делителя,кроме 1
int firstDivisor(int N) {
    for (int d = 2; d * d <= N; ++d) {
        if (N % d == 0) return d;
    }
    return N;
}


int main() {
    int N;
    std::cin >> N;
    if (N < 2 || N > 30){
        std::cout << "Wrong value of N.\n"; 
    }
    else{
        clock_t start = clock();
        int d = firstDivisor(N);
        //Коэффициент масштабирования
        int scale = N / d;

        State state(d);
        std::vector<Square> smallResult = state.find_solution();

        std::vector<Square> finalResult;
        //Полученный результат умножаем на коэфициент масштабирования и координаты сдвигаем на 1
        for (const auto& sq : smallResult) {
            finalResult.push_back({sq.x * scale + 1, sq.y * scale + 1, sq.size * scale});
        }

        std::cout << finalResult.size() << std::endl;
        for (const auto& sq : finalResult) {
            std::cout << sq.x << " " << sq.y << " " << sq.size << std::endl;
        }
        clock_t end = clock();
        double seconds = (double)(end - start) / CLOCKS_PER_SEC;
        //printf("The time: %f seconds\n", seconds);
    }
    return 0;
}

