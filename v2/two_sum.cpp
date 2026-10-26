// n target, then n integers in [-2*10^9,2*10^9]; n<=200000.
// Print two distinct original 0-based positions, or NONE. Target is long long.
#include <algorithm>
#include <iostream>
#include <utility>
#include <vector>
int main() {
  int n;
  long long target;
  if (!(std::cin >> n >> target) || n < 0 || n > 200000)
    return 1;
  std::vector<std::pair<int, int>> a(n);
  for (int i = 0; i < n; ++i) {
    if (!(std::cin >> a[i].first) || a[i].first < -2000000000 ||
        a[i].first > 2000000000)
      return 1;
    a[i].second = i;
  }
  std::sort(a.begin(), a.end());
  int l = 0, r = n - 1;
  while (l < r) {
    long long sum = 1LL * a[l].first + a[r].first;
    if (sum == target) {
      std::cout << a[l].second << ' ' << a[r].second << '\n';
      return 0;
    }
    if (sum < target)
      ++l;
    else
      --r;
  }
  std::cout << "NONE\n";
}
