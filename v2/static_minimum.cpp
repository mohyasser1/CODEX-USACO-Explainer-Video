// Static nonempty range-min queries. n q, n values, then l r with0<=l<r<=n.
// 1<=n<=100000,0<=q<=100000; values magnitude<=10^9.
#include <algorithm>
#include <iostream>
#include <vector>
int main() {
  int n, q;
  if (!(std::cin >> n >> q) || n < 1 || n > 100000 || q < 0 || q > 100000)
    return 1;
  std::vector<int> logs(n + 1, 0);
  for (int i = 2; i <= n; ++i)
    logs[i] = logs[i / 2] + 1;
  std::vector<std::vector<int>> table(logs[n] + 1, std::vector<int>(n));
  for (int &x : table[0])
    if (!(std::cin >> x) || x < -1000000000 || x > 1000000000)
      return 1;
  for (int k = 1; k <= logs[n]; ++k)
    for (int i = 0; i + (1 << k) <= n; ++i)
      table[k][i] = std::min(table[k - 1][i], table[k - 1][i + (1 << (k - 1))]);
  for (int i = 0; i < q; ++i) {
    int l, r;
    if (!(std::cin >> l >> r) || l < 0 || l >= r || r > n)
      return 1;
    int k = logs[r - l];
    std::cout << std::min(table[k][l], table[k][r - (1 << k)]) << '\n';
  }
}
