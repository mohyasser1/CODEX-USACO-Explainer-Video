#include "algorithms.hpp"
#include <cassert>
#include <iostream>
#include <random>
using namespace film;
int main() {
  std::mt19937 rng(20261026);
  int checks = 0;
  auto check = [&](bool ok) {
    ++checks;
    if (!ok)
      throw std::runtime_error("differential check failed: " +
                               std::to_string(checks));
  };
  for (int rep = 0; rep < 200; ++rep) {
    int n = 1 + rng() % 20;
    std::vector<ll> a(n);
    for (ll &x : a)
      x = int(rng() % 41) - 20;
    Prefix p(a);
    Fenwick fw(n);
    SegmentSum seg(a);
    LazySum lazy(n);
    for (int i = 0; i < n; ++i) {
      fw.add(i, a[i]);
      lazy.add(i, i + 1, a[i]);
    }
    for (int l = 0; l <= n; ++l)
      for (int r = l; r <= n; ++r)
        check(p.sum(l, r) ==
              std::accumulate(a.begin() + l, a.begin() + r, 0LL));
    for (int k = 0; k < 100; ++k) {
      int l = rng() % (n + 1), r = rng() % (n + 1);
      if (l > r)
        std::swap(l, r);
      ll delta = int(rng() % 21) - 10;
      if (k % 2) {
        for (int i = l; i < r; ++i) {
          a[i] += delta;
          fw.add(i, delta);
          seg.set(i, a[i]);
        }
        lazy.add(l, r, delta);
      } else {
        ll want = std::accumulate(a.begin() + l, a.begin() + r, 0LL);
        check(fw.sum(l, r) == want);
        check(seg.sum(l, r) == want);
        check(lazy.sum(l, r) == want);
      }
    }
    std::vector<std::vector<int>> g(n);
    Graph weighted(n);
    std::vector<std::vector<ll>> dist(n, std::vector<ll>(n, INF));
    DSU d(n);
    for (int i = 0; i < n; ++i)
      dist[i][i] = 0;
    for (int i = 0; i < n; ++i)
      for (int j = i + 1; j < n; ++j)
        if (rng() % 4 == 0) {
          int w = rng() % 12;
          g[i].push_back(j);
          g[j].push_back(i);
          weighted[i].push_back({j, w});
          weighted[j].push_back({i, w});
          dist[i][j] = dist[j][i] = w;
          d.unite(i, j);
        }
    for (int k = 0; k < n; ++k)
      for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
          if (dist[i][k] != INF && dist[k][j] != INF)
            dist[i][j] = std::min(dist[i][j], dist[i][k] + dist[k][j]);
    for (int s = 0; s < n; ++s) {
      auto b = bfs(g, s);
      auto z = dijkstra(weighted, s);
      for (int v = 0; v < n; ++v) {
        check(z[v] == dist[s][v]);
        check((d.find(s) == d.find(v)) == (b[v] != -1));
      }
    }
    std::vector<std::vector<int>> tree(n);
    for (int v = 1; v < n; ++v) {
      int u = rng() % v;
      tree[u].push_back(v);
      tree[v].push_back(u);
    }
    auto sums = distance_sums(tree);
    for (int s = 0; s < n; ++s) {
      auto b = bfs(tree, s);
      check(sums[s] == std::accumulate(b.begin(), b.end(), 0LL));
    }
  }
  for (int rep = 0; rep < 250; ++rep) {
    int n = 1 + rng() % 9;
    std::vector<ll> a(n);
    for (ll &x : a)
      x = 1 + rng() % 10;
    int days = 1 + rng() % n;
    // Independent exhaustive partition oracle for shipping.
    ll best = INF;
    for (int mask = 0; mask < (1 << (n - 1)); ++mask) {
      if (__builtin_popcount((unsigned)mask) + 1 > days)
        continue;
      ll peak = 0, load = a[0];
      for (int i = 1; i < n; ++i) {
        if (mask >> (i - 1) & 1) {
          peak = std::max(peak, load);
          load = 0;
        }
        load += a[i];
      }
      best = std::min(best, std::max(peak, load));
    }
    check(shipping(a, days) == best);
    int bestlis = 0;
    for (int mask = 0; mask < (1 << n); ++mask) {
      ll prev = -INF;
      int len = 0;
      bool ok = true;
      for (int i = 0; i < n; ++i)
        if (mask >> i & 1) {
          ok &= prev < a[i];
          prev = a[i];
          ++len;
        }
      if (ok)
        bestlis = std::max(bestlis, len);
    }
    check(lis(a) == bestlis);
    std::vector<std::pair<int, ll>> items;
    for (int i = 0; i < n; ++i)
      items.push_back({1 + int(rng() % 7), int(rng() % 15)});
    int W = rng() % 20;
    ll want = 0;
    for (int mask = 0; mask < (1 << n); ++mask) {
      int w = 0;
      ll val = 0;
      for (int i = 0; i < n; ++i)
        if (mask >> i & 1) {
          w += items[i].first;
          val += items[i].second;
        }
      if (w <= W)
        want = std::max(want, val);
    }
    check(knapsack(items, W) == want);
    std::vector<std::pair<ll, ll>> shows;
    for (int i = 0; i < n; ++i) {
      int s = rng() % 12;
      shows.push_back({s, s + 1 + rng() % 5});
    }
    int bestcount = 0;
    for (int mask = 0; mask < (1 << n); ++mask) {
      std::vector<std::pair<ll, ll>> v;
      for (int i = 0; i < n; ++i)
        if (mask >> i & 1)
          v.push_back(shows[i]);
      std::sort(v.begin(), v.end());
      bool ok = true;
      for (int i = 1; i < (int)v.size(); ++i)
        ok &= v[i - 1].second <= v[i].first;
      if (ok)
        bestcount = std::max(bestcount, (int)v.size());
    }
    check(schedule(shows) == bestcount);
    std::string s;
    for (int i = 0; i < n; ++i)
      s += char('a' + rng() % 3);
    auto pi = prefix_function(s);
    for (int i = 0; i < n; ++i) {
      int want = 0;
      for (int k = 1; k <= i; ++k)
        if (s.substr(0, k) == s.substr(i - k + 1, k))
          want = k;
      check(pi[i] == want);
    }
  }
  // Coin DP checked against shortest paths in the independent amount graph.
  for (int mask = 1; mask < 32; ++mask) {
    std::vector<int> coins;
    for (int c = 1; c <= 5; ++c)
      if (mask >> (c - 1) & 1)
        coins.push_back(c);
    std::vector<std::vector<int>> g(41);
    for (int s = 0; s <= 40; ++s)
      for (int c : coins)
        if (s + c <= 40)
          g[s].push_back(s + c);
    auto d = bfs(g, 0);
    for (int s = 0; s <= 40; ++s)
      check(min_coins(coins, s) == d[s]);
  }
  for (int a = -10; a <= 10; ++a)
    for (int e = 0; e <= 12; ++e) {
      ll want = 1;
      for (int k = 0; k < e; ++k)
        want = want * ((a % 7 + 7) % 7) % 7;
      check(mod_pow(a, e, 7) == want);
    }
  check(kruskal(3, {{0, 1, 2}, {1, 2, 3}, {0, 2, 10}}) ==
        std::make_pair(5LL, 2));
  check(kruskal(3, {{0, 1, 2}}) == std::make_pair(2LL, 1));
  check(topo({{2}, {2}, {}}).size() == 3);
  check(topo({{1}, {0}}).empty());
  check(shipping({3, 2, 2, 4, 1, 4}, 3) == 6);
  check(min_coins({1, 3, 4}, 6) == 2);
  check(lis({3, 1, 2, 5, 4}) == 3);

  // Exhaustive spanning-tree oracle on small weighted graphs, including
  // negatives.
  for (int rep = 0; rep < 60; ++rep) {
    int n = 2 + rng() % 4;
    std::vector<Edge> edges;
    for (int u = 0; u < n; ++u)
      for (int v = u + 1; v < n; ++v)
        if (rng() % 3)
          edges.push_back({u, v, int(rng() % 15) - 5});
    ll best = INF;
    for (int mask = 0; mask < (1 << edges.size()); ++mask) {
      if (__builtin_popcount((unsigned)mask) != n - 1)
        continue;
      std::vector<std::vector<int>> chosen(n);
      ll cost = 0;
      for (int e = 0; e < (int)edges.size(); ++e)
        if (mask >> e & 1) {
          auto x = edges[e];
          chosen[x.u].push_back(x.v);
          chosen[x.v].push_back(x.u);
          cost += x.w;
        }
      auto reach = bfs(chosen, 0);
      if (std::find(reach.begin(), reach.end(), -1) == reach.end())
        best = std::min(best, cost);
    }
    auto result = kruskal(n, edges);
    check((result.second == n - 1) == (best != INF));
    if (best != INF)
      check(result.first == best);
  }
  // Unweighted BFS distances independently checked by all-pairs Floyd-Warshall.
  for (int rep = 0; rep < 80; ++rep) {
    int n = 1 + rng() % 12;
    std::vector<std::vector<int>> g(n), dist(n, std::vector<int>(n, 1000));
    for (int u = 0; u < n; ++u) {
      dist[u][u] = 0;
      for (int v = 0; v < n; ++v)
        if (u != v && rng() % 5 == 0) {
          g[u].push_back(v);
          dist[u][v] = 1;
        }
    }
    for (int k = 0; k < n; ++k)
      for (int u = 0; u < n; ++u)
        for (int v = 0; v < n; ++v)
          dist[u][v] = std::min(dist[u][v], dist[u][k] + dist[k][v]);
    for (int u = 0; u < n; ++u) {
      auto actual = bfs(g, u);
      for (int v = 0; v < n; ++v)
        check(actual[v] == (dist[u][v] == 1000 ? -1 : dist[u][v]));
    }
  }
  check(two_sum({1500000000, 1500000000}, 3000000000LL));
  check(two_sum({-1500000000, -1500000000}, -3000000000LL));
  check(!two_sum({1500000000, 1500000000}, -1294967296LL));
  check(!two_sum({}, 0));
  check(!two_sum({1}, 2));
  for (int rep = 0; rep < 100; ++rep) {
    std::vector<int> a(10);
    for (int &v : a)
      v = (int(rng() % 3) - 1) * 1500000000;
    ll target = (ll(rng() % 5) - 2) * 1500000000LL;
    bool want = false;
    for (int i = 0; i < 10; ++i)
      for (int j = i + 1; j < 10; ++j)
        if (static_cast<ll>(a[i]) + static_cast<ll>(a[j]) == target)
          want = true;
    check(two_sum(a, target) == want);
  }
  std::cout << "PASS: " << checks
            << " deterministic and seeded differential assertions\n";
}
