// n limit then n nonnegative integers<=10^9; n<=100000,0<=limit<=10^14.
// Longest contiguous interval with sum<=limit; empty interval is allowed.
#include <algorithm>
#include <iostream>
#include <vector>
int main() {
  int n;
  long long limit;
  if (!(std::cin >> n >> limit) || n < 0 || n > 100000 || limit < 0 ||
      limit > 100000000000000LL)
    return 1;
  std::vector<long long> a(n);
  for (auto &x : a)
    if (!(std::cin >> x) || x < 0 || x > 1000000000LL)
      return 1;
  int left = 0, best = 0;
  long long sum = 0;
  for (int right = 0; right < n; ++right) {
    sum += a[right];
    while (sum > limit) {
      sum -= a[left];
      ++left;
    }
    best = std::max(best, right - left + 1);
  }
  std::cout << best << '\n';
}
