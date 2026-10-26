// n nonnegative prices (<=10^9), n<=100000; sorted line, then sum/distinct count.
#include <algorithm>
#include <iostream>
#include <vector>
int main() {
  int n;
  if (!(std::cin >> n) || n < 0 || n > 100000) return 1;
  std::vector<int> prices(n);
  long long sum = 0;
  for (int &p : prices) {
    if (!(std::cin >> p) || p < 0 || p > 1000000000) return 1;
    sum += p;
  }
  std::sort(prices.begin(), prices.end());
  int distinct = 0;
  for (int i = 0; i < n; ++i) {
    if (i == 0 || prices[i] != prices[i - 1]) ++distinct;
    std::cout << (i ? " " : "") << prices[i];
  }
  std::cout << '\n' << sum << ' ' << distinct << '\n';
}
