// Original festival exercise: n, then n rows of swap endpoints and guess.
// Labels 1..3. Swap BEFORE scoring. stdin/stdout adaptation of the pattern.
#include <array>
#include <algorithm>
#include <iostream>
#include <vector>
int main() {
    int n;
    if (!(std::cin>>n) || n<0 || n>100000) return 1;
    std::vector<std::array<int,3>> events(n);
    for (auto &e:events) {
        if (!(std::cin>>e[0]>>e[1]>>e[2])) return 1;
        for (int x:e) if (x<1 || x>3) return 1;
        if (e[0]==e[1]) return 1;
    }
    int best=0;
    for (int start=1;start<=3;++start) {
        int position=start,score=0;
        for (auto [a,b,guess]:events) {
            if (position==a) position=b;
            else if (position==b) position=a;
            if (position==guess) ++score;
        }
        best=std::max(best,score);
    }
    std::cout<<best<<'\n';
}
