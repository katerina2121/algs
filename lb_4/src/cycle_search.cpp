#include <iostream>
#include <vector>
#include <string>

#define RED "\033[1;31m"
#define BASIC "\033[0m"

using namespace std;

vector<int> prefixFunction(const string& s) {
    cout << "Вычисление префикс-функции - массивa p, где p[i] - длина наибольшего собственного префикса подстроки s[0...i], совпадающего с её суффиксом.:\n\n";
    int n = s.length();
    vector<int> p(n);
    p[0] = 0;
    cout << "p[0] = 0, так как у первого символа есть только тривиальный префикс\n\n";
    for (int i = 1; i < n; ++i) {
        cout << "Вычисление p[" << i << "]\n";
        int index = p[i - 1];
        cout << "За начальный индекс для сравнения(index) возьмем длину наибольшего префикса подстроки s[0..." << i-1 << "], то есть p["<< i-1 <<"] = " << index << "\n";
        while (index > 0 && s[i] != s[index]) {
            cout << "Символ s[" << i << "] = " << s[i] << " НЕ совпал с символом s[" << index << "] = " << s[index] << "\n";
            cout << "Переходим к более короткому префиксу. За индекс сравнения принимаем предыдущее значение массива префикс-значений по индексу [index - 1] = " << p[index-1] << "\n";
            index = p[index - 1];
        }
        if (s[i] == s[index]) {
            cout << "Символ s[" << i << "] = " << s[i] << " совпал с символом s[" << index << "] = " << s[index] << "\n";
            cout << "То есть можно продолжить текущим символом префикс для p[" << i - 1 << "]\n";
            index++;
        } else {
            cout << "Символ s[" << i << "] = " << s[i] << " НЕ совпал с символом s[" << index << "] = " << s[index] << "\n";
        }
        if (index > 0){
            cout << "Был найден наибольший собственный префикс, совпадающий с суффиксом, длины " << index << "\n";
        } else {
            cout << "Подстрока не имеет собственного префикса, совпадающиего с суффиксом\n";
        }
        cout << "Следовательно, p[" << i << "] = " << index << "\n\n";
        p[i] = index;
    }
    return p;
}

int cycle_search(string &pat, string &txt){
    int n = txt.length();
    int m = pat.length();

    if (n!=m) return -1;

    n *= 2;
    int index = -1;

    vector<int> prefix_array = prefixFunction(pat);
    cout << "Определим является ли " << txt << " циклическим сдвигом строки " << pat << "\n";
    int i = 0;
    int double_i = 0;
    int j = 0;
    cout << "Сравнение символов начинаем с начала строки и подстроки, то есть с нулевых индексов\n";

    while (double_i < n) {
        i = double_i % m;
        if (txt[i] == pat[j]) {
            cout << "Символ строки A[" << i << "] = " << txt[i] << " совпал с символом строки B" << j << "] = " << pat[j] << "\n";
            double_i++;
            j++;
            cout << "Поэтому переходим к следующим символам в обеих строках: индекс в строке A увеличиваем до " << i << ", индекс с строке B - " << j << "\n";
            if (j == m) {
                index = double_i - j;
                cout << RED << "Строка A является циклическим сдвигом строки B! Индекс начала B в A - " << index << BASIC << "\n";
                break;
            }
        }
        else {
            cout << "Символ строки A[" << i << "] = " << txt[i] << " НЕ совпал с символом строки B" << j << "] = " << pat[j] << "\n";
            if (j != 0){
                j = prefix_array[j - 1];
                cout << "Индекс в строке B сбрасываем до " << j << "\n";
            }else{
                double_i++;
                cout << "Переходим к следующему символу в строке A\n";
            }
        }
    }
    cout << "Вся строка A просмотрена, алгоритм завершен\n";
    return index;

}

int main() {
    string B, A;
    cin >> A;
    cin >> B;

    int res = cycle_search(B, A);
    cout << res << endl;
    return 0;
}
