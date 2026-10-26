// n m start, then directed u v weight edges. Nonnegative weights<=10^9.
// n<=200000,m<=200000. Print distances; -1 means unreachable.
#include <functional>
#include <iostream>
#include <limits>
#include <queue>
#include <utility>
#include <vector>
int main() {
  int n, m, start;
  if (!(std::cin >> n >> m >> start) || n < 1 || n > 200000 || m < 0 ||
      m > 200000 || start < 0 || start >= n)
    return 1;
  using ll = long long;
  using Entry = std::pair<ll, int>;
  std::vector<std::vector<std::pair<int, ll>>> g(n);
  for (int i = 0; i < m; ++i) {
    int u, v;
    ll w;
    if (!(std::cin >> u >> v >> w) || u < 0 || u >= n || v < 0 || v >= n ||
        w < 0 || w > 1000000000LL)
      return 1;
    g[u].push_back({v, w});
  }
  const ll inf = std::numeric_limits<ll>::max() / 4;
  std::vector<ll> d(n, inf);
  std::priority_queue<Entry, std::vector<Entry>, std::greater<Entry>> q;
  d[start] = 0;
  q.push({0, start});
  while (!q.empty()) {
    auto [distance, u] = q.top();
    q.pop();
    if (distance != d[u])
      continue;
    for (auto [v, w] : g[u])
      if (w < inf - distance && distance + w < d[v]) {
        d[v] = distance + w;
        q.push({d[v], v});
      }
  }
  for (int i = 0; i < n; ++i)
    std::cout << (i ? " " : "") << (d[i] == inf ? -1 : d[i]);
  std::cout << '\n';
}
