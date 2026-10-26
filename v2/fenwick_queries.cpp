// n q, then n values; A index delta or S l r (half-open).
// n,q<=100000; initial values/deltas have magnitude<=10^9.
#include <iostream>
#include <vector>
struct Fenwick {
  int n;
  std::vector<long long> bit;
  explicit Fenwick(int size) : n(size), bit(size + 1, 0) {}
  void add(int index, long long delta) {
    for (int i = index + 1; i <= n; i += i & -i)
      bit[i] += delta;
  }
  long long prefix(int boundary) const {
    long long sum = 0;
    for (int i = boundary; i > 0; i -= i & -i)
      sum += bit[i];
    return sum;
  }
  long long sum(int l, int r) const { return prefix(r) - prefix(l); }
};
int main() {
  int n, q;
  if (!(std::cin >> n >> q) || n < 0 || n > 100000 || q < 0 || q > 100000)
    return 1;
  Fenwick tree(n);
  for (int i = 0; i < n; ++i) {
    long long x;
    if (!(std::cin >> x) || x < -1000000000LL || x > 1000000000LL)
      return 1;
    tree.add(i, x);
  }
  for (int j = 0; j < q; ++j) {
    char kind;
    if (!(std::cin >> kind))
      return 1;
    if (kind == 'A') {
      int i;
      long long delta;
      if (!(std::cin >> i >> delta) || i < 0 || i >= n ||
          delta < -1000000000LL || delta > 1000000000LL)
        return 1;
      tree.add(i, delta);
    } else if (kind == 'S') {
      int l, r;
      if (!(std::cin >> l >> r) || l < 0 || l > r || r > n)
        return 1;
      std::cout << tree.sum(l, r) << '\n';
    } else
      return 1;
  }
}
