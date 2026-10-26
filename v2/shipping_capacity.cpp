// n d, then n nonnegative weights; keep order, no splitting, at most d groups.
// 1<=d<=n<=100000, each weight<=10^9. Print minimum feasible capacity.
#include <algorithm>
#include <iostream>
#include <vector>
bool feasible(const std::vector<long long> &weights, int allowed,
              long long capacity) {
  int days = 1;
  long long load = 0;
  for (long long w : weights) {
    if (w > capacity)
      return false;
    if (load + w > capacity) {
      ++days;
      load = 0;
    }
    load += w;
  }
  return days <= allowed;
}
int main() {
  int n, d;
  if (!(std::cin >> n >> d) || n < 1 || n > 100000 || d < 1 || d > n)
    return 1;
  std::vector<long long> a(n);
  long long lo = 0, hi = 0;
  for (auto &w : a) {
    if (!(std::cin >> w) || w < 0 || w > 1000000000LL)
      return 1;
    lo = std::max(lo, w);
    hi += w;
  }
  while (lo < hi) {
    long long mid = lo + (hi - lo) / 2;
    if (feasible(a, d, mid))
      hi = mid;
    else
      lo = mid + 1;
  }
  std::cout << lo << '\n';
}
