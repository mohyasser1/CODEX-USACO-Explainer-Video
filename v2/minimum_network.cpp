// n m, then undirected u v weight edges; |weight|<=10^9. Vertices0..n-1.
// n<=200000,m<=200000. Print MST total, or DISCONNECTED if no spanning tree.
#include <algorithm>
#include <iostream>
#include <numeric>
#include <tuple>
#include <vector>
struct DSU {
  std::vector<int> parent, size;
  explicit DSU(int n) : parent(n), size(n, 1) {
    std::iota(parent.begin(), parent.end(), 0);
  }
  int find(int x) {
    while (x != parent[x]) {
      parent[x] = parent[parent[x]];
      x = parent[x];
    }
    return x;
  }
  bool unite(int a, int b) {
    a = find(a);
    b = find(b);
    if (a == b)
      return false;
    if (size[a] < size[b])
      std::swap(a, b);
    parent[b] = a;
    size[a] += size[b];
    return true;
  }
};
int main() {
  int n, m;
  if (!(std::cin >> n >> m) || n < 1 || n > 200000 || m < 0 || m > 200000)
    return 1;
  std::vector<std::tuple<long long, int, int>> edges;
  for (int i = 0; i < m; ++i) {
    int u, v;
    long long w;
    if (!(std::cin >> u >> v >> w) || u < 0 || u >= n || v < 0 || v >= n ||
        w < -1000000000LL || w > 1000000000LL)
      return 1;
    edges.push_back({w, u, v});
  }
  std::sort(edges.begin(), edges.end());
  DSU dsu(n);
  long long total = 0;
  int used = 0;
  for (auto [w, u, v] : edges)
    if (dsu.unite(u, v)) {
      total += w;
      ++used;
    }
  if (used != n - 1)
    std::cout << "DISCONNECTED\n";
  else
    std::cout << total << '\n';
}
