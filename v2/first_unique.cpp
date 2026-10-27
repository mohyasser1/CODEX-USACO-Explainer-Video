#include <array>
#include <iostream>
#include <string>
using namespace std;
int main() {
    string s;
    if (!getline(cin, s) || s.size() > 100000) return 1;
    array<int, 26> frequency{};
    for (char c : s) {
        if (c < 'A' || c > 'Z') return 1;
        ++frequency[c - 'A'];
    }
    for (int i = 0; i < static_cast<int>(s.size()); ++i) {
        if (frequency[s[i] - 'A'] == 1) {
            cout << i << '\n';
            return 0;
        }
    }
    cout << -1 << '\n';
}
