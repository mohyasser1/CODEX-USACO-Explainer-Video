// n m followed by m directed prerequisites u->v; vertices0..n-1.
// Print any topological order, or IMPOSSIBLE if a directed cycle exists.
#include <iostream>
#include <queue>
#include <vector>
int main() {
  int n, m;
  if (!(std::cin >> n >> m) || n < 1 || n > 200000 || m < 0 || m > 200000)
    return 1;
  std::vector<std::vector<int>> g(n);
  std::vector<int> degree(n, 0), order;
  for (int i = 0; i < m; ++i) {
    int u, v;
    if (!(std::cin >> u >> v) || u < 0 || u >= n || v < 0 || v >= n)
      return 1;
    g[u].push_back(v);
    ++degree[v];
  }
  std::queue<int> ready;
  for (int u = 0; u < n; ++u)
    if (degree[u] == 0)
      ready.push(u);
  while (!ready.empty()) {
    int u = ready.front();
    ready.pop();
    order.push_back(u);
    for (int v : g[u])
      if (--degree[v] == 0)
        ready.push(v);
  }
  if (static_cast<int>(order.size()) != n) {
    std::cout << "IMPOSSIBLE\n";
    return 0;
  }
  for (int i = 0; i < n; ++i)
    std::cout << (i ? " " : "") << order[i];
  std::cout << '\n';
}
