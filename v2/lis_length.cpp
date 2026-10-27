#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;
int main() {
    int n;
    if (!(cin >> n) || n < 0 || n > 200000) return 1;
    vector<long long> tails;
    for (int i=0;i<n;++i) {
        long long x;
        if (!(cin>>x) || x < -1000000000LL || x > 1000000000LL) return 1;
        auto it=lower_bound(tails.begin(),tails.end(),x);
        if (it==tails.end()) tails.push_back(x);
        else *it=x;
    }
    cout << tails.size() << '\n';
}
