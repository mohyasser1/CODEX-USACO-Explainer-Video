#include <iostream>
#include <vector>
using namespace std;
int main() {
    int n, u, q;
    if (!(cin >> n >> u >> q) || n < 0 || n > 100000 || u < 0 || u > 10000 || q < 0 || q > 100000) return 1;
    vector<long long> a(n), diff(n + 1), prefix(n + 1);
    for (auto& x : a) if (!(cin >> x) || x < -1000000000LL || x > 1000000000LL) return 1;
    for (int j = 0; j < u; ++j) {
        int l, r; long long delta;
        if (!(cin >> l >> r >> delta) || l < 0 || l > r || r > n || delta < -1000000LL || delta > 1000000LL) return 1;
        diff[l] += delta; diff[r] -= delta;
    }
    long long active = 0;
    for (int i = 0; i < n; ++i) {
        active += diff[i]; a[i] += active;
        prefix[i + 1] = prefix[i] + a[i];
    }
    for (int j = 0; j < q; ++j) {
        int l, r;
        if (!(cin >> l >> r) || l < 0 || l > r || r > n) return 1;
        cout << prefix[r] - prefix[l] << '\n';
    }
}
