#ifndef USACO_FILM_ALGORITHMS_HPP
#define USACO_FILM_ALGORITHMS_HPP
#include <algorithm>
#include <functional>
#include <limits>
#include <numeric>
#include <queue>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
namespace film {
using ll = long long;
constexpr ll INF = std::numeric_limits<ll>::max() / 4;
// All array ranges are half-open [l,r). Inputs must fit the documented types.
// Integer values, wide target; promote before addition to avoid int overflow.
inline bool two_sum(std::vector<int> a, ll target) {
  std::sort(a.begin(), a.end());
  int l = 0, r = static_cast<int>(a.size()) - 1;
  while (l < r) {
    ll sum = 1LL * a[l] + a[r];
    if (sum == target)
      return true;
    if (sum < target)
      ++l;
    else
      --r;
  }
  return false;
}
struct Prefix {
  std::vector<ll> p;
  explicit Prefix(const std::vector<ll> &a) : p(a.size() + 1) {
    for (size_t i = 0; i < a.size(); ++i)
      p[i + 1] = p[i] + a[i];
  }
  ll sum(int l, int r) const { return p.at(r) - p.at(l); }
};
struct Fenwick {
  int n;
  std::vector<ll> bit;
  explicit Fenwick(int n) : n(n), bit(n + 1) {}
  void add(int i, ll x) {
    if (i < 0 || i >= n)
      throw std::out_of_range("index");
    for (++i; i <= n; i += i & -i)
      bit[i] += x;
  }
  ll prefix(int r) const {
    if (r < 0 || r > n)
      throw std::out_of_range("boundary");
    ll s = 0;
    for (; r; r -= r & -r)
      s += bit[r];
    return s;
  }
  ll sum(int l, int r) const { return prefix(r) - prefix(l); }
};
struct DSU {
  std::vector<int> p, sz;
  explicit DSU(int n) : p(n), sz(n, 1) { std::iota(p.begin(), p.end(), 0); }
  int find(int x) {
    while (x != p[x]) {
      p[x] = p[p[x]];
      x = p[x];
    }
    return x;
  }
  bool unite(int a, int b) {
    a = find(a);
    b = find(b);
    if (a == b)
      return false;
    if (sz[a] < sz[b])
      std::swap(a, b);
    p[b] = a;
    sz[a] += sz[b];
    return true;
  }
};
std::vector<int> bfs(const std::vector<std::vector<int>> &g, int s) {
  std::vector<int> d(g.size(), -1);
  std::queue<int> q;
  d.at(s) = 0;
  q.push(s);
  while (!q.empty()) {
    int u = q.front();
    q.pop();
    for (int v : g[u])
      if (d[v] == -1) {
        d[v] = d[u] + 1;
        q.push(v);
      }
  }
  return d;
}
using Graph = std::vector<std::vector<std::pair<int, ll>>>;
// Nonnegative weights; every finite path distance must be < INF.
std::vector<ll> dijkstra(const Graph &g, int s) {
  for (const auto &edges : g)
    for (auto [v, w] : edges) {
      (void)v;
      if (w < 0)
        throw std::invalid_argument("negative edge");
    }
  std::vector<ll> d(g.size(), INF);
  using P = std::pair<ll, int>;
  std::priority_queue<P, std::vector<P>, std::greater<P>> q;
  d.at(s) = 0;
  q.push({0, s});
  while (!q.empty()) {
    auto [du, u] = q.top();
    q.pop();
    if (du != d[u])
      continue;
    for (auto [v, w] : g[u])
      if (w < INF - du && du + w < d[v]) {
        d[v] = du + w;
        q.push({d[v], v});
      }
  }
  return d;
}
// Nonempty nonnegative weights, positive days; total must fit long long.
ll shipping(const std::vector<ll> &a, int days) {
  if (a.empty() || days <= 0)
    throw std::invalid_argument("shipping inputs");
  ll lo = 0, hi = 0;
  for (ll x : a) {
    if (x < 0)
      throw std::invalid_argument("negative weight");
    lo = std::max(lo, x);
    hi += x;
  }
  auto feasible = [&](ll cap) {
    int used = 1;
    ll load = 0;
    for (ll x : a) {
      if (load > cap - x) {
        ++used;
        load = 0;
      }
      load += x;
    }
    return used <= days;
  };
  while (lo < hi) {
    ll mid = lo + (hi - lo) / 2;
    if (feasible(mid))
      hi = mid;
    else
      lo = mid + 1;
  }
  return lo;
}
int min_coins(const std::vector<int> &coins, int target) {
  const int bad = target + 1;
  std::vector<int> d(target + 1, bad);
  d[0] = 0;
  for (int c : coins)
    if (c <= 0)
      throw std::invalid_argument("nonpositive coin");
  for (int s = 1; s <= target; ++s)
    for (int c : coins)
      if (c <= s && d[s - c] != bad)
        d[s] = std::min(d[s], d[s - c] + 1);
  return d[target] == bad ? -1 : d[target];
}
ll knapsack(const std::vector<std::pair<int, ll>> &items, int W) {
  std::vector<ll> d(W + 1);
  for (auto [w, v] : items) {
    if (w <= 0)
      throw std::invalid_argument("weight must be positive");
    for (int c = W; c >= w; --c)
      d[c] = std::max(d[c], d[c - w] + v);
  }
  return d[W];
}
int lis(const std::vector<ll> &a) {
  std::vector<ll> tails;
  for (ll x : a) {
    auto it = std::lower_bound(tails.begin(), tails.end(), x);
    if (it == tails.end())
      tails.push_back(x);
    else
      *it = x;
  }
  return static_cast<int>(tails.size());
}
// Positive-length half-open intervals. Maximum cardinality, not maximum weight.
int schedule(std::vector<std::pair<ll, ll>> a) {
  std::sort(a.begin(), a.end(), [](auto x, auto y) {
    return std::pair<ll, ll>{x.second, x.first} <
           std::pair<ll, ll>{y.second, y.first};
  });
  ll end = std::numeric_limits<ll>::min();
  int count = 0;
  for (auto [s, e] : a) {
    if (s >= e)
      throw std::invalid_argument("positive interval length required");
    if (s >= end) {
      end = e;
      ++count;
    }
  }
  return count;
}
struct Edge {
  int u, v;
  ll w;
};
// Returns {forest weight, number of selected edges}; connected iff edges=n-1.
std::pair<ll, int> kruskal(int n, std::vector<Edge> e) {
  std::sort(e.begin(), e.end(), [](auto a, auto b) { return a.w < b.w; });
  DSU d(n);
  ll total = 0;
  int used = 0;
  for (auto x : e) {
    if (d.unite(x.u, x.v)) {
      total += x.w;
      ++used;
    }
  }
  return {total, used};
}
struct SegmentSum {
  int n;
  std::vector<ll> t;
  explicit SegmentSum(const std::vector<ll> &a) : n(1) {
    while (n < (int)a.size())
      n *= 2;
    t.assign(2 * n, 0);
    std::copy(a.begin(), a.end(), t.begin() + n);
    for (int i = n - 1; i; i--)
      t[i] = t[2 * i] + t[2 * i + 1];
  }
  void set(int i, ll x) {
    i += n;
    t[i] = x;
    for (i /= 2; i; i /= 2)
      t[i] = t[2 * i] + t[2 * i + 1];
  }
  ll sum(int l, int r) const {
    ll left = 0, right = 0;
    for (l += n, r += n; l < r; l /= 2, r /= 2) {
      if (l & 1)
        left += t[l++];
      if (r & 1)
        right = t[--r] + right;
    }
    return left + right;
  }
};
struct LazySum {
  int n;
  std::vector<ll> t, lazy;
  explicit LazySum(int n) : n(n), t(4 * std::max(1, n)), lazy(t.size()) {}
  void apply(int p, int l, int r, ll x) {
    t[p] += x * (r - l);
    lazy[p] += x;
  }
  void push(int p, int l, int r) {
    if (r - l <= 1)
      return;
    int m = (l + r) / 2;
    apply(p * 2, l, m, lazy[p]);
    apply(p * 2 + 1, m, r, lazy[p]);
    lazy[p] = 0;
  }
  void add_impl(int p, int l, int r, int ql, int qr, ll x) {
    if (qr <= l || r <= ql)
      return;
    if (ql <= l && r <= qr) {
      apply(p, l, r, x);
      return;
    }
    push(p, l, r);
    int m = (l + r) / 2;
    add_impl(p * 2, l, m, ql, qr, x);
    add_impl(p * 2 + 1, m, r, ql, qr, x);
    t[p] = t[p * 2] + t[p * 2 + 1];
  }
  ll sum_impl(int p, int l, int r, int ql, int qr) {
    if (qr <= l || r <= ql)
      return 0;
    if (ql <= l && r <= qr)
      return t[p];
    push(p, l, r);
    int m = (l + r) / 2;
    return sum_impl(p * 2, l, m, ql, qr) + sum_impl(p * 2 + 1, m, r, ql, qr);
  }
  void add(int l, int r, ll x) {
    if (l < r)
      add_impl(1, 0, n, l, r, x);
  }
  ll sum(int l, int r) { return l == r ? 0 : sum_impl(1, 0, n, l, r); }
};
// Returns empty on a directed cycle (also empty for an empty graph).
std::vector<int> topo(const std::vector<std::vector<int>> &g) {
  int n = g.size();
  std::vector<int> in(n), order;
  for (auto &a : g)
    for (int v : a)
      ++in[v];
  std::queue<int> q;
  for (int i = 0; i < n; ++i)
    if (!in[i])
      q.push(i);
  while (!q.empty()) {
    int u = q.front();
    q.pop();
    order.push_back(u);
    for (int v : g[u])
      if (--in[v] == 0)
        q.push(v);
  }
  if ((int)order.size() != n)
    order.clear();
  return order;
}
std::vector<int> prefix_function(const std::string &s) {
  std::vector<int> p(s.size());
  for (int i = 1; i < (int)s.size(); ++i) {
    int j = p[i - 1];
    while (j && s[i] != s[j])
      j = p[j - 1];
    if (s[i] == s[j])
      ++j;
    p[i] = j;
  }
  return p;
}
// Prime-modulus specialization is NOT assumed. Multiplication safe for mod <=
// 1e9+7.
ll mod_pow(ll a, ll b, ll mod) {
  if (mod <= 0 || mod > 1000000007LL || b < 0)
    throw std::invalid_argument("mod_pow domain");
  a = (a % mod + mod) % mod;
  ll ans = 1 % mod;
  while (b) {
    if (b & 1)
      ans = ans * a % mod;
    a = a * a % mod;
    b /= 2;
  }
  return ans;
}
// Connected unweighted tree; iterative traversal avoids recursion depth limits.
std::vector<ll> distance_sums(const std::vector<std::vector<int>> &g) {
  int n = g.size();
  if (!n)
    return {};
  std::vector<int> par(n, -1), order{0}, depth(n), sz(n, 1);
  par[0] = 0;
  for (size_t k = 0; k < order.size(); ++k) {
    int u = order[k];
    for (int v : g[u])
      if (par[v] == -1) {
        par[v] = u;
        depth[v] = depth[u] + 1;
        order.push_back(v);
      }
  }
  if ((int)order.size() != n)
    throw std::invalid_argument("disconnected");
  for (int k = n - 1; k > 0; --k) {
    int u = order[k];
    sz[par[u]] += sz[u];
  }
  std::vector<ll> ans(n);
  ans[0] = std::accumulate(depth.begin(), depth.end(), 0LL);
  for (int k = 1; k < n; ++k) {
    int v = order[k];
    ans[v] = ans[par[v]] + n - 2LL * sz[v];
  }
  return ans;
}
} // namespace film
#endif
