// n target, then n positive denominations; unlimited copies of each.
// 1<=n<=100, 0<=target<=100000, 1<=coin<=1000000.
// Print minimum coin count and one choice, or -1 when impossible.
#include <algorithm>
#include <iostream>
#include <vector>
int main() {
  int n, target;
  if (!(std::cin >> n >> target) || n < 1 || n > 100 || target < 0 ||
      target > 100000)
    return 1;
  std::vector<int> coins(n);
  for (int &c : coins)
    if (!(std::cin >> c) || c < 1 || c > 1000000)
      return 1;
  const int inf = target + 1;
  std::vector<int> dp(target + 1, inf), last(target + 1, -1);
  dp[0] = 0;
  for (int amount = 1; amount <= target; ++amount) {
    for (int c : coins) {
      if (c <= amount && dp[amount - c] != inf &&
          dp[amount - c] + 1 < dp[amount]) {
        dp[amount] = dp[amount - c] + 1;
        last[amount] = c;
      }
    }
  }
  if (dp[target] == inf) {
    std::cout << "-1\n";
    return 0;
  }
  std::cout << dp[target] << '\n';
  bool first = true;
  for (int remaining = target; remaining > 0; remaining -= last[remaining]) {
    if (!first)
      std::cout << ' ';
    std::cout << last[remaining];
    first = false;
  }
  std::cout << '\n';
}
