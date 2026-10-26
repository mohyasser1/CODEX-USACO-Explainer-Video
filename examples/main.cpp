#include "algorithms.hpp"
#include <iostream>
// Usage: ./lesson <mode> ; see workbook for sample inputs.
int main(int argc, char **argv) {
  using namespace film;
  if (argc != 2) {
    std::cerr << "Modes: sum, range, shipping, coins, lis, bfs, dijkstra\n";
    return 1;
  }
  std::string mode = argv[1];
  if (mode == "sum") {
    ll a, b;
    if (!(std::cin >> a >> b))
      return 1;
    std::cout << a + b << '\n';
  } else if (mode == "range") {
    int n, q;
    std::cin >> n >> q;
    std::vector<ll> a(n);
    for (ll &x : a)
      std::cin >> x;
    Prefix p(a);
    while (q--) {
      int l, r;
      std::cin >> l >> r;
      std::cout << p.sum(l, r) << '\n';
    }
  } else if (mode == "shipping") {
    int n, days;
    std::cin >> n >> days;
    std::vector<ll> a(n);
    for (ll &x : a)
      std::cin >> x;
    std::cout << shipping(a, days) << '\n';
  } else if (mode == "coins") {
    int n, target;
    std::cin >> n >> target;
    std::vector<int> a(n);
    for (int &x : a)
      std::cin >> x;
    std::cout << min_coins(a, target) << '\n';
  } else if (mode == "lis") {
    int n;
    std::cin >> n;
    std::vector<ll> a(n);
    for (ll &x : a)
      std::cin >> x;
    std::cout << lis(a) << '\n';
  } else if (mode == "bfs") {
    int n, m, s;
    std::cin >> n >> m >> s;
    std::vector<std::vector<int>> g(n);
    while (m--) {
      int u, v;
      std::cin >> u >> v;
      g[u].push_back(v);
      g[v].push_back(u);
    }
    for (int d : bfs(g, s))
      std::cout << d << ' ';
    std::cout << '\n';
  } else if (mode == "dijkstra") {
    int n, m, s;
    std::cin >> n >> m >> s;
    Graph g(n);
    while (m--) {
      int u, v;
      ll w;
      std::cin >> u >> v >> w;
      g[u].push_back({v, w});
    }
    for (ll d : dijkstra(g, s))
      std::cout << (d == INF ? -1 : d) << ' ';
    std::cout << '\n';
  } else
    return 1;
}
