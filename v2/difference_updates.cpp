// n q, then q additions l r x on half-open [l,r), initially all zeros.
// 0<=n,q<=100000, |x|<=10^9. Stop boundary n is a valid sentinel.
#include <iostream>
#include <vector>
int main() {
  int n, q;
  if (!(std::cin >> n >> q) || n < 0 || n > 100000 || q < 0 || q > 100000)
    return 1;
  std::vector<long long> diff(n + 1, 0);
  for (int i = 0; i < q; ++i) {
    int l, r;
    long long x;
    if (!(std::cin >> l >> r >> x) || l < 0 || l > r || r > n ||
        x < -1000000000LL || x > 1000000000LL)
      return 1;
    diff[l] += x;
    diff[r] -= x;
  }
  long long active = 0;
  for (int i = 0; i < n; ++i) {
    active += diff[i];
    std::cout << (i ? " " : "") << active;
  }
  std::cout << '\n';
}
