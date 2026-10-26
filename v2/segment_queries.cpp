// n q, initial values; X index newValue or S l r (half-open).
// n,q<=100000; values magnitude<=10^9. Point assignment, range sum.
#include <iostream>
#include <vector>
struct SegmentSum {
  int base = 1;
  std::vector<long long> tree;
  explicit SegmentSum(const std::vector<long long> &a) {
    while (base < static_cast<int>(a.size()))
      base *= 2;
    tree.assign(2 * base, 0);
    for (int i = 0; i < static_cast<int>(a.size()); ++i)
      tree[base + i] = a[i];
    for (int i = base - 1; i > 0; --i)
      tree[i] = tree[2 * i] + tree[2 * i + 1];
  }
  void assign(int index, long long value) {
    int p = base + index;
    tree[p] = value;
    for (p /= 2; p > 0; p /= 2)
      tree[p] = tree[2 * p] + tree[2 * p + 1];
  }
  long long sum(int l, int r) const {
    long long answer = 0;
    for (l += base, r += base; l < r; l /= 2, r /= 2) {
      if (l & 1)
        answer += tree[l++];
      if (r & 1)
        answer += tree[--r];
    }
    return answer;
  }
};
int main() {
  int n, q;
  if (!(std::cin >> n >> q) || n < 0 || n > 100000 || q < 0 || q > 100000)
    return 1;
  std::vector<long long> a(n);
  for (auto &x : a)
    if (!(std::cin >> x) || x < -1000000000LL || x > 1000000000LL)
      return 1;
  SegmentSum tree(a);
  for (int j = 0; j < q; ++j) {
    char kind;
    if (!(std::cin >> kind))
      return 1;
    if (kind == 'X') {
      int i;
      long long x;
      if (!(std::cin >> i >> x) || i < 0 || i >= n || x < -1000000000LL ||
          x > 1000000000LL)
        return 1;
      tree.assign(i, x);
    } else if (kind == 'S') {
      int l, r;
      if (!(std::cin >> l >> r) || l < 0 || l > r || r > n)
        return 1;
      std::cout << tree.sum(l, r) << '\n';
    } else
      return 1;
  }
}
