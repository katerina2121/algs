#include <iostream>
#include <vector>
#include <string>

#define RED "\033[1;31m"
#define BASIC "\033[0m"

using namespace std;

vector<int> prefixFunction(const string& s) {
    cout << "Вычисление префикс-функции - массивa p, где p[i] - длина наибольшего собственного префикса подстроки s[0...i], совпадающего с её суффиксом:\n\n";
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
            cout << "То есть можно продолжить текущим символом префикс для p[" << i-1 << "]\n";
            index++;
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

vector<int> search(string &pat, string &txt) {
    int n = txt.length();
    int m = pat.length();
    vector<int> res;

    vector<int> prefix_array = prefixFunction(pat);

    cout << "Начинаем поиск подстроки " << pat << " в строке " << txt << "\n";
    int i = 0;
    int j = 0;
    cout << "Сравнение символов начинаем с начала строки и подстроки, то есть с нулевых индексов\n";
    while (i < n) {
        if (txt[i] == pat[j]) {
            cout << "Символ строки text[" << i << "] = " << txt[i] << " совпал с символом подстроки pattern[" << j << "] = " << pat[j] << "\n";
            i++;
            j++;
            cout << "Поэтому переходим к следующим символам в обеих строках: индекс в строке увеличиваем до " << i << ", индекс с подстроке - " << j << "\n";
            if (j == m) {
                cout << RED << "Вхождение подстроки найдено!!! Индекс начала подстроки в строке " << i - j << BASIC << "\n";
                res.push_back(i - j);
                j = prefix_array[j - 1];
                cout << "Индекс в подстроке сбрасываем до " << j << "\n";
            }
        }
        else {
            cout << "Символ строки text[" << i << "] = " << txt[i] << " НЕ совпал с символом подстроки pattern[" << j << "] = " << pat[j] << "\n";
            if (j != 0){
                j = prefix_array[j - 1];
                cout << "Индекс в подстроке сбрасываем до " << j << "\n";
            }else{
                i++;
                cout << "Переходим к следующему символу в строке\n";
            }
        }
    }
    cout << "Достигнут конец строки, поиск завершён\n";
    return res;
}


int main() {
    string pattern, text;
    cin >> text;
    cin >> pattern;

    vector<int> res = search(pattern, text);
    if (res.empty()) {
        cout << -1 << endl;
    } else {
        for (size_t i = 0; i < res.size(); ++i) {
            cout << res[i];
            if (i < res.size() - 1) {
                cout << ",";
            }
        }
        cout << endl;
    }
    return 0;
}


