// n capacity, then n weight/value pairs. Each item may be used at most once.
// n<=100,capacity<=100000,1<=weight<=100000,0<=value<=10^9.
#include <algorithm>
#include <iostream>
#include <vector>
int main() {
  int n, capacity;
  if (!(std::cin >> n >> capacity) || n < 0 || n > 100 || capacity < 0 ||
      capacity > 100000)
    return 1;
  std::vector<long long> dp(capacity + 1, 0);
  for (int i = 0; i < n; ++i) {
    int weight;
    long long value;
    if (!(std::cin >> weight >> value) || weight < 1 || weight > 100000 ||
        value < 0 || value > 1000000000LL)
      return 1;
    for (int c = capacity; c >= weight; --c)
      dp[c] = std::max(dp[c], dp[c - weight] + value);
  }
  std::cout << dp[capacity] << '\n';
}
