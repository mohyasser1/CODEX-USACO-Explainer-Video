// n start, then exactly one successor for each vertex0..n-1.
// Print tail length, cycle length, cycle entry; then distinct walk vertices.
#include <iostream>
#include <vector>
int main() {
  int n, start;
  if (!(std::cin >> n >> start) || n < 1 || n > 200000 || start < 0 ||
      start >= n)
    return 1;
  std::vector<int> next(n), seen(n, -1), path;
  for (int &v : next)
    if (!(std::cin >> v) || v < 0 || v >= n)
      return 1;
  int u = start;
  while (seen[u] == -1) {
    seen[u] = static_cast<int>(path.size());
    path.push_back(u);
    u = next[u];
  }
  int tail = seen[u], cycle = static_cast<int>(path.size()) - tail;
  std::cout << tail << ' ' << cycle << ' ' << u << '\n';
  for (int i = 0; i < static_cast<int>(path.size()); ++i)
    std::cout << (i ? " " : "") << path[i];
  std::cout << '\n';
}
